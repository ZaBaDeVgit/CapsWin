"""CapsWin - Indicador visual del Bloq Mayús para Windows.

Muestra un icono verde (MAYUS) o rojo (mayus) en la bandeja del sistema y
una notificación ovalada en la parte superior central de la pantalla cada
vez que cambia el estado del Bloq Mayús.

Diseño:
  * Tkinter se ejecuta en un único hilo dedicado (Tk no es thread-safe).
  * pystray ocupa el hilo principal, como exige la API de la bandeja.
  * El estado se consulta con ctypes/user32, sin dependencias de pywin32.
"""

from __future__ import annotations

import ctypes
import logging
import os
import queue
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path

import pystray
from PIL import Image, ImageDraw, ImageFont

__version__ = "2.0.0"

APP_NAME = "CapsWin"
MUTEX_NAME = "Local\\CapsWinSingleInstance"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
VK_CAPITAL = 0x14
ERROR_ALREADY_EXISTS = 183

COLOR_ON = "#22c55e"      # verde
COLOR_OFF = "#ef4444"     # rojo
TRANSPARENT = "#010203"   # color clave para recortar las esquinas de la notificación
TEXT_COLOR = "#ffffff"

POLL_INTERVAL = 0.1       # segundos entre comprobaciones del estado
TOAST_TOP = 80            # distancia desde el borde superior (px)
TOAST_HOLD_MS = 1600      # tiempo que la notificación permanece visible
FADE_STEP = 0.1
FADE_DELAY_MS = 16

_mutex_handle = None      # se mantiene vivo mientras dure el proceso


# ---------------------------------------------------------------------------
# Registro de errores (la app va sin consola, así que no se vería nada)
# ---------------------------------------------------------------------------
def _setup_logging() -> None:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / APP_NAME
    try:
        base.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=base / "capswin.log",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
        )
    except OSError:
        logging.basicConfig(level=logging.WARNING)


log = logging.getLogger(APP_NAME)


# ---------------------------------------------------------------------------
# Sistema
# ---------------------------------------------------------------------------
def _enable_dpi_awareness() -> None:
    """Evita que la notificación se vea borrosa en pantallas con escalado."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # PROCESS_SYSTEM_DPI_AWARE
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass


def _acquire_single_instance() -> bool:
    """Devuelve False si ya hay otra instancia de CapsWin en ejecución."""
    global _mutex_handle
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _mutex_handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    return ctypes.get_last_error() != ERROR_ALREADY_EXISTS


def is_caps_lock_on() -> bool:
    return bool(ctypes.windll.user32.GetKeyState(VK_CAPITAL) & 1)


# ---------------------------------------------------------------------------
# Inicio automático (HKCU\...\Run)
# ---------------------------------------------------------------------------
def _startup_command() -> str:
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'
    # Ejecutado desde código fuente: usar pythonw para no abrir consola.
    py = Path(sys.executable)
    pyw = py.with_name("pythonw.exe")
    interpreter = pyw if pyw.exists() else py
    return f'"{interpreter}" "{Path(__file__).resolve()}"'


def is_startup_enabled() -> bool:
    import winreg

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0,
                            winreg.KEY_QUERY_VALUE) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except OSError:
        return False


def set_startup(enabled: bool) -> None:
    import winreg

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0,
                        winreg.KEY_SET_VALUE) as key:
        if enabled:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _startup_command())
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass


# ---------------------------------------------------------------------------
# Iconos
# ---------------------------------------------------------------------------
_RESAMPLE = getattr(Image, "Resampling", Image).LANCZOS


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("segoeuib.ttf", "arialbd.ttf", "arial.ttf",
                 "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size)  # Pillow >= 10.1
    except TypeError:
        return ImageFont.load_default()


def create_icon(color: str, text: str, size: int = 64, scale: int = 4) -> Image.Image:
    """Icono redondeado con el texto centrado.

    Se dibuja a 4x y se reduce con LANCZOS para obtener bordes suavizados.
    """
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = 2 * scale
    draw.rounded_rectangle((pad, pad, s - pad, s - pad),
                           radius=int(s * 0.22), fill=color)

    max_width = s - 12 * scale
    font_size = int(s * 0.36)
    font = _load_font(font_size)
    while True:
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        if right - left <= max_width or font_size <= 8 * scale:
            break
        font_size -= scale
        font = _load_font(font_size)

    x = (s - (right - left)) / 2 - left
    y = (s - (bottom - top)) / 2 - top
    draw.text((x, y), text, fill=TEXT_COLOR, font=font)
    return img.resize((size, size), _RESAMPLE)


ICON_ON = create_icon(COLOR_ON, "MAYUS")
ICON_OFF = create_icon(COLOR_OFF, "mayus")


# ---------------------------------------------------------------------------
# Notificaciones (un único hilo con Tk)
# ---------------------------------------------------------------------------
class ToastNotifier:
    """Muestra una notificación ovalada cada vez que se le pide.

    Las llamadas a `show()` son seguras desde cualquier hilo: solo encolan el
    evento. Toda la interacción con Tk ocurre en el hilo propio de este objeto.
    Si llega una nueva notificación mientras hay una visible, la reemplaza.
    """

    def __init__(self) -> None:
        self._queue: queue.SimpleQueue[bool] = queue.SimpleQueue()
        self._current: tk.Toplevel | None = None
        self._root: tk.Tk | None = None
        self._font: tkfont.Font | None = None
        self._thread = threading.Thread(target=self._run, name="toast", daemon=True)
        self._thread.start()

    def show(self, is_on: bool) -> None:
        self._queue.put(is_on)

    # -- hilo de Tk ---------------------------------------------------------
    def _run(self) -> None:
        try:
            self._root = tk.Tk()
            self._root.withdraw()
            self._font = tkfont.Font(root=self._root, family="Segoe UI Semibold", size=12)
            self._poll()
            self._root.mainloop()
        except Exception:
            log.exception("La ventana de notificaciones se ha detenido")

    def _poll(self) -> None:
        latest = None
        try:
            while True:
                latest = self._queue.get_nowait()
        except queue.Empty:
            pass
        if latest is not None:
            self._display(latest)
        self._root.after(50, self._poll)

    def _display(self, is_on: bool) -> None:
        if self._current is not None:
            self._current.destroy()
            self._current = None

        root = self._root
        text = "MAYÚS ACTIVADO" if is_on else "MAYÚS DESACTIVADO"
        color = COLOR_ON if is_on else COLOR_OFF

        height = 52
        dot = 10
        pad_x = 26
        gap = 12
        width = pad_x + dot + gap + self._font.measure(text) + pad_x
        x = (root.winfo_screenwidth() - width) // 2

        win = tk.Toplevel(root)
        self._current = win
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.0)
        win.configure(bg=TRANSPARENT)
        win.geometry(f"{width}x{height}+{x}+{TOAST_TOP}")
        try:
            # En Windows las esquinas del canvas se vuelven transparentes.
            win.attributes("-transparentcolor", TRANSPARENT)
        except tk.TclError:
            pass

        canvas = tk.Canvas(win, width=width, height=height, bg=TRANSPARENT,
                           highlightthickness=0, bd=0)
        canvas.pack()
        r = height // 2
        # Cápsula: dos semicírculos y un rectángulo central, todo del mismo color.
        canvas.create_oval(0, 0, height, height, fill=color, outline=color)
        canvas.create_oval(width - height, 0, width, height, fill=color, outline=color)
        canvas.create_rectangle(r, 0, width - r, height, fill=color, outline=color)

        cy = height // 2
        cx = pad_x
        canvas.create_oval(cx, cy - dot // 2, cx + dot, cy + dot // 2,
                           fill=TEXT_COLOR, outline=TEXT_COLOR)
        canvas.create_text(cx + dot + gap, cy, text=text, anchor="w",
                           fill=TEXT_COLOR, font=self._font)

        self._fade(win, 1.0, then=lambda: win.after(TOAST_HOLD_MS,
                                                   lambda: self._fade(win, 0.0, then=lambda: self._close(win))))

    def _fade(self, win: tk.Toplevel, target: float, then=None) -> None:
        if self._current is not win:      # ya reemplazada o cerrada
            return
        try:
            alpha = float(win.attributes("-alpha"))
            if abs(alpha - target) < FADE_STEP / 2:
                win.attributes("-alpha", target)
                if then:
                    then()
                return
            alpha += FADE_STEP if alpha < target else -FADE_STEP
            win.attributes("-alpha", min(max(alpha, 0.0), 1.0))
            win.after(FADE_DELAY_MS, lambda: self._fade(win, target, then))
        except tk.TclError:
            self._close(win)

    def _close(self, win: tk.Toplevel) -> None:
        if self._current is win:
            self._current = None
        try:
            win.destroy()
        except tk.TclError:
            pass


# ---------------------------------------------------------------------------
# Bandeja del sistema
# ---------------------------------------------------------------------------
def apply_state(icon: pystray.Icon, is_on: bool) -> None:
    icon.icon = ICON_ON if is_on else ICON_OFF
    icon.title = ("CapsWin: Bloq Mayús activado" if is_on
                  else "CapsWin: Bloq Mayús desactivado")


def monitor(icon: pystray.Icon, toast: ToastNotifier) -> None:
    """Hilo de fondo: detecta cambios del Bloq Mayús y actualiza la UI."""
    state: bool | None = None
    while True:
        try:
            current = is_caps_lock_on()
            if current != state:
                first_run = state is None
                state = current
                apply_state(icon, current)
                if not first_run:          # no notificar al arrancar
                    toast.show(current)
        except Exception:
            log.exception("Error al comprobar el Bloq Mayús")
        time.sleep(POLL_INTERVAL)


def on_toggle_startup(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    try:
        set_startup(not is_startup_enabled())
    except OSError:
        log.exception("No se pudo cambiar el inicio automático")


def on_quit(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    icon.stop()


def build_menu() -> pystray.Menu:
    return pystray.Menu(
        pystray.MenuItem("Iniciar con Windows", on_toggle_startup,
                         checked=lambda item: is_startup_enabled()),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir", on_quit),
    )


def main() -> None:
    _setup_logging()
    _enable_dpi_awareness()
    if not _acquire_single_instance():
        log.info("CapsWin ya está en ejecución; saliendo.")
        return

    icon = pystray.Icon(APP_NAME, ICON_OFF, APP_NAME, build_menu())
    toast = ToastNotifier()
    threading.Thread(target=monitor, args=(icon, toast), name="monitor",
                     daemon=True).start()
    icon.run()


if __name__ == "__main__":
    main()

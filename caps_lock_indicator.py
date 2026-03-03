import pystray
from PIL import Image, ImageDraw, ImageFont
import win32api
import time
import threading
import tkinter as tk
import sys
import os

def create_icon(color, text=" "):
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.rectangle((4, 4, 60, 60), fill=color)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (64 - text_width) // 2
    y = (64 - text_height) // 2
    draw.text((x, y), text, fill='white', font=font)
    return image

icon_on = create_icon((0, 255, 0), "MAYUS")
icon_off = create_icon((255, 0, 0), "mayus")

def is_caps_lock_on():
    return win32api.GetKeyState(0x14) & 1 == 1

def show_notification(is_on):
    def notify_thread():
        message = "MAYUS ACTIVADO" if is_on else "MAYUS DESACTIVADO"
        bg_color = "#22c55e" if is_on else "#ef4444"
        
        root = tk.Tk()
        root.title("")
        root.overrideredirect(True)
        
        screen_w = root.winfo_screenwidth()
        
        w, h = 220, 50
        x = (screen_w - w) // 2
        y = 80
        
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.configure(bg=bg_color)
        root.attributes("-topmost", True)
        
        canvas = tk.Canvas(root, width=w, height=h, bg=bg_color, highlightthickness=0)
        canvas.pack()
        
        canvas.create_oval(4, 4, w-4, h-4, fill=bg_color, outline=bg_color)
        
        label = tk.Label(
            root,
            text=message,
            font=("Segoe UI", 14, "bold"),
            bg=bg_color,
            fg="white"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        
        root.after(2000, root.destroy)
        root.mainloop()
    
    threading.Thread(target=notify_thread, daemon=True).start()

def add_to_startup():
    import winreg
    exe_path = sys.executable
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "CapsWin", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except:
        pass

def check_caps_lock(icon):
    current_state = None
    while True:
        new_state = is_caps_lock_on()
        if new_state != current_state:
            current_state = new_state
            if new_state:
                icon.icon = icon_on
                icon.title = "Caps Lock: ON"
                show_notification(True)
            else:
                icon.icon = icon_off
                icon.title = "Caps Lock: OFF"
                show_notification(False)
        time.sleep(0.1)

def on_quit(icon, item):
    icon.stop()

def on_setup(icon, item):
    add_to_startup()

menu = (
    pystray.MenuItem('Iniciar con Windows', on_setup),
    pystray.MenuItem('Quit', on_quit),
)

icon = pystray.Icon('caps_lock_indicator', icon_off, "Caps Lock Indicator", menu)

thread = threading.Thread(target=check_caps_lock, args=(icon,))
thread.daemon = True
thread.start()

icon.run()

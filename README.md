<p align="center">
  <img src="https://capslock.win/static/logo.svg" width="120" alt="CapsWin Logo"/>
</p>

<h1 align="center">CapsWin</h1>

<p align="center">
  <strong>Indicador visual del Bloq Mayús para Windows</strong><br>
  Una aplicación minimalista que muestra el estado de Bloq Mayús de forma clara y elegante.
</p>

<p align="center">
  <img src="https://img.shields.io/github/release/ZaBaDeV/CapsWin?color=22c55e&label=Versi%C3%B3n" alt="Versión">
  <img src="https://img.shields.io/github/license/ZaBaDeV/CapsWin?color=3b82f6" alt="Licencia">
  <img src="https://img.shields.io/github/stars/ZaBaDeV/CapsWin?color=yellow" alt="Estrellas">
</p>

---

## ✨ Características

| Característica | Descripción |
|----------------|-------------|
| 🎨 **Notificación en cápsula** | Aparece centrada arriba, con fundido suave y el color del estado |
| 🟢🔴 **Icono en la bandeja** | Verde con `MAYUS` (activado) o rojo con `mayus` (desactivado) |
| 🔍 **Nítida en cualquier pantalla** | Compatible con escalado de Windows (DPI) |
| 🚀 **Inicio automático** | Activable o desactivable desde el menú de la bandeja |
| ⚡ **Bajo consumo** | Un solo hilo de interfaz, sin ventanas ni hilos acumulados |
| 🔒 **Una sola instancia** | Si ya está abierta, no se lanza una segunda copia |

---

## 📸 Capturas de Pantalla

<p align="center">
  <img src="https://capslock.win/static/screenshot-on.png" width="400" alt="CapsWin Activado"/>
  <img src="https://capslock.win/static/screenshot-off.png" width="400" alt="CapsWin Desactivado"/>
</p>

---

## 📥 Descarga

### Instalador (recomendado)
[**Descargar CapsWin_Setup.exe**](https://github.com/ZaBaDeV/CapsWin/releases/latest/download/CapsWin_Setup.exe)

### Portable
[**Descargar CapsWin.exe**](https://github.com/ZaBaDeV/CapsWin/releases/latest/download/CapsWin.exe)

---

## 🛠️ Instalación

### Con instalador
1. Descarga `CapsWin_Setup.exe`.
2. Ejecútalo y sigue los pasos (el idioma es español).
3. ¡Listo! La aplicación se iniciará automáticamente.

### Portable
1. Descarga `CapsWin.exe`.
2. Ejecútalo.
3. El icono aparecerá en la bandeja del sistema.

---

## 💻 Uso

- **Icono en la bandeja**: indica el estado del Bloq Mayús.
  - 🟢 Verde con «MAYUS» = Bloq Mayús activado
  - 🔴 Rojo con «mayus» = Bloq Mayús desactivado
- **Menú contextual** (clic derecho en el icono):
  - ✅ **Iniciar con Windows**: activa o desactiva el inicio automático.
  - ❌ **Salir**: cierra CapsWin.
- **Registro de errores**: `%LOCALAPPDATA%\CapsWin\capswin.log`.

---

## 🔧 Desarrollo

### Requisitos
- Windows 10/11
- Python 3.9+

```bash
pip install -r requirements.txt
```

### Ejecutar desde código fuente
```bash
python caps_lock_indicator.py
```

### Compilar el ejecutable
```bash
pip install pyinstaller
pyinstaller caps_lock_indicator.spec
```
Genera `dist\CapsWin.exe`.

### Compilar el instalador
Requiere [Inno Setup 6](https://jrsoftware.org/isinfo.php) y el ejecutable anterior:
```bash
iscc setup.iss
```
Genera `Output\CapsWin_Setup.exe`.

---

## 📁 Estructura del proyecto

```
CapsWin/
├── caps_lock_indicator.py    # Código principal
├── caps_lock_indicator.spec  # Configuración de PyInstaller
├── setup.iss                 # Script de Inno Setup
├── requirements.txt          # Dependencias de Python
├── README.md
├── dist/                     # Ejecutable compilado (generado)
└── Output/                   # Instalador compilado (generado)
```

---

## 📝 Licencia

Este proyecto se distribuye bajo licencia MIT.

---

## 👨‍💻 Autor

**ZaBaDeV** - Creador del proyecto

<p align="center">
  <a href="https://github.com/ZaBaDeV">
    <img src="https://img.shields.io/badge/GitHub-ZaBaDeV-181717?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
</p>

---

<p align="center">
  <sub>Creado con ❤️ por <a href="https://github.com/ZaBaDeV">ZaBaDeV</a> en 2026</sub>
</p>

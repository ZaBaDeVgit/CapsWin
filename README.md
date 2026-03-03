<p align="center">
  <img src="https://capslock.win/static/logo.svg" width="120" alt="CapsWin Logo"/>
</p>

<h1 align="center">CapsWin</h1>

<p align="center">
  <strong>Indicador visual del Bloq Mayús para Windows</strong><br>
  Una aplicación minimalista que muestra el estado de Bloq Mayús de forma clara y elegante.
</p>

<p align="center">
  <img src="https://img.shields.io/github/release/ZaBaDeV/CapsWin?color=22c55e&label=Versi%C3%B3n" alt="Version">
  <img src="https://img.shields.io/github/license/ZaBaDeV/CapsWin?color=3b82f6" alt="Licencia">
  <img src="https://img.shields.io/github/stars/ZaBaDeV/CapsWin?color=yellow" alt="Estrellas">
</p>

---

## ✨ Características

| Característica | Descripción |
|----------------|-------------|
| 🎨 **Diseño Moderno** | Notificaciones ovaladas con colores vibrantes |
| 🟢🔴 **Indicador Visual** | Icono verde/rojo en la bandeja del sistema |
| 📍 **Posición Inteligente** | Notificaciones aparecen en la parte superior central |
| 🚀 **Inicio Automático** | Se ejecuta al iniciar Windows |
| ⚡ **Bajo Consumo** | Uso mínimo de recursos del sistema |
| 🔔 **Notificaciones Bonitas** | Diseño ovalado con fondo verde (activado) o rojo (desactivado) |

---

## 📸 Capturas de Pantalla

<p align="center">
  <img src="https://capslock.win/static/screenshot-on.png" width="400" alt="CapsWin Activado"/>
  <img src="https://capslock.win/static/screenshot-off.png" width="400" alt="CapsWin Desactivado"/>
</p>

---

## 📥 Descarga

### Instalador (Recomendado)
[**Descargar CapsWin_Setup.exe**](https://github.com/ZaBaDeV/CapsWin/releases/latest/download/CapsWin_Setup.exe)

### Portable
[**Descargar CapsWin.exe**](https://github.com/ZaBaDeV/CapsWin/releases/latest/download/CapsWin.exe)

---

## 🛠️ Instalación

### Con Instalador
1. Descarga `CapsWin_Setup.exe`
2. Ejecuta el instalador
3. ¡Listo! La aplicación se iniciara automáticamente

### Portable
1. Descarga `CapsWin.exe`
2. Ejecuta el archivo
3. La aplicación aparecera en la bandeja del sistema

---

## 💻 Uso

- **Icono en bandeja**: El icono en la bandeja del sistema indica el estado:
  - 🟢 Verde con "MAYUS" = Bloq Mayús activado
  - 🔴 Rojo con "mayus" = Bloq Mayús desactivado

- **Menú contextual**: Clic derecho en el icono para:
  - ✅ Iniciar con Windows
  - ❌ Salir

---

## 🔧 Desarrollo

### Requisitos
```
Python 3.8+
pystray
Pillow
pywin32
```

### Instalación de dependencias
```bash
pip install pystray pillow pywin32
```

### Ejecutar desde código fuente
```bash
python caps_lock_indicator.py
```

### Compilar EXE
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole caps_lock_indicator.py
```

### Compilar instalador
```bash
pip install innosetup
iscc setup.iss
```

---

## 📁 Estructura del Proyecto

```
CapsWin/
├── caps_lock_indicator.py   # Código principal
├── setup.iss               # Script de Inno Setup
├── README.md               # Este archivo
├── dist/
│   └── CapsWin.exe         # Ejecutable compilado
└── Output/
    └── CapsWin_Setup.exe  # Instalador
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más información.

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

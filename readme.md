# 🎬 YouTube Downloader (FastAPI)

Aplicación local desarrollada en **Python + FastAPI** que permite **descargar videos de YouTube sin anuncios**, eligiendo **la calidad disponible** directamente desde YouTube.

> ⚠️ El uso de esta herramienta debe respetar los **Términos de Servicio de YouTube**. Está pensada para uso educativo y personal.

---

## 🚀 Características

- Descarga de videos de YouTube **sin anuncios**
- Selección de **calidad disponible** (según YouTube)
- Servidor web local con **FastAPI**
- Interfaz accesible desde el navegador
- Descarga y procesamiento local

---

## 🧩 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

### 1️⃣FFmpeg (obligatorio)

Este proyecto **requiere FFmpeg** para el procesamiento de audio y video.

#### ✅ Instalación en Windows usando `winget`

Ejecuta en **PowerShell** o **CMD**:

```powershell
winget install ffmpeg
```

Verifica la instalación:

```bash
ffmpeg -version
```

> Si el comando no se reconoce, reinicia la terminal o el sistema.

---

## 📦 Instalación del proyecto

1. Descarga el último release desde GitHub
2. Ejecuta el archivo `YTDownloader.exe`
3. Completa la instalación con Innosetup

---

## ▶️ Ejecución

Inicia el programa `YouTube Downloader.exe`
---

## 🌐 Acceso desde el navegador

Una vez iniciado, la aplicación estará disponible en:

```
http://127.0.0.1:8000
```

---

## 🛠️ Tecnologías utilizadas

- **Python**
- **FastAPI**
- **Uvicorn**
- **FFmpeg**
- **yt-dlp / youtube-dl** (según implementación)

---

## 📌 Notas importantes

- El programa **solo permite calidades disponibles en YouTube**
- Todo se ejecuta **localmente**, no usa servidores externos
- FFmpeg es obligatorio para combinar audio y video en alta calidad

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

---

## 🙌 Autor

Desarrollado por **KarmaDevz**


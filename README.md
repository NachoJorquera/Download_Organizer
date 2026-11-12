# Download Organizer para macOS 📁

Un organizador automático de archivos para la carpeta Downloads que utiliza LaunchAgent de macOS para monitorear y organizar archivos automáticamente según su tipo.

## ✨ Características

- **Organización automática**: Detecta nuevos archivos en Downloads y los organiza instantáneamente
- **Categorización inteligente**: Organiza archivos por tipo (Documentos, Imágenes, Media, etc.)
- **Detección de Screenshots**: Identifica automáticamente screenshots de macOS
- **Ejecución en background**: Funciona silenciosamente usando LaunchAgent
- **Sin dependencias externas**: Usa solo Python del sistema

## 📋 Requisitos

- **macOS** (cualquier versión moderna)
- **Python 3** (preinstalado en macOS)
- **Terminal** o **Warp**

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Download_Organizer.git
cd Download_Organizer
```

### 2. Configurar permisos del script

```bash
chmod +x launch_organizer.sh install.sh
```

### 3. Crear el archivo `.env`

```bash
cp .env.example .env
```

`.env` define `DOWNLOADS_PATH`, la carpeta que se vigila y organiza. Por defecto es `$HOME/Downloads`. Git ignora este archivo.

Edita `config.py` si quieres personalizar las categorías y extensiones:

```bash
nano config.py
```

### 4. Configurar permisos de macOS

**⚠️ IMPORTANTE**: Debes otorgar permisos de "Full Disk Access" a los siguientes componentes:

1. Abre **System Settings** → **Privacy & Security**
2. Selecciona **"Full Disk Access"** en la barra lateral
3. Haz clic en el botón **"+"** y agrega:
   - `/usr/bin/python3`
   - `/bin/bash`
   - `/Applications/Utilities/Terminal.app` (si usas Terminal)
   - `/Applications/Warp.app` (si usas Warp)

### 5. Instalar el LaunchAgent

```bash
./install.sh
```

`install.sh` copia el plist a `~/Library/LaunchAgents/` con las rutas de `.env` y de la carpeta del proyecto, y carga el servicio. Vuelve a ejecutarlo si cambias `.env` o mueves el proyecto.

### 6. Verificar instalación

```bash
# Verificar que el servicio esté cargado
launchctl list | grep com.project.organize_downloads

# Deberías ver algo como: -    0    com.project.organize_downloads
```

## 🧪 Probar funcionamiento

1. **Crea un archivo de prueba en Downloads:**
   ```bash
   touch ~/Downloads/test.pdf
   ```

2. **Espera unos segundos** y verifica que se movió a `~/Downloads/Documents/`

3. **El organizador está funcionando** si el archivo desapareció de la raíz de Downloads

## 📁 Estructura de carpetas

El organizador creará automáticamente estas carpetas en `~/Downloads/`:

- **📄 Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`
- **🖼️ Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`
- **📸 Screenshots**: Screenshots de macOS (patrón específico)
- **🗜️ Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **📊 Excels**: `.xls`, `.xlsx`, `.csv`
- **📽️ Media**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.mp3`, `.wav`
- **🎨 SVGs**: `.svg`
- **💾 Codes**: `.py`, `.js`, `.html`, `.css`, `.json`
- **📑 PPTs**: `.ppt`, `.pptx`

## 🔧 Comandos útiles

### Gestión del servicio

```bash
# Detener el servicio
launchctl unload ~/Library/LaunchAgents/com.project.organize_downloads.plist

# Iniciar el servicio
launchctl load ~/Library/LaunchAgents/com.project.organize_downloads.plist

# Verificar estado
launchctl list | grep com.project.organize_downloads

# Ejecutar manualmente (para pruebas)
python3 download_organizer.py
```

### Desinstalación

```bash
# Detener y eliminar el servicio
launchctl unload ~/Library/LaunchAgents/com.project.organize_downloads.plist
rm ~/Library/LaunchAgents/com.project.organize_downloads.plist

# Eliminar el directorio del proyecto
rm -rf ~/Downloads/Download_Organizer
```

## 🛠️ Personalización

### Agregar nuevas categorías

Edita `config.py` para agregar nuevos tipos de archivo:

```python
CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
    "MiCategoria": [".ext1", ".ext2"],  # Nueva categoría
    # ... resto de categorías
}
```

### Cambiar ruta de Downloads

Edita `DOWNLOADS_PATH` en `.env` y vuelve a ejecutar `./install.sh`:

```bash
DOWNLOADS_PATH="/ruta/a/tu/carpeta"
```

## 🔍 Solución de problemas

### El servicio no organiza archivos

1. **Verificar permisos**: Asegúrate de haber agregado todos los componentes a "Full Disk Access"
2. **Verificar estado del servicio**:
   ```bash
   launchctl list | grep com.project.organize_downloads
   ```
3. **Verificar logs**:
   ```bash
   cat /tmp/com.project.organize_downloads.out
   cat /tmp/com.project.organize_downloads.err
   ```

### Error "Permission denied"

- Revisa que `/usr/bin/python3` y `/bin/bash` tengan "Full Disk Access"
- Reinicia el servicio después de otorgar permisos

### El servicio no se carga

```bash
# Verificar sintaxis del plist
plutil -lint ~/Library/LaunchAgents/com.project.organize_downloads.plist

# Verificar permisos del script
ls -la launch_organizer.sh
# Debe mostrar: -rwxr-xr-x
```

## 📝 Notas

- El organizador funciona **solo con archivos nuevos** que se agreguen a Downloads
- **No reorganiza** archivos existentes al instalar
- Los **archivos en subcarpetas** no son procesados
- El servicio se ejecuta **automáticamente** al detectar cambios

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

**⭐ ¡Si te resultó útil, dale una estrella al repositorio!**


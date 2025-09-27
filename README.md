# 🖥️ Prototipo de Sistema Operativo - Sistema de Archivos

## 📋 Descripción del Proyecto

Este proyecto implementa un **sistema de archivos simulado** como parte de un prototipo de sistema operativo educativo. El sistema utiliza una estructura tipo FAT simplificada y proporciona operaciones CRUD completas para archivos y directorios, con persistencia en disco virtual.

## 🎯 Objetivos

- **Simular** el funcionamiento de un sistema de archivos real
- **Implementar** operaciones básicas de gestión de archivos y directorios
- **Demostrar** conceptos fundamentales de sistemas operativos
- **Proporcionar** una interfaz interactiva para experimentar con el sistema

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **FileSystem** (`filesystem.py`)
   - Clase principal que gestiona el sistema de archivos
   - Implementa estructura tipo FAT simplificada
   - Maneja operaciones CRUD y navegación

2. **VirtualDisk** (`filesystem.py`)
   - Simula un disco virtual usando archivos JSON
   - Proporciona persistencia de datos
   - Gestiona la tabla FAT

3. **OSShell** (`shell.py`)
   - Interfaz de línea de comandos interactiva
   - Implementa comandos similares a sistemas Unix/Windows
   - Proporciona experiencia de usuario completa

4. **FileNode** (`filesystem.py`)
   - Representa archivos y directorios en memoria
   - Mantiene metadatos y relaciones jerárquicas
   - Estructura de árbol para navegación eficiente

## 🚀 Características Implementadas

### ✅ Operaciones CRUD
- **Crear**: Archivos y directorios
- **Leer**: Contenido de archivos
- **Actualizar**: Modificar contenido existente
- **Eliminar**: Archivos y directorios vacíos

### ✅ Sistema de Directorios
- Navegación jerárquica (cd, pwd)
- Listado de contenido (ls, dir)
- Creación de estructura de carpetas (mkdir)
- Visualización en árbol (tree)

### ✅ Persistencia
- Almacenamiento en disco virtual (JSON)
- Carga automática al iniciar
- Guardado automático tras modificaciones

### ✅ Interfaz de Usuario
- Shell interactivo con comandos familiares
- Mensajes informativos con emojis
- Manejo de errores robusto
- Ayuda integrada

## 📁 Estructura del Proyecto

```
os-prototype-fs/
├── filesystem.py      # Sistema de archivos principal
├── shell.py          # Interfaz de comandos
├── demo.py           # Demostración automatizada
├── README.md         # Este archivo
├── virtual_disk.json # Disco virtual (se crea automáticamente)
└── venv/            # Entorno virtual de Python
```

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.7 o superior
- Sistema operativo: Windows, Linux, o macOS

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd os-prototype-fs
   ```

2. **Activar el entorno virtual** (opcional pero recomendado)
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Verificar instalación de Python**
   ```bash
   python --version
   ```

## 🎮 Uso del Sistema

### Modo Interactivo (Recomendado)

Ejecutar el shell interactivo:
```bash
python shell.py
```

### Modo Demostración

Ejecutar demostración automatizada:
```bash
python demo.py
```

## 📖 Comandos Disponibles

### 📁 Navegación y Listado
- `ls`, `dir` - Lista archivos y directorios
- `cd <directorio>` - Cambia de directorio
- `pwd` - Muestra directorio actual
- `tree` - Muestra árbol de directorios

### 📂 Gestión de Directorios
- `mkdir <nombre>` - Crea un directorio
- `rmdir <nombre>` - Elimina un directorio vacío

### 📄 Gestión de Archivos
- `touch <archivo>` - Crea un archivo vacío
- `cat <archivo>` - Muestra contenido de archivo
- `echo <texto> > <archivo>` - Escribe texto en archivo
- `rm <archivo>` - Elimina un archivo
- `cp <origen> <destino>` - Copia un archivo

### 🔧 Sistema
- `info` - Información del sistema
- `clear` - Limpia la pantalla
- `help` - Muestra ayuda de comandos
- `exit`, `quit` - Sale del sistema

## 💡 Ejemplos de Uso

### Ejemplo 1: Crear estructura básica
```bash
OS-FS:/$ mkdir documentos
OS-FS:/$ mkdir proyectos
OS-FS:/$ ls
OS-FS:/$ cd documentos
OS-FS:/documentos$ touch readme.txt
OS-FS:/documentos$ echo "Hola mundo" > readme.txt
OS-FS:/documentos$ cat readme.txt
```

### Ejemplo 2: Navegación y gestión
```bash
OS-FS:/$ tree
OS-FS:/$ cd proyectos
OS-FS:/proyectos$ mkdir mi_proyecto
OS-FS:/proyectos$ cd mi_proyecto
OS-FS:/proyectos/mi_proyecto$ touch main.py
OS-FS:/proyectos/mi_proyecto$ pwd
```

## 🔧 Detalles Técnicos

### Estructura de Datos
- **Tabla FAT**: Almacenada en formato JSON
- **Árbol de nodos**: Estructura en memoria para navegación rápida
- **Metadatos**: Timestamps, permisos, tamaños

### Persistencia
- Archivo JSON como "disco virtual"
- Guardado automático tras cada operación
- Carga automática al inicializar

### Limitaciones Actuales
- Tamaño máximo de archivo: Limitado por memoria disponible
- Sin compresión de datos
- Sin fragmentación de archivos
- Sin usuarios ni permisos avanzados

## 🧪 Testing y Validación

### Ejecutar Demostración
```bash
python demo.py
```

La demostración incluye:
- Creación de directorios y archivos
- Operaciones CRUD completas
- Navegación entre directorios
- Verificación de persistencia

### Casos de Prueba Manual
1. Crear archivos con contenido
2. Navegar entre directorios
3. Modificar archivos existentes
4. Eliminar archivos y directorios
5. Reiniciar y verificar persistencia

## 🚧 Posibles Mejoras Futuras

- **Permisos de usuario**: Sistema de usuarios y permisos
- **Compresión**: Compresión de archivos grandes
- **Fragmentación**: Simulación de fragmentación de disco
- **Journaling**: Sistema de registro de transacciones
- **GUI**: Interfaz gráfica de usuario
- **Red**: Compartición de archivos en red

## 👥 Contribución al Proyecto de Equipo

Este módulo de **Sistema de Archivos** se integra con otros componentes del prototipo de OS:

- **Gestión de Procesos**: Puede acceder a archivos ejecutables
- **Gestión de Memoria**: Carga archivos en memoria virtual
- **Interfaz de Usuario**: Proporciona comandos de archivo al shell principal

## 📝 Notas de Desarrollo

### Decisiones de Diseño
- **JSON para persistencia**: Fácil de leer y debuggear
- **Estructura de árbol**: Navegación eficiente
- **Comandos familiares**: Experiencia de usuario intuitiva

### Consideraciones de Rendimiento
- Carga completa en memoria al iniciar
- Guardado tras cada operación (trade-off seguridad/rendimiento)
- Búsqueda lineal en directorios (aceptable para prototipo)

## 📞 Soporte

Para preguntas o problemas:
1. Revisar este README
2. Ejecutar `python shell.py` y usar comando `help`
3. Revisar código fuente con comentarios detallados

---

**🎓 Proyecto Educativo - Sistemas Operativos**  
*Implementación de Sistema de Archivos Simulado*
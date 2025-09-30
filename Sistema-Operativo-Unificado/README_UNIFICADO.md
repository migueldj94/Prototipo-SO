# Sistema Operativo Unificado - Prototipo Educativo

## 📋 Descripción

Este proyecto es un **Sistema Operativo Unificado** que integra múltiples funcionalidades de gestión de sistema en una sola aplicación educativa. Combina gestión de procesos, sistema de archivos simulado, y herramientas de monitoreo del sistema.

## 📦 Instalación y Configuración

### 🔧 Requisitos del Sistema
- **Python 3.7+** instalado en el sistema
- **pip** (gestor de paquetes de Python)
- **psutil** (se instala automáticamente desde requirements.txt)

## 🚀 Características Principales

### 🔧 Gestión de Procesos
- **Listar Procesos**: Visualización completa de todos los procesos en ejecución
- **Información Detallada**: Obtener datos específicos de cualquier proceso (CPU, memoria, estado)
- **Iniciar Procesos**: Crear nuevos procesos con diferentes configuraciones
- **Finalizar Procesos**: Terminar procesos de forma segura por PID o nombre
- **Búsqueda**: Encontrar procesos por nombre con filtros avanzados
- **Estadísticas**: Monitoreo en tiempo real de CPU, memoria y sistema

### 📁 Sistema de Archivos Simulado
- **Navegación**: Cambio de directorios con comandos tipo Unix/Linux
- **Gestión de Archivos**: Crear, eliminar, y visualizar archivos
- **Gestión de Directorios**: Crear y eliminar directorios
- **Información**: Obtener detalles de archivos y directorios (permisos, tamaño, fechas)
- **Persistencia**: Los datos se guardan automáticamente en JSON

### 📊 Monitoreo del Sistema
- **Estadísticas en Tiempo Real**: CPU, memoria, número de procesos
- **Procesos Recientes**: Visualización de los últimos procesos iniciados
- **Información del Sistema**: Detalles técnicos y estado del sistema

## 🎮 Uso del Sistema

### Ejecutar el Sistema Operativo Unificado
```bash
python main.py
```

### Opción 3: Módulos Individuales
```bash
# Solo gestión de procesos
python src/listar.py

# Solo sistema de archivos
python src/filesystem.py

# Solo iniciar procesos
python src/iniciar.py

# Solo finalizar procesos
python src/finalizar.py
```

## 🗂️ Estructura del Proyecto

```
Sistema-Operativo-Unificado/
├── main.py                         # 🌟 Aplicación principal del sistema operativo unificado
├── requirements.txt                # Dependencias del proyecto
├── README_UNIFICADO.md            # Esta documentación
├── filesystem_data.json           # Datos del sistema de archivos (auto-generado)
└── src/
    ├── listar.py                  # Gestión y listado de procesos
    ├── info.py                    # Información detallada de procesos
    ├── iniciar.py                 # Iniciar nuevos procesos
    ├── finalizar.py               # Finalizar procesos existentes
    └── filesystem.py              # Sistema de archivos simulado
```

## 🎯 Guía de Uso Rápida

### Gestión de Procesos
1. **Listar todos los procesos**: Opción 1 o 2 del menú principal
2. **Ver información específica**: Opción 3, ingresa el PID del proceso
3. **Iniciar un proceso**: Opción 4, puedes usar comandos como `notepad`, `calc`, etc.
4. **Finalizar un proceso**: Opción 5, ingresa PID o busca por nombre

### Sistema de Archivos
1. **Acceder**: Opción 6 del menú principal
2. **Comandos básicos**:
   - `ls` (listar): Opción 1
   - `cd` (cambiar directorio): Opción 2
   - `mkdir` (crear directorio): Opción 3
   - `touch` (crear archivo): Opción 4
   - `cat` (ver archivo): Opción 5
   - `rm` (eliminar): Opción 6

### Ejemplos Prácticos

#### Crear una estructura de archivos:
```
1. Ir al sistema de archivos (opción 6)
2. Crear directorio "documentos" (opción 3)
3. Cambiar a "documentos" (opción 2)
4. Crear archivo "nota.txt" (opción 4)
5. Ver contenido del directorio (opción 1)
```

#### Monitorear un proceso:
```
1. Listar procesos (opción 2)
2. Encontrar el PID del proceso deseado
3. Ver información detallada (opción 3)
4. Ingresa el PID para ver CPU, memoria, etc.
```

## 🔧 Funcionalidades Avanzadas

### Gestión de Procesos Avanzada
- **Búsqueda inteligente**: Encuentra procesos por nombre parcial
- **Confirmación de seguridad**: Previene eliminación accidental de procesos críticos
- **Manejo de errores**: Gestión robusta de permisos y procesos inexistentes

### Sistema de Archivos Avanzado
- **Persistencia automática**: Los cambios se guardan automáticamente
- **Navegación intuitiva**: Soporte para rutas relativas y absolutas
- **Información detallada**: Permisos, fechas, tamaños, propietarios

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'psutil'"
```bash
pip install psutil
```

### Error: "Permission denied" al finalizar procesos
- Algunos procesos del sistema requieren permisos de administrador
- Ejecuta como administrador o elige procesos de usuario

### El sistema de archivos no guarda cambios
- Verifica permisos de escritura en el directorio
- Asegúrate de que no hay antivirus bloqueando la creación de archivos JSON

### Problemas de codificación en Windows
- Asegúrate de usar una terminal que soporte UTF-8
- Usa PowerShell o Windows Terminal en lugar del CMD tradicional

## 📚 Conceptos Educativos

Este proyecto demuestra conceptos fundamentales de sistemas operativos:

1. **Gestión de Procesos**: Creación, monitoreo y terminación
2. **Sistema de Archivos**: Estructura jerárquica, metadatos, persistencia
3. **Interfaz de Usuario**: Menús interactivos y manejo de entrada
4. **Manejo de Errores**: Validación y recuperación de errores
5. **Modularidad**: Separación de responsabilidades en módulos

## 🤝 Contribuciones

Este es un proyecto educativo. Las mejoras sugeridas incluyen:
- Implementación de permisos de archivos más realistas
- Simulación de memoria virtual
- Planificador de procesos básico
- Interfaz gráfica con tkinter o PyQt

## 📄 Licencia

Proyecto educativo de código abierto. Libre para uso académico y educativo.

## 👨‍💻 Soporte

Para problemas o preguntas:
1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de usar Python 3.7 o superior

---

**¡Disfruta explorando los conceptos de sistemas operativos! 🚀**
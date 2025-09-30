"""
MÓDULO DE INFORMACIÓN DETALLADA DE PROCESOS
==========================================

Este módulo proporciona funcionalidades para obtener información detallada
de procesos específicos del sistema operativo. Permite consultar datos
técnicos y estadísticas de rendimiento de cualquier proceso activo mediante
su PID (Process ID).

Funcionalidades principales:
- Consulta de información detallada por PID
- Estadísticas de rendimiento (CPU y memoria)
- Información de usuario propietario del proceso
- Estado actual del proceso
- Manejo robusto de errores y validaciones

Dependencias:
- psutil: Para acceso a información detallada de procesos del sistema

Casos de uso:
- Diagnóstico de procesos problemáticos
- Monitoreo de rendimiento específico
- Auditoría de procesos del sistema
- Análisis de uso de recursos por proceso

Autor: Sistema Operativo Unificado

"""

import psutil

def info_proceso():
    """
    Obtener y mostrar información detallada de un proceso específico por PID.
    
    Esta función permite al usuario consultar información completa de cualquier
    proceso activo en el sistema mediante su PID (Process ID). Proporciona
    datos técnicos, estadísticas de rendimiento y información del usuario
    propietario del proceso.
    
    Funcionalidades:
    - Solicitud interactiva del PID del proceso
    - Validación de entrada numérica
    - Consulta de información completa del proceso
    - Formato de salida estructurado y legible
    - Manejo robusto de errores y excepciones
    
    Información mostrada:
    - Nombre: Nombre del ejecutable o proceso
    - Estado: Estado actual del proceso (running, sleeping, etc.)
    - Usuario: Nombre del usuario propietario del proceso
    - CPU %: Porcentaje de uso de CPU del proceso
    - Memoria %: Porcentaje de uso de memoria RAM del proceso
    
    Validaciones y manejo de errores:
    - Verificación de existencia del proceso (NoSuchProcess)
    - Validación de entrada numérica (ValueError)
    - Mensajes de error informativos y amigables
    - Acceso seguro a propiedades del proceso
    
    Características técnicas:
    - Medición de CPU con intervalo de 0.1 segundos para precisión
    - Cálculo de porcentaje de memoria con 2 decimales
    - Acceso a metadatos del proceso de forma segura
    - Compatibilidad multiplataforma
    
    Proceso de ejecución:
    1. Solicita al usuario el PID del proceso a consultar
    2. Valida que la entrada sea un número entero válido
    3. Crea objeto Process con el PID especificado
    4. Obtiene y muestra información detallada del proceso
    5. Maneja errores de proceso inexistente o entrada inválida
    
    Examples:
        >>> info_proceso()
        Ingrese el PID del proceso: 1234
        
        === INFORMACIÓN DEL PROCESO ===
        Nombre: chrome.exe
        Estado: running
        Usuario: DESKTOP-ABC\\usuario
        CPU %: 2.5
        Memoria %: 3.45
        
        >>> info_proceso()
        Ingrese el PID del proceso: 99999
        ⚠️  No existe un proceso con ese PID.
        
        >>> info_proceso()
        Ingrese el PID del proceso: abc
        ⚠️  Debe ingresar un número válido.
    
    Raises:
        psutil.NoSuchProcess: Cuando el PID especificado no corresponde a ningún proceso activo
        ValueError: Cuando la entrada no es un número entero válido
        psutil.AccessDenied: Cuando no hay permisos para acceder a la información del proceso
    
    Note:
        - Los porcentajes de CPU pueden variar según la carga del sistema
        - Algunos procesos del sistema pueden requerir permisos administrativos
        - El estado del proceso puede cambiar durante la consulta
        - La precisión de las mediciones depende de la carga del sistema
    """
    try:
        # Solicitar PID del proceso al usuario
        pid = int(input("Ingrese el PID del proceso: "))
        
        # Crear objeto Process con el PID especificado
        p = psutil.Process(pid)
        
        # Mostrar encabezado de información
        print("\n=== INFORMACIÓN DEL PROCESO ===")
        
        # Obtener y mostrar nombre del proceso
        print(f"Nombre: {p.name()}")
        
        # Obtener y mostrar estado actual del proceso
        print(f"Estado: {p.status()}")
        
        # Obtener y mostrar usuario propietario del proceso
        print(f"Usuario: {p.username()}")
        
        # Obtener y mostrar porcentaje de uso de CPU (con intervalo para precisión)
        print(f"CPU %: {p.cpu_percent(interval=0.1)}")
        
        # Obtener y mostrar porcentaje de uso de memoria (con 2 decimales)
        print(f"Memoria %: {p.memory_percent():.2f}")
        
    except psutil.NoSuchProcess:
        # Manejar caso de proceso inexistente
        print("⚠️  No existe un proceso con ese PID.")
    except ValueError:
        # Manejar caso de entrada no numérica
        print("⚠️  Debe ingresar un número válido.")
    except psutil.AccessDenied:
        # Manejar caso de acceso denegado (proceso del sistema)
        print("⚠️  Acceso denegado. El proceso puede requerir permisos administrativos.")
    except Exception as e:
        # Manejar cualquier otro error inesperado
        print(f"⚠️  Error inesperado: {str(e)}")

# Punto de entrada del módulo para pruebas independientes
if __name__ == "__main__":
    info_proceso()

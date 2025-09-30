"""
GESTOR DE PROCESOS DEL SISTEMA OPERATIVO UNIFICADO
==================================================

Este módulo implementa un gestor completo de procesos que permite visualizar,
buscar y monitorear los procesos en ejecución del sistema operativo. Utiliza
la biblioteca psutil para obtener información detallada del sistema.

Funcionalidades principales:
- Listado completo de procesos activos con PID y nombre
- Búsqueda de procesos por nombre con coincidencias parciales
- Estadísticas del sistema (CPU, memoria, número de procesos)
- Interfaz de usuario interactiva con menú de opciones

Dependencias:
- psutil: Para acceso a información de procesos y sistema
- os: Para operaciones del sistema operativo (limpiar pantalla)

Autor: Sistema Operativo Unificado

"""

import psutil
import os

def mostrar_procesos():
    """
    Mostrar todos los procesos en ejecución del sistema.
    
    Esta función obtiene y muestra una lista completa de todos los procesos
    actualmente en ejecución en el sistema, incluyendo su PID (Process ID)
    y nombre. Es útil para obtener una vista general del estado del sistema.
    
    Funcionalidades:
    - Obtiene información de todos los procesos activos
    - Maneja procesos sin nombre de forma segura
    - Formato tabular claro y legible
    - Encabezado visual distintivo
    
    Información mostrada:
    - PID: Identificador único del proceso
    - Nombre: Nombre del ejecutable o proceso
    
    Manejo de errores:
    - Procesos sin nombre se muestran como "<sin nombre>"
    - Acceso seguro a información de procesos
    
    Examples:
        >>> mostrar_procesos()
        ==================================================
          LISTA DE PROCESOS EN EJECUCIÓN   
        ==================================================
        PID:   1234 - Nombre: python.exe
        PID:   5678 - Nombre: notepad.exe
        PID:   9012 - Nombre: chrome.exe
    """
    print("\n" + "="*50)
    print("  LISTA DE PROCESOS EN EJECUCIÓN   ")
    print("="*50)
    
    # Iterar sobre todos los procesos del sistema
    for p in psutil.process_iter(['pid', 'name']):
        # Obtener nombre del proceso de forma segura
        name = p.info.get('name') or "<sin nombre>"
        # Mostrar información formateada
        print(f"PID: {p.info['pid']:>6} - Nombre: {name}")

def buscar_proceso():
    """
    Buscar procesos por nombre usando coincidencias parciales.
    
    Esta función permite al usuario buscar procesos específicos ingresando
    parte del nombre del proceso. Realiza búsquedas case-insensitive y
    muestra todos los procesos que contengan el texto buscado.
    
    Funcionalidades:
    - Búsqueda interactiva con entrada del usuario
    - Coincidencias parciales (substring matching)
    - Búsqueda case-insensitive para mayor flexibilidad
    - Contador de resultados encontrados
    - Formato de salida consistente con mostrar_procesos()
    
    Proceso de búsqueda:
    1. Solicita al usuario el nombre o parte del nombre a buscar
    2. Normaliza la entrada (lowercase, sin espacios extra)
    3. Itera sobre todos los procesos del sistema
    4. Compara nombres usando coincidencia parcial
    5. Muestra resultados y cuenta total de coincidencias
    
    Manejo de errores:
    - Procesos sin nombre se manejan de forma segura
    - Entrada vacía o solo espacios se procesa correctamente
    
    Examples:
        >>> buscar_proceso()
        Ingrese el nombre del proceso a buscar: chrome
        
        Buscando procesos que contengan: 'chrome'
        ----------------------------------------
        PID:   1234 - Nombre: chrome.exe
        PID:   5678 - Nombre: chrome_proxy.exe
        
        Se encontraron 2 procesos
    """
    # Solicitar entrada del usuario
    nombre = input("\nIngrese el nombre del proceso a buscar: ").lower().strip()
    print(f"\nBuscando procesos que contengan: '{nombre}'")
    print("-" * 40)
    
    encontrados = 0
    # Buscar en todos los procesos del sistema
    for p in psutil.process_iter(['pid', 'name']):
        # Obtener nombre del proceso de forma segura y normalizada
        name = (p.info.get('name') or "").lower()
        # Verificar coincidencia parcial
        if nombre in name:
            print(f"PID: {p.info['pid']:>6} - Nombre: {p.info.get('name')}")
            encontrados += 1
    
    # Mostrar resumen de resultados
    print(f"\nSe encontraron {encontrados} procesos")

def mostrar_estadisticas():
    """
    Mostrar estadísticas completas del sistema operativo.
    
    Esta función recopila y presenta información clave sobre el estado
    actual del sistema, incluyendo uso de recursos y número de procesos.
    Es útil para monitoreo del rendimiento y diagnóstico del sistema.
    
    Estadísticas mostradas:
    - Uso de CPU: Porcentaje de utilización del procesador
    - Uso de memoria: Porcentaje de memoria RAM utilizada
    - Total de procesos: Número de procesos actualmente en ejecución
    
    Características técnicas:
    - Medición de CPU con intervalo de 1 segundo para precisión
    - Acceso a información de memoria virtual del sistema
    - Conteo dinámico de procesos activos
    - Formato visual claro con encabezados distintivos
    
    Información técnica:
    - CPU: Utiliza psutil.cpu_percent() con intervalo para medición precisa
    - Memoria: Accede a psutil.virtual_memory() para estadísticas RAM
    - Procesos: Cuenta todos los procesos mediante process_iter()
    
    Examples:
        >>> mostrar_estadisticas()
        ==================================================
        ESTADÍSTICAS DEL SISTEMA
        ==================================================
        Uso de CPU: 15.2%
        Uso de memoria: 67.8%
        Total de procesos ejecutándose: 156
    """
    print("\n" + "="*50)
    print("ESTADÍSTICAS DEL SISTEMA")
    print("="*50)
    
    # Obtener uso de CPU con medición de 1 segundo para precisión
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"Uso de CPU: {cpu_percent}%")
    
    # Obtener información de memoria virtual
    memoria = psutil.virtual_memory()
    print(f"Uso de memoria: {memoria.percent}%")
    
    # Contar número total de procesos activos
    procesos = list(psutil.process_iter(['pid']))
    print(f"Total de procesos ejecutándose: {len(procesos)}")

def ejecutar_gestor():
    """
    Función principal que ejecuta el gestor de procesos interactivo.
    
    Esta función implementa el bucle principal del programa, proporcionando
    una interfaz de usuario basada en menú para acceder a todas las
    funcionalidades del gestor de procesos. Maneja la navegación, entrada
    del usuario y control de flujo del programa.
    
    Características de la interfaz:
    - Menú interactivo con opciones numeradas
    - Limpieza automática de pantalla para mejor experiencia
    - Manejo robusto de entrada del usuario
    - Pausa entre operaciones para revisión de resultados
    - Salida controlada del programa
    
    Opciones del menú:
    1. Mostrar todos los procesos - Lista completa de procesos activos
    2. Buscar proceso por nombre - Búsqueda interactiva de procesos
    3. Mostrar estadísticas del sistema - Información de rendimiento
    4. Salir - Terminar el programa de forma controlada
    
    Manejo de errores:
    - Validación de entrada del usuario
    - Manejo de interrupciones por teclado (Ctrl+C)
    - Mensajes de error informativos para opciones inválidas
    - Limpieza adecuada al salir del programa
    
    Compatibilidad:
    - Limpieza de pantalla multiplataforma (Windows/Linux/Mac)
    - Manejo de diferentes tipos de terminal
    - Codificación de caracteres apropiada
    
    Control de flujo:
    - Bucle infinito hasta que el usuario elija salir
    - Pausa después de cada operación para revisión
    - Limpieza de pantalla antes de mostrar el menú
    
    Examples:
        >>> ejecutar_gestor()
        ==================================================
        GESTOR DE PROCESOS DEL SISTEMA
        ==================================================
        1. Mostrar todos los procesos
        2. Buscar proceso por nombre
        3. Mostrar estadísticas del sistema
        4. Salir
        --------------------------------------------------
        Seleccione una opción (1-4): 1
        
        [Ejecuta la opción seleccionada]
        
        Presione Enter para continuar...
    """
    try:
        while True:
            # Limpiar pantalla para mejor experiencia de usuario
            # Comando multiplataforma: 'cls' para Windows, 'clear' para Unix/Linux/Mac
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Mostrar menú principal con formato visual atractivo
            print("="*50)
            print("GESTOR DE PROCESOS DEL SISTEMA")
            print("="*50)
            print("1. Mostrar todos los procesos")
            print("2. Buscar proceso por nombre")
            print("3. Mostrar estadísticas del sistema ")      
            print("4. Salir")
            print("-"*50)
            
            # Obtener selección del usuario
            opcion = input("Seleccione una opción (1-4): ").strip()
            
            # Procesar la opción seleccionada
            if opcion == "1":
                mostrar_procesos()
            elif opcion == "2":
                buscar_proceso()
            elif opcion == "3":
                mostrar_estadisticas()
            elif opcion == "4":
                print("\n¡Hasta luego!")
                break
            else:
                # Manejar entrada inválida
                print("\nOpción no válida. Por favor, seleccione 1-4.")
            
            # Pausa para que el usuario pueda revisar los resultados
            input("\nPresione Enter para continuar...")
            
    except KeyboardInterrupt:
        # Manejo elegante de interrupción por teclado (Ctrl+C)
        print("\n\nInterrupción por teclado. Saliendo...")

# Punto de entrada del programa
if __name__ == "__main__":
    ejecutar_gestor()

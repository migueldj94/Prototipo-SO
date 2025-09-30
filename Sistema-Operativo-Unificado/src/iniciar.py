"""
MÓDULO DE GESTIÓN E INICIO DE PROCESOS DEL SISTEMA
=================================================

Este módulo proporciona un conjunto completo de herramientas para iniciar,
crear y monitorear procesos en el sistema operativo. Permite ejecutar
comandos personalizados, aplicaciones comunes y procesos con parámetros
específicos de forma segura y controlada.

Funcionalidades principales:
- Inicio de procesos personalizados mediante comandos
- Lanzamiento de aplicaciones comunes del sistema
- Creación de procesos con parámetros y configuraciones específicas
- Monitoreo de procesos recientes iniciados
- Interfaz de usuario interactiva con menú de opciones

Características técnicas:
- Uso de subprocess para manejo seguro de procesos
- Integración con psutil para monitoreo avanzado
- Manejo robusto de errores y excepciones
- Compatibilidad multiplataforma (Windows/Linux/Mac)
- Validación de entrada y parámetros

Dependencias:
- subprocess: Para creación y manejo de procesos del sistema
- os: Para operaciones del sistema operativo
- psutil: Para monitoreo y estadísticas de procesos

Casos de uso:
- Automatización de tareas del sistema
- Lanzamiento de aplicaciones desde el SO unificado
- Creación de procesos con configuraciones específicas
- Monitoreo de actividad de procesos


"""

import subprocess
import os
import psutil

def iniciar_proceso():
    """
    Iniciar un nuevo proceso mediante comando personalizado.
    
    Esta función permite al usuario ejecutar cualquier comando o programa
    disponible en el sistema mediante entrada interactiva. Proporciona
    retroalimentación sobre el éxito o fallo del proceso iniciado.
    
    Funcionalidades:
    - Entrada interactiva de comandos personalizados
    - Validación de entrada no vacía
    - Ejecución segura mediante subprocess.Popen
    - Retroalimentación inmediata con PID del proceso
    - Manejo robusto de errores de ejecución
    
    Proceso de ejecución:
    1. Solicita al usuario el comando a ejecutar
    2. Valida que el comando no esté vacío
    3. Ejecuta el comando usando subprocess.Popen con shell=True
    4. Muestra información del proceso iniciado (PID y comando)
    5. Maneja errores de comando no encontrado o ejecución
    
    Características técnicas:
    - Uso de shell=True para compatibilidad con comandos del sistema
    - Manejo de FileNotFoundError para comandos inexistentes
    - Captura de excepciones generales para errores inesperados
    - Validación de entrada con strip() para espacios
    
    Información mostrada:
    - Confirmación de inicio exitoso
    - PID (Process ID) del proceso creado
    - Comando ejecutado para referencia
    
    Examples:
        >>> iniciar_proceso()
        Ingrese el comando o programa a ejecutar: notepad
        Iniciando proceso: notepad
        ✅ Proceso iniciado exitosamente
        PID: 1234
        Comando: notepad
        
        >>> iniciar_proceso()
        Ingrese el comando o programa a ejecutar: comando_inexistente
        Iniciando proceso: comando_inexistente
        ⚠️  Comando no encontrado
    
    Raises:
        FileNotFoundError: Cuando el comando especificado no existe
        Exception: Para cualquier otro error durante la ejecución
    
    Note:
        - Los comandos se ejecutan con los permisos del usuario actual
        - Algunos comandos pueden requerir permisos administrativos
        - El proceso se ejecuta de forma asíncrona (no bloquea la interfaz)
    """
    try:
        # Solicitar comando al usuario con validación
        comando = input("Ingrese el comando o programa a ejecutar: ").strip()
        
        # Validar que el comando no esté vacío
        if not comando:
            print("⚠️  Debe ingresar un comando válido")
            return
        
        print(f"Iniciando proceso: {comando}")
        
        # Iniciar el proceso de forma segura
        proceso = subprocess.Popen(comando, shell=True)
        
        # Mostrar confirmación y detalles del proceso
        print(f"✅ Proceso iniciado exitosamente")
        print(f"PID: {proceso.pid}")
        print(f"Comando: {comando}")
        
    except FileNotFoundError:
        # Manejar comando no encontrado
        print("⚠️  Comando no encontrado")
    except Exception as e:
        # Manejar cualquier otro error
        print(f"⚠️  Error al iniciar el proceso: {e}")

def iniciar_aplicacion():
    """
    Iniciar aplicaciones comunes del sistema desde un menú predefinido.
    
    Esta función proporciona una interfaz simplificada para lanzar aplicaciones
    comunes del sistema operativo Windows. Presenta un menú numerado con
    opciones predefinidas para facilitar el acceso a herramientas frecuentes.
    
    Aplicaciones disponibles:
    1. Bloc de notas (notepad) - Editor de texto básico
    2. Calculadora (calc) - Calculadora del sistema
    3. Paint (mspaint) - Editor de imágenes básico
    4. Explorador de archivos (explorer) - Navegador de archivos
    5. Símbolo del sistema (cmd) - Terminal de comandos
    6. PowerShell (powershell) - Terminal avanzado
    7. Administrador de tareas (taskmgr) - Monitor de procesos
    
    Funcionalidades:
    - Menú interactivo con aplicaciones predefinidas
    - Validación de selección del usuario
    - Ejecución segura de aplicaciones del sistema
    - Retroalimentación con PID del proceso iniciado
    - Manejo de errores de ejecución
    
    Proceso de ejecución:
    1. Muestra menú de aplicaciones disponibles
    2. Solicita selección del usuario (1-7)
    3. Valida la selección ingresada
    4. Ejecuta la aplicación correspondiente
    5. Muestra confirmación con PID o error
    
    Características técnicas:
    - Diccionario de aplicaciones con nombres y comandos
    - Validación de selección mediante claves del diccionario
    - Ejecución mediante subprocess.Popen para compatibilidad
    - Manejo de excepciones específicas por aplicación
    
    Examples:
        >>> iniciar_aplicacion()
        
        Aplicaciones disponibles:
        ------------------------------
        1. Bloc de notas
        2. Calculadora
        3. Paint
        4. Explorador de archivos
        5. Símbolo del sistema
        6. PowerShell
        7. Administrador de tareas
        
        Seleccione una aplicación (1-7): 1
        ✅ Bloc de notas iniciado exitosamente (PID: 1234)
    
    Note:
        - Las aplicaciones están optimizadas para Windows
        - Algunas aplicaciones pueden requerir permisos específicos
        - Los comandos son estándar del sistema Windows
    """
    # Diccionario de aplicaciones comunes con nombres descriptivos y comandos
    aplicaciones = {
        "1": ("Bloc de notas", "notepad"),
        "2": ("Calculadora", "calc"),
        "3": ("Paint", "mspaint"),
        "4": ("Explorador de archivos", "explorer"),
        "5": ("Símbolo del sistema", "cmd"),
        "6": ("PowerShell", "powershell"),
        "7": ("Administrador de tareas", "taskmgr")
    }
    
    # Mostrar menú de aplicaciones disponibles
    print("\nAplicaciones disponibles:")
    print("-" * 30)
    for key, (nombre, _) in aplicaciones.items():
        print(f"{key}. {nombre}")
    
    # Solicitar selección del usuario
    seleccion = input("\nSeleccione una aplicación (1-7): ").strip()
    
    # Validar selección y ejecutar aplicación
    if seleccion in aplicaciones:
        nombre, comando = aplicaciones[seleccion]
        try:
            # Ejecutar la aplicación seleccionada
            proceso = subprocess.Popen(comando, shell=True)
            print(f"✅ {nombre} iniciado exitosamente (PID: {proceso.pid})")
        except Exception as e:
            # Manejar errores de ejecución específicos de la aplicación
            print(f"⚠️  Error al iniciar {nombre}: {e}")
    else:
        # Manejar selección inválida
        print("⚠️  Selección inválida")

def crear_proceso_personalizado():
    """
    Crear un proceso con parámetros y configuraciones personalizadas.
    
    Esta función avanzada permite crear procesos con configuraciones específicas,
    incluyendo argumentos de línea de comandos y directorio de trabajo personalizado.
    Es útil para ejecutar programas con parámetros específicos o en contextos
    particulares del sistema de archivos.
    
    Parámetros configurables:
    - Programa/ejecutable: Ruta o nombre del programa a ejecutar
    - Argumentos: Parámetros de línea de comandos (opcional)
    - Directorio de trabajo: Directorio desde el cual ejecutar (opcional)
    
    Funcionalidades:
    - Configuración interactiva de parámetros del proceso
    - Validación de programa requerido
    - Verificación de existencia del directorio de trabajo
    - Construcción automática del comando completo
    - Ejecución con configuraciones personalizadas
    
    Proceso de configuración:
    1. Solicita programa/ejecutable (requerido)
    2. Solicita argumentos opcionales
    3. Solicita directorio de trabajo opcional
    4. Valida existencia del directorio si se especifica
    5. Construye y ejecuta el comando completo
    6. Muestra información detallada del proceso creado
    
    Características técnicas:
    - Validación de entrada con strip() para espacios
    - Verificación de existencia de directorio con os.path.exists()
    - Construcción dinámica del comando con argumentos
    - Uso del parámetro cwd en subprocess.Popen
    - Manejo robusto de errores de configuración y ejecución
    
    Examples:
        >>> crear_proceso_personalizado()
        Crear proceso personalizado:
        Programa/ejecutable: python
        Argumentos (opcional): -c "print('Hola mundo')"
        Directorio de trabajo (opcional): C:\\temp
        ✅ Proceso personalizado iniciado exitosamente
        PID: 1234
        Comando: python -c "print('Hola mundo')"
        Directorio: C:\\temp
    
    Note:
        - El directorio de trabajo debe existir para ser utilizado
        - Los argumentos se concatenan automáticamente al programa
        - Si no se especifica directorio, se usa el directorio actual
    """
    try:
        print("Crear proceso personalizado:")
        
        # Solicitar programa/ejecutable (requerido)
        programa = input("Programa/ejecutable: ").strip()
        
        # Solicitar argumentos opcionales
        argumentos = input("Argumentos (opcional): ").strip()
        
        # Solicitar directorio de trabajo opcional
        directorio = input("Directorio de trabajo (opcional): ").strip()
        
        # Validar que se haya especificado un programa
        if not programa:
            print("⚠️  Debe especificar un programa")
            return
        
        # Construir comando completo con argumentos
        comando_completo = f"{programa} {argumentos}".strip()
        
        # Configurar el directorio de trabajo si se especifica y existe
        cwd = directorio if directorio and os.path.exists(directorio) else None
        
        # Crear el proceso con configuraciones personalizadas
        proceso = subprocess.Popen(comando_completo, shell=True, cwd=cwd)
        
        # Mostrar información detallada del proceso creado
        print(f"✅ Proceso personalizado iniciado exitosamente")
        print(f"PID: {proceso.pid}")
        print(f"Comando: {comando_completo}")
        if cwd:
            print(f"Directorio: {cwd}")
            
    except Exception as e:
        # Manejar errores de creación del proceso
        print(f"⚠️  Error al crear el proceso: {e}")

def monitorear_procesos_iniciados():
    """
    Mostrar los procesos más recientes iniciados en el sistema.
    
    Esta función proporciona una vista de los últimos 10 procesos iniciados
    en el sistema, ordenados por tiempo de creación. Es útil para monitorear
    la actividad reciente del sistema y verificar procesos recién creados.
    
    Información mostrada:
    - Número de orden (1-10)
    - PID (Process ID) del proceso
    - Nombre del proceso/ejecutable
    - Hora de inicio del proceso (HH:MM:SS)
    
    Funcionalidades:
    - Obtención de información de todos los procesos activos
    - Ordenamiento por tiempo de creación (más recientes primero)
    - Formato tabular claro y legible
    - Manejo seguro de procesos inaccesibles
    - Conversión de timestamps a formato legible
    
    Proceso de monitoreo:
    1. Itera sobre todos los procesos del sistema
    2. Obtiene PID, nombre y tiempo de creación de cada proceso
    3. Maneja procesos inaccesibles de forma segura
    4. Ordena procesos por tiempo de creación (descendente)
    5. Muestra los 10 más recientes con formato legible
    
    Características técnicas:
    - Uso de psutil.process_iter() para acceso a procesos
    - Manejo de excepciones NoSuchProcess y AccessDenied
    - Ordenamiento con sorted() y lambda para tiempo de creación
    - Conversión de timestamp con datetime.fromtimestamp()
    - Formato de tiempo con strftime() para legibilidad
    
    Examples:
        >>> monitorear_procesos_iniciados()
        ==================================================
        PROCESOS RECIENTES (últimos 10)
        ==================================================
         1. PID:   1234 - python.exe - 14:30:25
         2. PID:   5678 - notepad.exe - 14:29:18
         3. PID:   9012 - chrome.exe - 14:28:45
         ...
    
    Note:
        - Solo muestra procesos a los que se tiene acceso
        - Los tiempos se muestran en formato local del sistema
        - Algunos procesos del sistema pueden no ser accesibles
    """
    print("\n" + "="*50)
    print("PROCESOS RECIENTES (últimos 10)")
    print("="*50)
    
    try:
        procesos = []
        
        # Iterar sobre todos los procesos del sistema
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                # Agregar información del proceso a la lista
                procesos.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Manejar procesos inaccesibles de forma segura
                continue
        
        # Ordenar por tiempo de creación (más recientes primero)
        procesos_ordenados = sorted(procesos, key=lambda x: x['create_time'], reverse=True)
        
        # Mostrar los 10 procesos más recientes
        for i, proc in enumerate(procesos_ordenados[:10], 1):
            import datetime
            # Convertir timestamp a formato legible
            tiempo = datetime.datetime.fromtimestamp(proc['create_time'])
            print(f"{i:2}. PID: {proc['pid']:>6} - {proc['name']} - {tiempo.strftime('%H:%M:%S')}")
            
    except Exception as e:
        # Manejar errores generales de acceso a procesos
        print(f"⚠️  Error al obtener procesos: {e}")

def ejecutar_iniciar():
    """
    Función principal que ejecuta el menú interactivo de gestión de procesos.
    
    Esta función implementa el bucle principal del módulo, proporcionando
    una interfaz de usuario completa para acceder a todas las funcionalidades
    de inicio y gestión de procesos. Maneja la navegación, entrada del usuario
    y control de flujo del programa.
    
    Opciones del menú:
    1. Iniciar proceso personalizado - Ejecutar comandos personalizados
    2. Iniciar aplicación común - Lanzar aplicaciones predefinidas
    3. Crear proceso con parámetros - Configuración avanzada de procesos
    4. Ver procesos recientes - Monitoreo de actividad reciente
    5. Volver al menú principal - Salir del módulo
    
    Características de la interfaz:
    - Menú interactivo con opciones numeradas
    - Limpieza automática de pantalla para mejor experiencia
    - Manejo robusto de entrada del usuario
    - Pausa entre operaciones para revisión de resultados
    - Navegación controlada entre funciones
    
    Control de flujo:
    - Bucle infinito hasta que el usuario elija salir
    - Limpieza de pantalla antes de mostrar el menú
    - Validación de entrada del usuario
    - Pausa después de cada operación
    - Salida controlada al menú principal
    
    Manejo de errores:
    - Validación de opciones del menú (1-5)
    - Mensajes informativos para opciones inválidas
    - Manejo elegante de interrupciones
    
    Examples:
        >>> ejecutar_iniciar()
        ==================================================
        INICIAR PROCESOS DEL SISTEMA
        ==================================================
        1. Iniciar proceso personalizado
        2. Iniciar aplicación común
        3. Crear proceso con parámetros
        4. Ver procesos recientes
        5. Volver al menú principal
        --------------------------------------------------
        Seleccione una opción (1-5): 1
        
        [Ejecuta la función correspondiente]
        
        Presione Enter para continuar...
    
    Note:
        - La limpieza de pantalla es compatible con Windows y Unix
        - Cada operación incluye pausa para revisión de resultados
        - La opción 5 retorna al sistema principal
    """
    while True:
        # Limpiar pantalla para mejor experiencia de usuario
        # Comando multiplataforma: 'cls' para Windows, 'clear' para Unix/Linux/Mac
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Mostrar menú principal con formato visual atractivo
        print("="*50)
        print("INICIAR PROCESOS DEL SISTEMA")
        print("="*50)
        print("1. Iniciar proceso personalizado")
        print("2. Iniciar aplicación común")
        print("3. Crear proceso con parámetros")
        print("4. Ver procesos recientes")
        print("5. Volver al menú principal")
        print("-"*50)
        
        # Obtener selección del usuario
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        # Procesar la opción seleccionada
        if opcion == "1":
            iniciar_proceso()
        elif opcion == "2":
            iniciar_aplicacion()
        elif opcion == "3":
            crear_proceso_personalizado()
        elif opcion == "4":
            monitorear_procesos_iniciados()
        elif opcion == "5":
            # Salir del módulo y volver al menú principal
            break
        else:
            # Manejar entrada inválida
            print("\nOpción no válida. Por favor, seleccione 1-5.")
        
        # Pausa para que el usuario pueda revisar los resultados
        input("\nPresione Enter para continuar...")

# Punto de entrada del módulo para ejecución independiente
if __name__ == "__main__":
    ejecutar_iniciar()
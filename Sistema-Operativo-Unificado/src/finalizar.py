"""
MÓDULO DE FINALIZACIÓN DE PROCESOS
==================================

Este módulo proporciona funcionalidades para terminar procesos del sistema operativo
de manera segura y controlada. Permite finalizar procesos tanto por PID como por nombre,
con confirmaciones de seguridad y manejo robusto de errores.

Funcionalidades principales:
- Terminación de procesos por PID específico
- Terminación de procesos por nombre (con búsqueda)
- Validación de permisos y existencia de procesos
- Confirmaciones de seguridad antes de terminar procesos
- Manejo completo de errores y excepciones

Dependencias:
- psutil: Para gestión y control de procesos del sistema
- os: Para operaciones del sistema operativo (limpiar pantalla)

Autor: Sistema Operativo Unificado
Versión: 1.0
"""

import psutil
import os

def matar_proceso():
    """
    Termina un proceso específico del sistema por su PID.
    
    Esta función solicita al usuario el PID del proceso a terminar,
    verifica su existencia, solicita confirmación y procede con la
    terminación si el usuario confirma la acción.
    
    Funcionalidades:
    - Validación de entrada numérica para PID
    - Verificación de existencia del proceso
    - Obtención del nombre del proceso para confirmación
    - Solicitud de confirmación antes de terminar
    - Terminación segura del proceso
    
    Manejo de errores:
    - ValueError: Para entradas no numéricas
    - psutil.NoSuchProcess: Cuando el proceso no existe
    - psutil.AccessDenied: Cuando no hay permisos suficientes
    - Exception: Para errores inesperados
    
    Ejemplo de uso:
    >>> matar_proceso()
    Ingrese el PID del proceso a terminar: 1234
    ¿Está seguro de terminar el proceso 'notepad.exe' (PID: 1234)? (s/n): s
    ✅ Proceso 'notepad.exe' (PID: 1234) terminado exitosamente
    """
    try:
        # Solicitar PID al usuario con validación
        pid = int(input("Ingrese el PID del proceso a terminar: "))
        
        # Verificar si el proceso existe en el sistema
        if not psutil.pid_exists(pid):
            print(f"⚠️  No existe un proceso con PID {pid}")
            return
        
        # Obtener información del proceso
        proceso = psutil.Process(pid)
        nombre_proceso = proceso.name()
        
        # Solicitar confirmación antes de proceder
        confirmacion = input(f"¿Está seguro de terminar el proceso '{nombre_proceso}' (PID: {pid})? (s/n): ")
        
        # Procesar confirmación y terminar proceso si es afirmativa
        if confirmacion.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            proceso.terminate()
            print(f"✅ Proceso '{nombre_proceso}' (PID: {pid}) terminado exitosamente")
        else:
            print("❌ Operación cancelada")
            
    except psutil.NoSuchProcess:
        print("⚠️  El proceso ya no existe o fue terminado")
    except psutil.AccessDenied:
        print("⚠️  No tiene permisos para terminar este proceso")
    except ValueError:
        print("⚠️  Debe ingresar un número válido")
    except Exception as e:
        print(f"⚠️  Error inesperado: {e}")

def matar_proceso_por_nombre():
    """
    Busca y termina procesos del sistema por su nombre.
    
    Esta función permite buscar procesos por nombre (búsqueda parcial),
    muestra una lista de procesos encontrados, permite al usuario
    seleccionar cuál terminar y procede con la terminación.
    
    Funcionalidades:
    - Búsqueda de procesos por nombre (insensible a mayúsculas)
    - Listado de procesos encontrados con PID y nombre
    - Selección interactiva del proceso a terminar
    - Opción de cancelar la operación
    - Terminación segura del proceso seleccionado
    
    Algoritmo de búsqueda:
    1. Itera sobre todos los procesos del sistema
    2. Compara el nombre ingresado con el nombre del proceso (parcial)
    3. Recopila todos los procesos que coinciden
    4. Presenta lista numerada para selección
    
    Manejo de errores:
    - Validación de entrada vacía
    - psutil.NoSuchProcess: Para procesos que desaparecen durante la búsqueda
    - psutil.AccessDenied: Para procesos sin permisos de acceso
    - ValueError: Para selecciones no numéricas
    - Exception: Para errores inesperados
    
    Ejemplo de uso:
    >>> matar_proceso_por_nombre()
    Ingrese el nombre del proceso a terminar: notepad
    
    Se encontraron 2 procesos:
    1. PID: 1234 - Nombre: notepad.exe
    2. PID: 5678 - Nombre: notepad++.exe
    
    Ingrese el número del proceso a terminar (0 para cancelar): 1
    ✅ Proceso 'notepad.exe' (PID: 1234) terminado exitosamente
    """
    try:
        # Solicitar nombre del proceso con validación
        nombre = input("Ingrese el nombre del proceso a terminar: ").strip()
        
        if not nombre:
            print("⚠️  Debe ingresar un nombre válido")
            return
        
        procesos_encontrados = []
        
        # Buscar procesos que coincidan con el nombre (búsqueda parcial)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if nombre.lower() in proc.info['name'].lower():
                    procesos_encontrados.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Continuar si el proceso desaparece o no hay permisos
                continue
        
        # Verificar si se encontraron procesos
        if not procesos_encontrados:
            print(f"⚠️  No se encontraron procesos con el nombre '{nombre}'")
            return
        
        # Mostrar lista de procesos encontrados
        print(f"\nSe encontraron {len(procesos_encontrados)} procesos:")
        for i, proc in enumerate(procesos_encontrados, 1):
            print(f"{i}. PID: {proc.info['pid']} - Nombre: {proc.info['name']}")
        
        # Solicitar selección del proceso a terminar
        seleccion = input("\nIngrese el número del proceso a terminar (0 para cancelar): ")
        
        try:
            indice = int(seleccion) - 1
            if indice == -1:
                print("❌ Operación cancelada")
                return
            elif 0 <= indice < len(procesos_encontrados):
                # Terminar el proceso seleccionado
                proceso = procesos_encontrados[indice]
                proceso.terminate()
                print(f"✅ Proceso '{proceso.info['name']}' (PID: {proceso.info['pid']}) terminado exitosamente")
            else:
                print("⚠️  Selección inválida")
        except ValueError:
            print("⚠️  Debe ingresar un número válido")
            
    except Exception as e:
        print(f"⚠️  Error inesperado: {e}")

def ejecutar_finalizar():
    """
    Menú principal para la gestión de finalización de procesos.
    
    Esta función presenta un menú interactivo que permite al usuario
    elegir entre diferentes métodos de terminación de procesos:
    - Por PID específico
    - Por nombre del proceso
    - Regresar al menú principal
    
    Características del menú:
    - Interfaz clara y organizada
    - Limpieza de pantalla entre operaciones
    - Bucle continuo hasta que el usuario elija salir
    - Validación de opciones ingresadas
    - Pausa después de cada operación para revisar resultados
    
    Estructura del menú:
    1. Terminar proceso por PID - Llama a matar_proceso()
    2. Terminar proceso por nombre - Llama a matar_proceso_por_nombre()
    3. Volver al menú principal - Sale del bucle
    
    Flujo de ejecución:
    1. Limpiar pantalla
    2. Mostrar opciones del menú
    3. Procesar selección del usuario
    4. Ejecutar función correspondiente
    5. Pausar para mostrar resultados
    6. Repetir hasta que el usuario elija salir
    
    Ejemplo de uso:
    >>> ejecutar_finalizar()
    ==================================================
    FINALIZAR PROCESOS DEL SISTEMA
    ==================================================
    1. Terminar proceso por PID
    2. Terminar proceso por nombre
    3. Volver al menú principal
    --------------------------------------------------
    Seleccione una opción (1-3): 1
    """
    while True:
        # Limpiar pantalla para mejor presentación
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Mostrar encabezado del menú
        print("="*50)
        print("FINALIZAR PROCESOS DEL SISTEMA")
        print("="*50)
        print("1. Terminar proceso por PID")
        print("2. Terminar proceso por nombre")
        print("3. Volver al menú principal")
        print("-"*50)
        
        # Solicitar y procesar opción del usuario
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            matar_proceso()
        elif opcion == "2":
            matar_proceso_por_nombre()
        elif opcion == "3":
            break  # Salir del bucle y regresar al menú principal
        else:
            print("\nOpción no válida. Por favor, seleccione 1-3.")
        
        # Pausa para permitir al usuario revisar los resultados
        input("\nPresione Enter para continuar...")

# Punto de entrada del módulo cuando se ejecuta directamente
if __name__ == "__main__":
    ejecutar_finalizar()
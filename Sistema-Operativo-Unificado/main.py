
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA OPERATIVO UNIFICADO - PROTOTIPO EDUCATIVO
==================================================

Este es un prototipo educativo de un sistema operativo que integra múltiples 
funcionalidades básicas de administración del sistema en una sola aplicación.

FUNCIONALIDADES PRINCIPALES:
---------------------------
🔧 GESTIÓN DE PROCESOS:
   - Listar todos los procesos del sistema con información detallada
   - Obtener información específica de un proceso por PID
   - Iniciar nuevos procesos y aplicaciones
   - Finalizar procesos existentes de forma segura

📁 SISTEMA DE ARCHIVOS SIMULADO:
   - Crear y eliminar archivos y directorios virtuales
   - Navegar por la estructura de directorios simulada
   - Visualizar contenido de archivos
   - Comandos de terminal avanzados (tree, pwd, find)

📊 MONITOREO DEL SISTEMA:
   - Estadísticas en tiempo real de CPU y memoria
   - Búsqueda de procesos por nombre
   - Información detallada del sistema

⚙️ UTILIDADES:
   - Información completa del sistema operativo unificado
   - Limpieza de pantalla
   - Gestión de sesión con tiempo de ejecución

ARQUITECTURA:
------------
El sistema está dividido en módulos especializados ubicados en la carpeta 'src/':
- listar.py: Gestión y listado de procesos
- info.py: Información detallada de procesos
- finalizar.py: Terminación segura de procesos
- iniciar.py: Inicio de nuevos procesos
- filesystem.py: Sistema de archivos simulado completo

DEPENDENCIAS:
------------
- psutil: Para gestión avanzada de procesos del sistema
- json: Para persistencia de datos del sistema de archivos
- datetime: Para manejo de fechas y tiempos
- subprocess: Para ejecución de procesos externos

"""

# ============================================================================
# IMPORTACIONES DE LIBRERÍAS ESTÁNDAR
# ============================================================================
import os          # Operaciones del sistema operativo (limpiar pantalla, etc.)
import sys         # Información del sistema Python y plataforma
import datetime    # Manejo de fechas y tiempos para sesión y logs
from pathlib import Path  # Manejo moderno de rutas de archivos

# ============================================================================
# IMPORTACIONES DE MÓDULOS PROPIOS
# ============================================================================
# Módulo de gestión de procesos - funciones para listar y administrar procesos
from src.listar import ejecutar_gestor, mostrar_procesos, buscar_proceso, mostrar_estadisticas

# Módulo de información de procesos - obtener detalles específicos de un proceso
from src.info import info_proceso

# Módulo de finalización de procesos - terminar procesos de forma segura
from src.finalizar import ejecutar_finalizar, matar_proceso

# Módulo de inicio de procesos - crear y ejecutar nuevos procesos
from src.iniciar import ejecutar_iniciar, iniciar_proceso

# Módulo del sistema de archivos simulado - funcionalidad completa de archivos virtuales
from src.filesystem import ejecutar_filesystem

# ============================================================================
# CLASE PRINCIPAL DEL SISTEMA OPERATIVO UNIFICADO
# ============================================================================

class SistemaOperativoUnificado:
    """
    Clase principal que maneja todo el sistema operativo unificado.
    
    Esta clase actúa como el núcleo del sistema, coordinando todas las 
    funcionalidades y módulos disponibles. Gestiona la interfaz de usuario,
    el flujo de navegación entre módulos y mantiene el estado de la sesión.
    
    Atributos:
        version (str): Versión actual del sistema
        nombre (str): Nombre completo del sistema
        fecha_inicio (datetime): Momento en que se inició la sesión actual
    
    Métodos principales:
        - mostrar_banner(): Muestra el banner de bienvenida
        - mostrar_menu_principal(): Presenta el menú de opciones
        - ejecutar_opcion(): Procesa la selección del usuario
        - ejecutar(): Bucle principal del sistema
    """
    
    def __init__(self):
        """
        Inicializar el sistema operativo unificado.
        
        Establece los valores básicos del sistema como versión, nombre
        y registra el momento de inicio de la sesión para estadísticas.
        """
        self.version = "1.0"                                    # Versión del sistema
        self.nombre = "Sistema Operativo Unificado"             # Nombre del sistema
        self.fecha_inicio = datetime.datetime.now()             # Timestamp de inicio de sesión
    
    def mostrar_banner(self):
        """
        Mostrar el banner principal del sistema con información básica.
        
        Limpia la pantalla y muestra un banner decorativo con:
        - Nombre del sistema
        - Versión y tipo (prototipo educativo)
        - Fecha y hora de inicio de sesión
        
        El banner utiliza caracteres Unicode para crear un diseño atractivo.
        """
        # Limpiar pantalla según el sistema operativo
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Crear banner decorativo con información del sistema
        print("╔" + "="*70 + "╗")
        print("║" + f"{self.nombre:^70}" + "║")
        print("║" + f"Versión {self.version} - Prototipo Educativo{'':<32}" + "║")
        print("║" + f"Iniciado: {self.fecha_inicio.strftime('%d/%m/%Y %H:%M:%S')}{'':<32}" + "║")
        print("╚" + "="*70 + "╝")
        print()  # Línea en blanco para separación
    
    def mostrar_menu_principal(self):
        """
        Mostrar el menú principal del sistema con todas las opciones disponibles.
        
        Presenta un menú organizado por categorías que incluye:
        - 🔧 GESTIÓN DE PROCESOS: Opciones 1-5 para administrar procesos
        - 📁 SISTEMA DE ARCHIVOS: Opción 6 para el simulador de archivos
        - 📊 MONITOREO DEL SISTEMA: Opciones 7-8 para estadísticas y búsqueda
        - ⚙️ UTILIDADES: Opciones 9-10 para información y limpieza
        - Opción 0 para salir del sistema
        
        El menú utiliza caracteres Unicode para crear un diseño visual atractivo
        y organizado que facilita la navegación del usuario.
        """
        print("┌─────────────────────────────────────────────────────────────────────┐")
        print("│                        MENÚ PRINCIPAL                               │")
        print("├─────────────────────────────────────────────────────────────────────┤")
        
        # Sección de Gestión de Procesos
        print("│  🔧 GESTIÓN DE PROCESOS                                            │")
        print("│     1. Gestor Completo de Procesos                                 │")
        print("│     2. Listar Procesos Rápido                                      │")
        print("│     3. Información de Proceso                                       │")
        print("│     4. Iniciar Proceso                                              │")
        print("│     5. Finalizar Proceso                                            │")
        print("│                                                                     │")
        
        # Sección de Sistema de Archivos
        print("│  📁 SISTEMA DE ARCHIVOS                                            │")
        print("│     6. Sistema de Archivos Simulado                                │")
        print("│                                                                     │")
        
        # Sección de Monitoreo del Sistema
        print("│  📊 MONITOREO DEL SISTEMA                                          │")
        print("│     7. Estadísticas del Sistema                                     │")
        print("│     8. Buscar Proceso por Nombre                                    │")
        print("│                                                                     │")
        
        # Sección de Utilidades
        print("│  ⚙️  UTILIDADES                                                     │")
        print("│     9. Información del Sistema                                      │")
        print("│    10. Limpiar Pantalla                                             │")
        print("│                                                                     │")
        
        # Opción de salida
        print("│     0. Salir del Sistema                                            │")
        print("└─────────────────────────────────────────────────────────────────────┘")
    
    def mostrar_info_sistema(self):
        """Mostrar información del sistema operativo unificado"""
        print("\n" + "="*60)
        print("INFORMACIÓN DEL SISTEMA OPERATIVO UNIFICADO")
        print("="*60)
        
        # Información básica
        print(f"Nombre: {self.nombre}")
        print(f"Versión: {self.version}")
        print(f"Fecha de inicio: {self.fecha_inicio.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Tiempo de ejecución
        tiempo_ejecucion = datetime.datetime.now() - self.fecha_inicio
        horas, remainder = divmod(tiempo_ejecucion.seconds, 3600)
        minutos, segundos = divmod(remainder, 60)
        print(f"Tiempo de ejecución: {horas:02d}:{minutos:02d}:{segundos:02d}")
        
        # Módulos disponibles
        print("\nMódulos disponibles:")
        print("  ✅ Gestión de Procesos")
        print("     - Listar procesos del sistema")
        print("     - Obtener información detallada")
        print("     - Iniciar nuevos procesos")
        print("     - Finalizar procesos existentes")
        print("  ✅ Sistema de Archivos Simulado")
        print("     - Crear/eliminar archivos y directorios")
        print("     - Navegación por directorios")
        print("     - Visualización de contenido")
        print("  ✅ Monitoreo del Sistema")
        print("     - Estadísticas de CPU y memoria")
        print("     - Búsqueda de procesos")
        print("     - Información del sistema")
        
        # Información técnica
        print(f"\nPlataforma: {sys.platform}")
        print(f"Versión de Python: {sys.version.split()[0]}")
        print(f"Directorio de trabajo: {os.getcwd()}")
        
        # Dependencias
        print("\nDependencias requeridas:")
        print("  - psutil (gestión de procesos)")
        print("  - json (persistencia de datos)")
        print("  - datetime (manejo de fechas)")
        print("  - subprocess (ejecución de procesos)")
    
    def limpiar_pantalla(self):
        """Limpiar la pantalla del sistema"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("✅ Pantalla limpiada exitosamente")
    
    def mostrar_despedida(self):
        """Mostrar mensaje de despedida"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        tiempo_total = datetime.datetime.now() - self.fecha_inicio
        horas, remainder = divmod(tiempo_total.seconds, 3600)
        minutos, segundos = divmod(remainder, 60)
        
        print("╔" + "="*70 + "╗")
        print("║" + "GRACIAS POR USAR EL SISTEMA OPERATIVO UNIFICADO".center(70) + "║")
        print("║" + " "*70 + "║")
        print("║" + f"Tiempo total de sesión: {horas:02d}:{minutos:02d}:{segundos:02d}".center(70) + "║")
        print("║" + f"Desarrollado con fines educativos".center(70) + "║")
        print("║" + " "*70 + "║")
        print("║" + "¡Hasta la próxima! 👋".center(70) + "║")
        print("╚" + "="*70 + "╝")
    
    def ejecutar(self):
        """
        Método principal que ejecuta el bucle del sistema operativo unificado.
        
        Este método implementa el bucle principal del sistema que:
        1. Muestra el banner de bienvenida al inicio
        2. Presenta el menú principal de opciones
        3. Captura y procesa la entrada del usuario
        4. Ejecuta la funcionalidad correspondiente según la opción seleccionada
        5. Maneja errores de entrada inválida con mensajes informativos
        6. Continúa ejecutándose hasta que el usuario seleccione salir (opción 0)
        
        El sistema incluye manejo de excepciones para:
        - Valores no numéricos (ValueError)
        - Interrupciones del teclado (KeyboardInterrupt - Ctrl+C)
        - Errores inesperados del sistema
        
        Funcionalidades disponibles:
        - Gestión completa de procesos (opciones 1-5)
        - Sistema de archivos simulado (opción 6)
        - Monitoreo del sistema (opciones 7-8)
        - Utilidades del sistema (opciones 9-10)
        """
        # Mostrar banner de bienvenida al iniciar el sistema
        self.mostrar_banner()
        
        while True:
            try:
                # Mostrar el menú principal con todas las opciones
                self.mostrar_menu_principal()
                
                # Capturar la opción seleccionada por el usuario
                opcion = input("\n🔹 Seleccione una opción: ").strip()
                
                # Procesar la opción seleccionada
                if opcion == "0":
                    # Opción de salida del sistema
                    print("\n" + "="*70)
                    print("🔴 CERRANDO SISTEMA OPERATIVO UNIFICADO")
                    print("   ¡Gracias por usar nuestro sistema!")
                    print("="*70)
                    break
                    
                elif opcion == "1":
                    # Gestor completo de procesos con interfaz avanzada
                    print("\n🔧 Iniciando Gestor Completo de Procesos...")
                    from src.listar import ejecutar_gestor
                    ejecutar_gestor()
                    
                elif opcion == "2":
                    # Listado rápido de procesos activos
                    print("\n📋 Listando procesos activos...")
                    from src.listar import mostrar_procesos
                    mostrar_procesos()
                    
                elif opcion == "3":
                    # Información detallada de un proceso específico
                    print("\n🔍 Consultando información de proceso...")
                    from src.info import info_proceso
                    info_proceso()
                    
                elif opcion == "4":
                    # Iniciar un nuevo proceso en el sistema
                    print("\n🚀 Iniciando nuevo proceso...")
                    from src.iniciar import ejecutar_iniciar
                    ejecutar_iniciar()
                    
                elif opcion == "5":
                    # Finalizar un proceso existente
                    print("\n🛑 Finalizando proceso...")
                    from src.finalizar import ejecutar_finalizar
                    ejecutar_finalizar()
                    
                elif opcion == "6":
                    # Sistema de archivos simulado con terminal avanzada
                    print("\n📁 Accediendo al Sistema de Archivos Simulado...")
                    from src.filesystem import ejecutar_filesystem
                    ejecutar_filesystem()
                    
                elif opcion == "7":
                    # Estadísticas completas del sistema
                    print("\n📊 Generando estadísticas del sistema...")
                    from src.listar import mostrar_estadisticas
                    mostrar_estadisticas()
                    
                elif opcion == "8":
                    # Búsqueda de procesos por nombre
                    print("\n🔎 Buscando proceso por nombre...")
                    from src.listar import buscar_proceso
                    buscar_proceso()
                    
                elif opcion == "9":
                    # Información general del sistema operativo
                    print("\n💻 Mostrando información del sistema...")
                    self.mostrar_info_sistema()
                    
                elif opcion == "10":
                    # Limpiar la pantalla de la consola
                    print("\n🧹 Limpiando pantalla...")
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    
                else:
                    # Manejo de opciones inválidas
                    print("\n❌ OPCIÓN INVÁLIDA")
                    print("   Por favor, seleccione un número del 0 al 10")
                    
                # Pausa para que el usuario pueda leer los resultados
                if opcion != "0" and opcion != "10":
                    input("\n⏸️  Presione Enter para continuar...")
                    
            except ValueError:
                # Error cuando se ingresa un valor no numérico
                print("\n❌ ERROR: Debe ingresar un número válido")
                input("⏸️  Presione Enter para continuar...")
                
            except KeyboardInterrupt:
                # Manejo de interrupción por teclado (Ctrl+C)
                print("\n\n🔴 INTERRUPCIÓN DETECTADA")
                print("   Cerrando sistema de forma segura...")
                break
                
            except Exception as e:
                # Manejo de errores inesperados del sistema
                print(f"\n❌ ERROR INESPERADO: {str(e)}")
                print("   El sistema continuará funcionando...")
                input("⏸️  Presione Enter para continuar...")

def verificar_dependencias():
    """
    Verificar que todas las dependencias necesarias estén instaladas.
    
    Esta función comprueba la disponibilidad de las librerías externas
    requeridas para el funcionamiento del sistema operativo unificado:
    
    - psutil: Librería para obtener información de procesos y sistema
    - pathlib: Librería para manejo de rutas (incluida en Python 3.4+)
    
    Returns:
        bool: True si todas las dependencias están disponibles, False en caso contrario
        
    Raises:
        ImportError: Si alguna dependencia crítica no está instalada
        
    La función proporciona mensajes informativos sobre el estado de cada
    dependencia y sugerencias de instalación en caso de faltar alguna.
    """
    try:
        # Verificar psutil - librería crítica para gestión de procesos
        import psutil
        print("✅ psutil: Disponible")
        
        # Verificar pathlib - incluida en Python 3.4+
        import pathlib
        print("✅ pathlib: Disponible")
        
        print("🎉 Todas las dependencias están correctamente instaladas")
        return True
        
    except ImportError as e:
        # Manejo de dependencias faltantes
        print(f"❌ Error de dependencia: {e}")
        print("\n📦 Para instalar las dependencias faltantes, ejecute:")
        print("   pip install -r requirements.txt")
        print("\n   O instale manualmente:")
        print("   pip install psutil")
        return False


def main():
    """
    Función principal del sistema operativo unificado.
    
    Esta función es el punto de entrada principal del programa que:
    1. Verifica que todas las dependencias estén instaladas
    2. Crea una instancia del sistema operativo unificado
    3. Inicia la ejecución del sistema
    4. Maneja errores críticos de inicialización
    
    El sistema solo se ejecutará si todas las dependencias están disponibles.
    En caso de faltar alguna dependencia, se mostrará un mensaje informativo
    con instrucciones para la instalación.
    
    Funcionalidades del sistema:
    - Gestión completa de procesos del sistema
    - Sistema de archivos simulado con comandos de terminal
    - Monitoreo en tiempo real del sistema
    - Utilidades de información y mantenimiento
    """
    try:
        # Verificar dependencias antes de iniciar el sistema
        print("🔍 Verificando dependencias del sistema...")
        if not verificar_dependencias():
            print("\n❌ No se puede iniciar el sistema sin las dependencias requeridas")
            return
        
        print("\n" + "="*70)
        print("🚀 INICIANDO SISTEMA OPERATIVO UNIFICADO")
        print("="*70)
        
        # Crear e iniciar el sistema operativo unificado
        sistema = SistemaOperativoUnificado()
        sistema.ejecutar()
        
    except KeyboardInterrupt:
        # Manejo de interrupción durante la inicialización
        print("\n\n⚠️  Inicialización interrumpida por el usuario")
        print("   Sistema cerrado de forma segura")
        
    except Exception as e:
        # Manejo de errores críticos durante la inicialización
        print(f"\n❌ ERROR CRÍTICO DE INICIALIZACIÓN: {str(e)}")
        print("   No se pudo iniciar el sistema operativo unificado")
        print("   Verifique la instalación y las dependencias")


# Punto de entrada del programa
if __name__ == "__main__":
    # Ejecutar la función principal cuando el script se ejecute directamente
    main()
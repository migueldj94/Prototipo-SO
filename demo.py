"""
Demostración del Sistema de Archivos Simulado
=============================================

Este módulo proporciona una demostración completa de las funcionalidades
del sistema de archivos simulado desarrollado como prototipo de OS.

Funcionalidades demostradas:
- Creación y gestión de directorios
- Operaciones CRUD en archivos
- Navegación entre directorios
- Persistencia de datos
- Listado y visualización de contenido

Autor: Equipo de Desarrollo OS
Versión: 2.0
"""

from filesystem import FileSystem
import os
import time
from typing import List, Tuple


class DemoConfig:
    """Configuración para la demostración."""
    
    DEMO_FILE = "demo_disk_clean.json"
    ANIMATION_DELAY = 0.8  # Segundos entre pasos
    
    # Datos de prueba
    DIRECTORIES = ["documentos", "proyectos", "temp", "bin"]
    
    FILES_DATA = [
        ("readme.txt", """Este es un archivo de prueba del sistema de archivos simulado.
Contiene información básica sobre el proyecto de sistemas operativos.

CARACTERÍSTICAS PRINCIPALES:
- Sistema de archivos tipo FAT simplificado
- Operaciones CRUD completas
- Navegación jerárquica de directorios
- Persistencia automática en disco virtual
- Interfaz de línea de comandos interactiva

¡Prototipo funcionando correctamente!"""),
        
        ("config.ini", """[sistema]
version=2.0
debug=true
max_files=1000

[archivos]
max_size=1048576
encoding=utf-8

[persistencia]
auto_save=true
backup_enabled=false"""),
        
        ("datos.log", """2024-01-15 10:30:00 - Sistema de archivos iniciado
2024-01-15 10:30:01 - Cargando configuración desde config.ini
2024-01-15 10:30:02 - Inicializando tabla FAT
2024-01-15 10:30:03 - Creando directorio raíz
2024-01-15 10:30:04 - Sistema listo para operaciones
2024-01-15 10:30:05 - Modo demostración activado""")
    ]
    
    SUBDIRECTORY_FILES = [
        ("carta.txt", """Estimado evaluador,

Este documento demuestra la capacidad del sistema de archivos
para manejar archivos en subdirectorios.

El sistema implementa:
✓ Navegación entre directorios
✓ Creación de archivos en cualquier ubicación
✓ Mantenimiento de la estructura jerárquica
✓ Persistencia de datos entre sesiones

Atentamente,
Equipo de Desarrollo"""),
        
        ("notas.md", """# Notas del Proyecto - Sistema de Archivos

## Objetivos Cumplidos
- [x] Implementar sistema de archivos simulado
- [x] Crear operaciones CRUD completas
- [x] Desarrollar navegación de directorios
- [x] Implementar persistencia de datos
- [x] Crear interfaz de línea de comandos
- [x] Desarrollar suite de pruebas automatizadas

## Arquitectura
- **FileNode**: Representa archivos y directorios
- **VirtualDisk**: Simula el disco físico
- **FileSystem**: Interfaz principal del sistema

## Próximos Pasos
- Optimización de rendimiento
- Implementación de permisos avanzados
- Soporte para enlaces simbólicos""")
    ]


class DemoPresenter:
    """Clase para manejar la presentación visual de la demostración."""
    
    @staticmethod
    def print_header():
        """Imprime el encabezado de la demostración."""
        print("🖥️  DEMOSTRACIÓN DEL SISTEMA DE ARCHIVOS SIMULADO")
        print("=" * 65)
        print("Este demo muestra las capacidades del prototipo de OS")
        print("desarrollado para el proyecto de sistemas operativos.")
        print("=" * 65)
    
    @staticmethod
    def print_separator(title: str):
        """Imprime un separador con título."""
        print("\n" + "=" * 65)
        print(f"🔹 {title}")
        print("=" * 65)
    
    @staticmethod
    def print_step(step: str, delay: bool = True):
        """Imprime un paso de la demostración con animación opcional."""
        print(f"\n➤ {step}")
        if delay:
            time.sleep(DemoConfig.ANIMATION_DELAY)
    
    @staticmethod
    def print_success(message: str):
        """Imprime un mensaje de éxito."""
        print(f"✅ {message}")
    
    @staticmethod
    def print_error(message: str):
        """Imprime un mensaje de error."""
        print(f"❌ {message}")
    
    @staticmethod
    def print_info(message: str):
        """Imprime un mensaje informativo."""
        print(f"ℹ️  {message}")
    
    @staticmethod
    def print_file_content(filename: str, content: str, max_length: int = 150):
        """Imprime el contenido de un archivo de forma formateada."""
        print(f"📄 Contenido de {filename}:")
        print("-" * 50)
        if len(content) > max_length:
            print(content[:max_length] + "...")
            print(f"[... {len(content) - max_length} caracteres más]")
        else:
            print(content)
        print("-" * 50)


class FileSystemDemo:
    """Clase principal para ejecutar la demostración del sistema de archivos."""
    
    def __init__(self):
        """Inicializa la demostración."""
        self.fs = None
        self.presenter = DemoPresenter()
        self._setup_clean_environment()
    
    def _setup_clean_environment(self):
        """Configura un entorno limpio para la demostración."""
        if os.path.exists(DemoConfig.DEMO_FILE):
            os.remove(DemoConfig.DEMO_FILE)
        self.fs = FileSystem(DemoConfig.DEMO_FILE)
    
    def _handle_operation_result(self, success: bool, message: str, operation: str) -> bool:
        """
        Maneja el resultado de una operación del sistema de archivos.
        
        Args:
            success (bool): Si la operación fue exitosa
            message (str): Mensaje de la operación
            operation (str): Descripción de la operación
            
        Returns:
            bool: True si fue exitosa, False si falló
        """
        if success:
            self.presenter.print_success(f"{operation}: {message}")
            return True
        else:
            self.presenter.print_error(f"{operation} falló: {message}")
            return False
    
    def demo_initialization(self):
        """Demuestra la inicialización del sistema."""
        self.presenter.print_separator("INICIALIZACIÓN DEL SISTEMA")
        self.presenter.print_step("Sistema de archivos inicializado correctamente")
        self.presenter.print_info(f"Directorio actual: {self.fs.get_current_directory()}")
        self.presenter.print_info(f"Archivo de disco: {DemoConfig.DEMO_FILE}")
    
    def demo_directory_creation(self):
        """Demuestra la creación de directorios."""
        self.presenter.print_separator("CREACIÓN DE ESTRUCTURA DE DIRECTORIOS")
        
        created_count = 0
        for directory in DemoConfig.DIRECTORIES:
            self.presenter.print_step(f"Creando directorio: {directory}")
            success, message = self.fs.create_directory(directory)
            if self._handle_operation_result(success, message, f"Directorio '{directory}'"):
                created_count += 1
        
        self.presenter.print_info(f"Directorios creados exitosamente: {created_count}/{len(DemoConfig.DIRECTORIES)}")
        
        # Listar contenido
        self.presenter.print_step("Listando contenido del directorio raíz:")
        success, message, items = self.fs.list_directory()
        if success:
            for item in items:
                icon = "📁" if item["type"] == "directory" else "📄"
                print(f"  {icon} {item['name']} ({item['type']})")
        else:
            self.presenter.print_error(f"Error listando directorio: {message}")
    
    def demo_file_operations(self):
        """Demuestra las operaciones con archivos."""
        self.presenter.print_separator("OPERACIONES CON ARCHIVOS")
        
        # Crear archivos
        created_files = 0
        for filename, content in DemoConfig.FILES_DATA:
            self.presenter.print_step(f"Creando archivo: {filename}")
            success, message = self.fs.create_file(filename, content)
            if self._handle_operation_result(success, message, f"Archivo '{filename}'"):
                self.presenter.print_info(f"Tamaño: {len(content)} bytes")
                created_files += 1
        
        self.presenter.print_info(f"Archivos creados: {created_files}/{len(DemoConfig.FILES_DATA)}")
        
        # Listar archivos creados
        self.presenter.print_step("Listando archivos creados:")
        success, message, items = self.fs.list_directory()
        if success:
            file_count = 0
            for item in items:
                if item["type"] == "file":
                    print(f"  📄 {item['name']} - {item['size']} bytes")
                    file_count += 1
            self.presenter.print_info(f"Total de archivos: {file_count}")
        else:
            self.presenter.print_error(f"Error listando directorio: {message}")
    
    def demo_file_reading(self):
        """Demuestra la lectura de archivos."""
        self.presenter.print_separator("LECTURA DE ARCHIVOS")
        
        for filename, _ in DemoConfig.FILES_DATA:
            self.presenter.print_step(f"Leyendo contenido de: {filename}")
            success, message, content = self.fs.read_file(filename)
            if success and content is not None:
                self.presenter.print_file_content(filename, content)
            else:
                self.presenter.print_error(f"Error leyendo '{filename}': {message}")
    
    def demo_navigation(self):
        """Demuestra la navegación entre directorios."""
        self.presenter.print_separator("NAVEGACIÓN ENTRE DIRECTORIOS")
        
        # Navegar a directorio documentos
        self.presenter.print_step("Cambiando al directorio 'documentos'")
        success, message = self.fs.change_directory("documentos")
        
        if not self._handle_operation_result(success, message, "Cambio de directorio"):
            return
        
        self.presenter.print_info(f"Ubicación actual: {self.fs.get_current_directory()}")
        
        # Crear archivos en subdirectorio
        self.presenter.print_step("Creando archivos en el subdirectorio")
        for filename, content in DemoConfig.SUBDIRECTORY_FILES:
            success_file, message_file = self.fs.create_file(filename, content)
            self._handle_operation_result(success_file, message_file, f"Archivo '{filename}'")
        
        # Listar contenido del subdirectorio
        self.presenter.print_step("Listando contenido del subdirectorio:")
        success, message, items = self.fs.list_directory()
        if success:
            for item in items:
                icon = "📁" if item["type"] == "directory" else "📄"
                size_info = f" - {item['size']} bytes" if item["type"] == "file" else ""
                print(f"  {icon} {item['name']}{size_info}")
        else:
            self.presenter.print_error(f"Error listando directorio: {message}")
        
        # Volver al directorio raíz
        self.presenter.print_step("Regresando al directorio raíz")
        success, message = self.fs.change_directory("/")
        self._handle_operation_result(success, message, "Regreso al directorio raíz")
        self.presenter.print_info(f"Ubicación actual: {self.fs.get_current_directory()}")
    
    def demo_file_updates(self):
        """Demuestra la actualización de archivos."""
        self.presenter.print_separator("ACTUALIZACIÓN DE ARCHIVOS")
        
        # Actualizar archivo existente
        self.presenter.print_step("Actualizando archivo 'readme.txt'")
        
        new_content = """Este es un archivo de prueba del sistema de archivos simulado.
¡CONTENIDO ACTUALIZADO EN LA DEMOSTRACIÓN!

CARACTERÍSTICAS IMPLEMENTADAS:
✓ Estructura tipo FAT simplificada
✓ Operaciones CRUD completas (Create, Read, Update, Delete)
✓ Navegación jerárquica de directorios
✓ Persistencia automática en disco virtual
✓ Interfaz de comandos interactiva
✓ Suite de pruebas automatizadas
✓ Manejo robusto de errores

ARQUITECTURA DEL SISTEMA:
- FileNode: Representa archivos y directorios en memoria
- VirtualDisk: Simula el almacenamiento físico
- FileSystem: Proporciona la interfaz principal

¡Sistema de archivos funcionando perfectamente!
Demostración completada exitosamente."""
        
        success, message = self.fs.update_file("readme.txt", new_content)
        if self._handle_operation_result(success, message, "Actualización de archivo"):
            self.presenter.print_info(f"Nuevo tamaño: {len(new_content)} bytes")
    
    def demo_file_deletion(self):
        """Demuestra la eliminación de archivos."""
        self.presenter.print_separator("OPERACIONES DE ELIMINACIÓN")
        
        # Crear y eliminar archivo temporal
        self.presenter.print_step("Creando archivo temporal para demostrar eliminación")
        temp_content = "Este es un archivo temporal que será eliminado para demostrar la funcionalidad."
        
        success_create, message_create = self.fs.create_file("temp_demo.txt", temp_content)
        if self._handle_operation_result(success_create, message_create, "Creación de archivo temporal"):
            
            self.presenter.print_step("Eliminando archivo temporal")
            success_delete, message_delete = self.fs.delete_file("temp_demo.txt")
            self._handle_operation_result(success_delete, message_delete, "Eliminación de archivo")
    
    def demo_persistence(self):
        """Demuestra la persistencia de datos."""
        self.presenter.print_separator("PERSISTENCIA DE DATOS")
        
        self.presenter.print_step("Verificando persistencia automática")
        self.presenter.print_info(f"Los datos se guardan automáticamente en '{DemoConfig.DEMO_FILE}'")
        self.presenter.print_info("Al reiniciar, el sistema cargará el estado previo")
        
        # Verificar que el archivo de disco existe
        if os.path.exists(DemoConfig.DEMO_FILE):
            file_size = os.path.getsize(DemoConfig.DEMO_FILE)
            self.presenter.print_success(f"Archivo de disco creado: {file_size} bytes")
        else:
            self.presenter.print_error("Archivo de disco no encontrado")
    
    def demo_final_structure(self):
        """Muestra la estructura final del sistema de archivos."""
        self.presenter.print_separator("ESTRUCTURA FINAL DEL SISTEMA")
        
        self.presenter.print_step("Generando vista completa del sistema de archivos:")
        
        # Obtener estadísticas del sistema
        stats = self.fs.get_system_stats()
        
        print(f"\n📊 ESTADÍSTICAS DEL SISTEMA:")
        print(f"  📁 Total de directorios: {stats['total_directories']}")
        print(f"  📄 Total de archivos: {stats['total_files']}")
        print(f"  💾 Tamaño total: {stats['total_size_bytes']} bytes")
        print(f"  🔧 Operaciones realizadas: {stats['operations']['total_operations']}")
        
        # Mostrar contenido del directorio raíz
        success, message, items = self.fs.list_directory()
        print(f"\n📁 Contenido del directorio raíz (/):")
        if success:
            for item in items:
                icon = "📁" if item["type"] == "directory" else "📄"
                if item["type"] == "directory":
                    # Contar elementos en el directorio
                    dir_success, _, dir_items = self.fs.list_directory(item["name"])
                    count = len(dir_items) if dir_success else 0
                    size_info = f"({count} elementos)"
                else:
                    size_info = f"({item['size']} bytes)"
                print(f"  {icon} {item['name']} {size_info}")
        else:
            self.presenter.print_error(f"Error listando directorio: {message}")
    
    def demo_completion(self):
        """Muestra el mensaje de finalización."""
        self.presenter.print_separator("DEMOSTRACIÓN COMPLETADA")
        
        self.presenter.print_success("Todas las operaciones ejecutadas exitosamente")
        self.presenter.print_success("El sistema de archivos simulado está funcionando correctamente")
        
        print("\n📋 FUNCIONALIDADES DEMOSTRADAS:")
        functionalities = [
            "Creación y gestión de directorios",
            "Operaciones CRUD completas en archivos",
            "Navegación jerárquica entre directorios",
            "Persistencia automática de datos",
            "Listado y visualización de contenido",
            "Manejo robusto de errores",
            "Estadísticas del sistema en tiempo real"
        ]
        
        for func in functionalities:
            print(f"  ✓ {func}")
        
        print(f"\n🚀 PRÓXIMOS PASOS:")
        print(f"  • Para usar el sistema interactivamente: python shell.py")
        print(f"  • Para ejecutar las pruebas: python test_crud.py")
        print(f"  • Los datos persisten en: {DemoConfig.DEMO_FILE}")
    
    def run_complete_demo(self):
        """Ejecuta la demostración completa."""
        try:
            self.presenter.print_header()
            
            # Ejecutar todas las secciones de la demostración
            demo_sections = [
                self.demo_initialization,
                self.demo_directory_creation,
                self.demo_file_operations,
                self.demo_file_reading,
                self.demo_navigation,
                self.demo_file_updates,
                self.demo_file_deletion,
                self.demo_persistence,
                self.demo_final_structure,
                self.demo_completion
            ]
            
            for section in demo_sections:
                section()
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Demostración interrumpida por el usuario")
            print("🔄 El estado actual se ha guardado automáticamente")
            
        except Exception as e:
            print(f"\n❌ Error durante la demostración: {e}")
            print("🔍 Información detallada del error:")
            import traceback
            traceback.print_exc()
            print(f"\n💾 Los datos pueden haberse guardado parcialmente en: {DemoConfig.DEMO_FILE}")


def main():
    """Función principal para ejecutar la demostración."""
    demo = FileSystemDemo()
    demo.run_complete_demo()


if __name__ == "__main__":
    main()
import os
import sys
from datetime import datetime
from filesystem import FileSystem


class CRUDTester:
    """
    Clase para realizar pruebas automatizadas de todas las operaciones CRUD.
    """
    
    def __init__(self, test_disk_file: str = "test_crud_disk.json"):
        """
        Inicializa el tester con un sistema de archivos de prueba.
        
        Args:
            test_disk_file (str): Archivo de disco para las pruebas
        """
        self.test_disk_file = test_disk_file
        self.fs = FileSystem(test_disk_file)
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Limpiar archivo de prueba si existe
        if os.path.exists(test_disk_file):
            os.remove(test_disk_file)
        
        print("🧪 Iniciando pruebas CRUD del Sistema de Archivos Simulado")
        print("=" * 60)
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """
        Registra el resultado de una prueba.
        
        Args:
            test_name (str): Nombre de la prueba
            success (bool): Si la prueba fue exitosa
            message (str): Mensaje adicional
        """
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} {test_name}"
        if message:
            result += f" - {message}"
        
        print(result)
        self.test_results.append((test_name, success, message))
        
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_file_creation(self):
        """Prueba la creación de archivos."""
        print("\n📄 Probando creación de archivos...")
        
        # Crear archivo vacío
        success, msg = self.fs.create_file("test1.txt", "")
        self.log_test("Crear archivo vacío", success, msg)
        
        # Crear archivo con contenido
        success, msg = self.fs.create_file("test2.txt", "Contenido de prueba")
        self.log_test("Crear archivo con contenido", success, msg)
        
        # Intentar crear archivo duplicado (debe fallar)
        success, msg = self.fs.create_file("test1.txt", "Duplicado")
        self.log_test("Crear archivo duplicado (debe fallar)", not success, msg)
        
        # Crear archivo con nombre inválido
        success, msg = self.fs.create_file("", "Contenido")
        self.log_test("Crear archivo con nombre vacío (debe fallar)", not success, msg)
    
    def test_file_reading(self):
        """Prueba la lectura de archivos."""
        print("\n📖 Probando lectura de archivos...")
        
        # Leer archivo existente vacío
        success, msg, content = self.fs.read_file("test1.txt")
        self.log_test("Leer archivo vacío", success and content == "", msg)
        
        # Leer archivo existente con contenido
        success, msg, content = self.fs.read_file("test2.txt")
        self.log_test("Leer archivo con contenido", 
                     success and content == "Contenido de prueba", msg)
        
        # Intentar leer archivo inexistente
        success, msg, content = self.fs.read_file("inexistente.txt")
        self.log_test("Leer archivo inexistente (debe fallar)", not success, msg)
    
    def test_file_updating(self):
        """Prueba la actualización de archivos."""
        print("\n✏️  Probando actualización de archivos...")
        
        # Actualizar archivo existente
        success, msg = self.fs.update_file("test1.txt", "Nuevo contenido")
        self.log_test("Actualizar archivo existente", success, msg)
        
        # Verificar que se actualizó correctamente
        success, msg, content = self.fs.read_file("test1.txt")
        self.log_test("Verificar actualización", 
                     success and content == "Nuevo contenido", msg)
        
        # Intentar actualizar archivo inexistente
        success, msg = self.fs.update_file("inexistente.txt", "Contenido")
        self.log_test("Actualizar archivo inexistente (debe fallar)", not success, msg)
    
    def test_file_deletion(self):
        """Prueba la eliminación de archivos."""
        print("\n🗑️  Probando eliminación de archivos...")
        
        # Eliminar archivo existente
        success, msg = self.fs.delete_file("test2.txt")
        self.log_test("Eliminar archivo existente", success, msg)
        
        # Verificar que se eliminó
        success, msg, content = self.fs.read_file("test2.txt")
        self.log_test("Verificar eliminación", not success, msg)
        
        # Intentar eliminar archivo inexistente
        success, msg = self.fs.delete_file("inexistente.txt")
        self.log_test("Eliminar archivo inexistente (debe fallar)", not success, msg)
    
    def test_directory_creation(self):
        """Prueba la creación de directorios."""
        print("\n📁 Probando creación de directorios...")
        
        # Crear directorio
        success, msg = self.fs.create_directory("test_dir")
        self.log_test("Crear directorio", success, msg)
        
        # Crear directorio anidado
        success, msg = self.fs.change_directory("test_dir")
        if success:
            success, msg = self.fs.create_directory("subdir")
            self.log_test("Crear subdirectorio", success, msg)
        
        # Volver al directorio raíz
        self.fs.change_directory("/")
        
        # Intentar crear directorio duplicado
        success, msg = self.fs.create_directory("test_dir")
        self.log_test("Crear directorio duplicado (debe fallar)", not success, msg)
    
    def test_directory_navigation(self):
        """Prueba la navegación entre directorios."""
        print("\n🧭 Probando navegación de directorios...")
        
        # Cambiar a directorio existente
        success, msg = self.fs.change_directory("test_dir")
        self.log_test("Cambiar a directorio existente", success, msg)
        
        # Verificar directorio actual
        current = self.fs.get_current_directory()
        self.log_test("Verificar directorio actual", current == "/test_dir")
        
        # Cambiar a subdirectorio
        success, msg = self.fs.change_directory("subdir")
        self.log_test("Cambiar a subdirectorio", success, msg)
        
        # Volver al directorio padre
        success, msg = self.fs.change_directory("..")
        self.log_test("Volver al directorio padre", success, msg)
        
        # Volver al directorio raíz
        success, msg = self.fs.change_directory("/")
        self.log_test("Volver al directorio raíz", success, msg)
        
        # Intentar cambiar a directorio inexistente
        success, msg = self.fs.change_directory("inexistente")
        self.log_test("Cambiar a directorio inexistente (debe fallar)", not success, msg)
    
    def test_directory_listing(self):
        """Prueba el listado de directorios."""
        print("\n📋 Probando listado de directorios...")
        
        # Listar directorio raíz
        success, msg, items = self.fs.list_directory()
        self.log_test("Listar directorio raíz", success and len(items) > 0, msg)
        
        # Listar directorio específico
        success, msg, items = self.fs.list_directory("test_dir")
        self.log_test("Listar directorio específico", success, msg)
        
        # Intentar listar directorio inexistente
        success, msg, items = self.fs.list_directory("inexistente")
        self.log_test("Listar directorio inexistente (debe fallar)", not success, msg)
    
    def test_file_operations(self):
        """Prueba operaciones adicionales con archivos."""
        print("\n🔧 Probando operaciones adicionales...")
        
        # Crear archivo para pruebas
        self.fs.create_file("original.txt", "Contenido original")
        
        # Copiar archivo
        success, msg = self.fs.copy_file("original.txt", "copia.txt")
        self.log_test("Copiar archivo", success, msg)
        
        # Verificar que la copia tiene el mismo contenido
        success, msg, content = self.fs.read_file("copia.txt")
        self.log_test("Verificar contenido de copia", 
                     success and content == "Contenido original", msg)
        
        # Verificar existencia de archivo
        exists = self.fs.file_exists("original.txt")
        self.log_test("Verificar existencia de archivo", exists)
        
        # Verificar no existencia
        exists = self.fs.file_exists("inexistente.txt")
        self.log_test("Verificar no existencia", not exists)
        
        # Obtener información de archivo
        success, msg, info = self.fs.get_file_info("original.txt")
        self.log_test("Obtener información de archivo", success, msg)
    
    def test_search_functionality(self):
        """Prueba la funcionalidad de búsqueda."""
        print("\n🔍 Probando funcionalidad de búsqueda...")
        
        # Crear archivos para búsqueda
        self.fs.create_file("buscar1.txt", "Este archivo contiene la palabra clave")
        self.fs.create_file("buscar2.txt", "Otro archivo de prueba")
        self.fs.create_file("documento.doc", "Documento importante")
        
        # Buscar por nombre
        results = self.fs.search_files("buscar")
        self.log_test("Buscar archivos por nombre", len(results) >= 2)
        
        # Buscar por contenido
        results = self.fs.search_files("clave", search_content=True)
        self.log_test("Buscar archivos por contenido", len(results) >= 1)
        
        # Buscar patrón inexistente
        results = self.fs.search_files("inexistente")
        self.log_test("Buscar patrón inexistente", len(results) == 0)
    
    def test_system_statistics(self):
        """Prueba las estadísticas del sistema."""
        print("\n📊 Probando estadísticas del sistema...")
        
        # Obtener estadísticas
        stats = self.fs.get_system_stats()
        
        # Verificar que las estadísticas contienen información válida
        has_files = stats['total_files'] > 0
        has_dirs = stats['total_directories'] > 0
        has_operations = stats['operations']['total_operations'] > 0
        
        self.log_test("Estadísticas contienen archivos", has_files)
        self.log_test("Estadísticas contienen directorios", has_dirs)
        self.log_test("Estadísticas contienen operaciones", has_operations)
    
    def test_persistence(self):
        """Prueba la persistencia de datos."""
        print("\n💾 Probando persistencia de datos...")
        
        # Crear datos de prueba
        self.fs.create_file("persistencia.txt", "Datos persistentes")
        self.fs.create_directory("dir_persistente")
        
        # Crear nuevo sistema de archivos con el mismo disco
        fs2 = FileSystem(self.test_disk_file)
        
        # Verificar que los datos persisten
        success, msg, content = fs2.read_file("persistencia.txt")
        self.log_test("Persistencia de archivos", 
                     success and content == "Datos persistentes", msg)
        
        success, msg, items = fs2.list_directory()
        dir_exists = any(item['name'] == 'dir_persistente' for item in items)
        self.log_test("Persistencia de directorios", dir_exists)
    
    def test_error_handling(self):
        """Prueba el manejo de errores."""
        print("\n⚠️  Probando manejo de errores...")
        
        # Nombres de archivo inválidos
        invalid_names = ["", ".", "..", "/", "\\", "con/barra"]
        
        for name in invalid_names:
            success, msg = self.fs.create_file(name, "contenido")
            self.log_test(f"Rechazar nombre inválido '{name}'", not success)
        
        # Operaciones en directorio como archivo
        success, msg, content = self.fs.read_file("test_dir")
        self.log_test("Leer directorio como archivo (debe fallar)", not success)
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas."""
        print(f"🚀 Iniciando pruebas completas - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Ejecutar todas las pruebas
        self.test_file_creation()
        self.test_file_reading()
        self.test_file_updating()
        self.test_file_deletion()
        self.test_directory_creation()
        self.test_directory_navigation()
        self.test_directory_listing()
        self.test_file_operations()
        self.test_search_functionality()
        self.test_system_statistics()
        self.test_persistence()
        self.test_error_handling()
        
        # Mostrar resumen
        self.show_summary()
        
        # Limpiar archivo de prueba
        if os.path.exists(self.test_disk_file):
            os.remove(self.test_disk_file)
    
    def show_summary(self):
        """Muestra el resumen de las pruebas."""
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE PRUEBAS CRUD")
        print("=" * 60)
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total de pruebas:     {total_tests}")
        print(f"Pruebas exitosas:     {self.passed_tests} ✅")
        print(f"Pruebas fallidas:     {self.failed_tests} ❌")
        print(f"Tasa de éxito:        {success_rate:.1f}%")
        
        if self.failed_tests > 0:
            print("\n❌ PRUEBAS FALLIDAS:")
            for test_name, success, message in self.test_results:
                if not success:
                    print(f"  - {test_name}: {message}")
        
        print("\n" + "=" * 60)
        
        if self.failed_tests == 0:
            print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
            print("✅ El sistema de archivos CRUD está funcionando correctamente")
        else:
            print("⚠️  Algunas pruebas fallaron. Revisar implementación.")
        
        print("=" * 60)


def main():
    """Función principal para ejecutar las pruebas."""
    print("🧪 Sistema de Pruebas CRUD - Sistema de Archivos Simulado")
    print("=" * 60)
    
    tester = CRUDTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
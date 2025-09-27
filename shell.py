import os
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime
from filesystem import FileSystem


class OSShell:
    
    
    def __init__(self, disk_file: str = "shell_disk.json"):
        """
        Inicializa el shell con un sistema de archivos.
        
        Args:
            disk_file (str): Archivo del disco virtual a utilizar
        """
        self.fs = FileSystem(disk_file)
        self.running = True
        self.command_history: List[str] = []
        
        # Configuración de colores para la interfaz
        self.colors = {
            'reset': '\033[0m',
            'bold': '\033[1m',
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m'
        }
        
        # Mapeo de comandos a métodos
        self.commands = {
            'help': self.cmd_help,
            'ls': self.cmd_ls,
            'cd': self.cmd_cd,
            'pwd': self.cmd_pwd,
            'mkdir': self.cmd_mkdir,
            'rmdir': self.cmd_rmdir,
            'touch': self.cmd_touch,
            'cat': self.cmd_cat,
            'echo': self.cmd_echo,
            'write': self.cmd_write,
            'append': self.cmd_append,
            'rm': self.cmd_rm,
            'cp': self.cmd_cp,
            'mv': self.cmd_mv,
            'find': self.cmd_find,
            'tree': self.cmd_tree,
            'info': self.cmd_info,
            'stats': self.cmd_stats,
            'history': self.cmd_history,
            'clear': self.cmd_clear,
            'exit': self.cmd_exit,
            'quit': self.cmd_exit
        }
    
    def _colorize(self, text: str, color: str) -> str:
        """
        Aplica color al texto si el terminal lo soporta.
        
        Args:
            text (str): Texto a colorizar
            color (str): Color a aplicar
            
        Returns:
            str: Texto colorizado
        """
        if os.name == 'nt':  # Windows
            return text  # Por simplicidad, sin colores en Windows
        return f"{self.colors.get(color, '')}{text}{self.colors['reset']}"
    
    def _print_success(self, message: str):
        """Imprime un mensaje de éxito en verde."""
        print(f"✅ {self._colorize(message, 'green')}")
    
    def _print_error(self, message: str):
        """Imprime un mensaje de error en rojo."""
        print(f"❌ {self._colorize(message, 'red')}")
    
    def _print_warning(self, message: str):
        """Imprime un mensaje de advertencia en amarillo."""
        print(f"⚠️  {self._colorize(message, 'yellow')}")
    
    def _print_info(self, message: str):
        """Imprime un mensaje informativo en azul."""
        print(f"ℹ️  {self._colorize(message, 'blue')}")
    
    def _format_size(self, size_bytes: int) -> str:
        """
        Formatea el tamaño en bytes a una representación legible.
        
        Args:
            size_bytes (int): Tamaño en bytes
            
        Returns:
            str: Tamaño formateado (ej: "1.5 KB")
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def _format_datetime(self, dt: datetime) -> str:
        """
        Formatea una fecha y hora para mostrar.
        
        Args:
            dt (datetime): Fecha y hora a formatear
            
        Returns:
            str: Fecha formateada
        """
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_prompt(self) -> str:
        """
        Genera el prompt del shell con el directorio actual.
        
        Returns:
            str: Prompt formateado
        """
        current_dir = self.fs.get_current_directory()
        prompt = f"{self._colorize('SimulatedOS', 'cyan')}:{self._colorize(current_dir, 'blue')}$ "
        return prompt
    
    # ==========================================
    # COMANDOS CRUD - ARCHIVOS
    # ==========================================
    
    def cmd_touch(self, args: List[str]) -> None:
        """
        Crea un archivo vacío o actualiza la fecha de modificación.
        
        Uso: touch <nombre_archivo>
        """
        if not args:
            self._print_error("Uso: touch <nombre_archivo>")
            return
        
        filename = args[0]
        
        # Si el archivo existe, solo actualizar fecha
        if self.fs.file_exists(filename):
            success, msg, content = self.fs.read_file(filename)
            if success:
                success, msg = self.fs.update_file(filename, content)
                if success:
                    self._print_success(f"Fecha de '{filename}' actualizada")
                else:
                    self._print_error(msg)
            else:
                self._print_error(msg)
        else:
            # Crear archivo nuevo
            success, msg = self.fs.create_file(filename, "")
            if success:
                self._print_success(msg)
            else:
                self._print_error(msg)
    
    def cmd_cat(self, args: List[str]) -> None:
        """
        Muestra el contenido de un archivo.
        
        Uso: cat <nombre_archivo>
        """
        if not args:
            self._print_error("Uso: cat <nombre_archivo>")
            return
        
        filename = args[0]
        success, msg, content = self.fs.read_file(filename)
        
        if success:
            if content:
                print(content)
            else:
                self._print_info(f"El archivo '{filename}' está vacío")
        else:
            self._print_error(msg)
    
    def cmd_echo(self, args: List[str]) -> None:
        """
        Escribe texto en un archivo (sobrescribe el contenido).
        
        Uso: echo "texto" > archivo
        Uso: echo "texto"  (solo muestra el texto)
        """
        if not args:
            self._print_error("Uso: echo \"texto\" [> archivo]")
            return
        
        # Unir todos los argumentos como texto
        text = " ".join(args)
        
        # Verificar si hay redirección
        if ">" in text:
            parts = text.split(">", 1)
            if len(parts) == 2:
                content = parts[0].strip().strip('"').strip("'")
                filename = parts[1].strip()
                
                success, msg = self.fs.create_file(filename, content)
                if not success:
                    # Si no se pudo crear, intentar actualizar
                    success, msg = self.fs.update_file(filename, content)
                
                if success:
                    self._print_success(f"Texto escrito en '{filename}'")
                else:
                    self._print_error(msg)
            else:
                self._print_error("Formato inválido. Uso: echo \"texto\" > archivo")
        else:
            # Solo mostrar el texto
            print(text.strip('"').strip("'"))
    
    def cmd_write(self, args: List[str]) -> None:
        """
        Escribe contenido en un archivo de forma interactiva.
        
        Uso: write <nombre_archivo>
        """
        if not args:
            self._print_error("Uso: write <nombre_archivo>")
            return
        
        filename = args[0]
        
        print(f"Escribiendo en '{filename}'. Presiona Ctrl+D (Linux/Mac) o Ctrl+Z+Enter (Windows) para terminar:")
        print("=" * 50)
        
        lines = []
        try:
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
        except KeyboardInterrupt:
            self._print_warning("Escritura cancelada")
            return
        
        content = "\n".join(lines)
        
        # Intentar crear o actualizar el archivo
        success, msg = self.fs.create_file(filename, content)
        if not success:
            success, msg = self.fs.update_file(filename, content)
        
        if success:
            self._print_success(f"Contenido guardado en '{filename}' ({len(content)} bytes)")
        else:
            self._print_error(msg)
    
    def cmd_append(self, args: List[str]) -> None:
        """
        Añade contenido al final de un archivo.
        
        Uso: append <nombre_archivo> "texto"
        """
        if len(args) < 2:
            self._print_error("Uso: append <nombre_archivo> \"texto\"")
            return
        
        filename = args[0]
        new_text = " ".join(args[1:]).strip('"').strip("'")
        
        # Leer contenido actual
        success, msg, current_content = self.fs.read_file(filename)
        if not success:
            self._print_error(f"No se pudo leer '{filename}': {msg}")
            return
        
        # Añadir nuevo contenido
        updated_content = current_content + "\n" + new_text if current_content else new_text
        
        success, msg = self.fs.update_file(filename, updated_content)
        if success:
            self._print_success(f"Texto añadido a '{filename}'")
        else:
            self._print_error(msg)
    
    def cmd_rm(self, args: List[str]) -> None:
        """
        Elimina un archivo o directorio vacío.
        
        Uso: rm <nombre>
        """
        if not args:
            self._print_error("Uso: rm <nombre>")
            return
        
        filename = args[0]
        success, msg = self.fs.delete_file(filename)
        
        if success:
            self._print_success(msg)
        else:
            self._print_error(msg)
    
    def cmd_cp(self, args: List[str]) -> None:
        """
        Copia un archivo.
        
        Uso: cp <origen> <destino>
        """
        if len(args) != 2:
            self._print_error("Uso: cp <origen> <destino>")
            return
        
        source, destination = args[0], args[1]
        success, msg = self.fs.copy_file(source, destination)
        
        if success:
            self._print_success(msg)
        else:
            self._print_error(msg)
    
    def cmd_mv(self, args: List[str]) -> None:
        """
        Mueve/renombra un archivo (copia + elimina original).
        
        Uso: mv <origen> <destino>
        """
        if len(args) != 2:
            self._print_error("Uso: mv <origen> <destino>")
            return
        
        source, destination = args[0], args[1]
        
        # Copiar archivo
        success, msg = self.fs.copy_file(source, destination)
        if not success:
            self._print_error(f"Error copiando: {msg}")
            return
        
        # Eliminar original
        success, msg = self.fs.delete_file(source)
        if success:
            self._print_success(f"'{source}' movido a '{destination}'")
        else:
            self._print_error(f"Archivo copiado pero no se pudo eliminar el original: {msg}")
    
    # ==========================================
    # COMANDOS CRUD - DIRECTORIOS
    # ==========================================
    
    def cmd_mkdir(self, args: List[str]) -> None:
        """
        Crea un nuevo directorio.
        
        Uso: mkdir <nombre_directorio>
        """
        if not args:
            self._print_error("Uso: mkdir <nombre_directorio>")
            return
        
        dirname = args[0]
        success, msg = self.fs.create_directory(dirname)
        
        if success:
            self._print_success(msg)
        else:
            self._print_error(msg)
    
    def cmd_rmdir(self, args: List[str]) -> None:
        """
        Elimina un directorio vacío.
        
        Uso: rmdir <nombre_directorio>
        """
        if not args:
            self._print_error("Uso: rmdir <nombre_directorio>")
            return
        
        dirname = args[0]
        success, msg = self.fs.delete_file(dirname)  # delete_file maneja directorios también
        
        if success:
            self._print_success(msg)
        else:
            self._print_error(msg)
    
    def cmd_ls(self, args: List[str]) -> None:
        """
        Lista el contenido del directorio actual o especificado.
        
        Uso: ls [directorio] [-l para formato detallado]
        """
        detailed = "-l" in args
        path = None
        
        # Filtrar argumentos
        for arg in args:
            if arg != "-l":
                path = arg
                break
        
        success, msg, items = self.fs.list_directory(path)
        
        if not success:
            self._print_error(msg)
            return
        
        if not items:
            self._print_info("Directorio vacío")
            return
        
        if detailed:
            # Formato detallado
            print(f"{'Permisos':<10} {'Tipo':<10} {'Tamaño':<10} {'Modificado':<20} {'Nombre'}")
            print("-" * 70)
            
            for item in items:
                size_str = str(item['size']) if item['type'] == 'file' else f"<{item['size']}>"
                modified_str = self._format_datetime(item['modified'])
                
                # Colorizar según el tipo
                name = item['name']
                if item['type'] == 'directory':
                    name = self._colorize(name + "/", 'blue')
                
                print(f"{item['permissions']:<10} {item['type']:<10} {size_str:<10} {modified_str:<20} {name}")
        else:
            # Formato simple
            for item in items:
                name = item['name']
                if item['type'] == 'directory':
                    name = self._colorize(name + "/", 'blue')
                print(name, end="  ")
            print()  # Nueva línea al final
    
    def cmd_cd(self, args: List[str]) -> None:
        """
        Cambia el directorio actual.
        
        Uso: cd [directorio]
        """
        if not args:
            # Sin argumentos, ir al directorio raíz
            success, msg = self.fs.change_directory("/")
        else:
            success, msg = self.fs.change_directory(args[0])
        
        if success:
            # No mostrar mensaje de éxito para cd, solo cambiar
            pass
        else:
            self._print_error(msg)
    
    def cmd_pwd(self, args: List[str]) -> None:
        """
        Muestra el directorio actual.
        
        Uso: pwd
        """
        current_dir = self.fs.get_current_directory()
        print(self._colorize(current_dir, 'blue'))
    
    # ==========================================
    # COMANDOS DE INFORMACIÓN Y UTILIDADES
    # ==========================================
    
    def cmd_tree(self, args: List[str]) -> None:
        """
        Muestra la estructura de directorios en forma de árbol.
        
        Uso: tree [directorio]
        """
        path = args[0] if args else None
        success, msg, items = self.fs.list_directory(path)
        
        if not success:
            self._print_error(msg)
            return
        
        current_path = path or self.fs.get_current_directory()
        print(f"📁 {self._colorize(current_path, 'blue')}")
        
        self._print_tree_recursive(current_path, "", True)
    
    def _print_tree_recursive(self, path: str, prefix: str, is_last: bool) -> None:
        """
        Función auxiliar para imprimir el árbol recursivamente.
        
        Args:
            path (str): Ruta actual
            prefix (str): Prefijo para la indentación
            is_last (bool): Si es el último elemento del nivel
        """
        success, msg, items = self.fs.list_directory(path)
        if not success:
            return
        
        for i, item in enumerate(items):
            is_last_item = (i == len(items) - 1)
            current_prefix = "└── " if is_last_item else "├── "
            
            name = item['name']
            if item['type'] == 'directory':
                name = self._colorize(name, 'blue')
                icon = "📁"
            else:
                icon = "📄"
            
            print(f"{prefix}{current_prefix}{icon} {name}")
            
            # Recursión para directorios
            if item['type'] == 'directory':
                next_prefix = prefix + ("    " if is_last_item else "│   ")
                child_path = f"{path}/{item['name']}" if path != "/" else f"/{item['name']}"
                self._print_tree_recursive(child_path, next_prefix, is_last_item)
    
    def cmd_info(self, args: List[str]) -> None:
        """
        Muestra información detallada de un archivo o directorio.
        
        Uso: info <nombre>
        """
        if not args:
            self._print_error("Uso: info <nombre>")
            return
        
        filename = args[0]
        success, msg, info = self.fs.get_file_info(filename)
        
        if not success:
            self._print_error(msg)
            return
        
        print(f"\n📋 {self._colorize('Información detallada', 'bold')}")
        print("=" * 40)
        print(f"Nombre:           {info['name']}")
        print(f"Tipo:             {info['type']}")
        print(f"Ruta completa:    {info['full_path']}")
        print(f"Tamaño:           {self._format_size(info['size'])}")
        if info['type'] == 'directory':
            print(f"Tamaño recursivo: {self._format_size(info['size_recursive'])}")
        print(f"Creado:           {self._format_datetime(info['created'])}")
        print(f"Modificado:       {self._format_datetime(info['modified'])}")
        print(f"Permisos:         {info['permissions']}")
        print(f"Accesos:          {info['access_count']}")
        print()
    
    def cmd_stats(self, args: List[str]) -> None:
        """
        Muestra estadísticas del sistema de archivos.
        
        Uso: stats
        """
        stats = self.fs.get_system_stats()
        
        print(f"\n📊 {self._colorize('Estadísticas del Sistema', 'bold')}")
        print("=" * 50)
        print(f"Directorio actual:    {stats['current_directory']}")
        print(f"Total de archivos:    {stats['total_files']}")
        print(f"Total de directorios: {stats['total_directories']}")
        print(f"Tamaño total:         {self._format_size(stats['total_size_bytes'])}")
        
        print(f"\n📈 {self._colorize('Operaciones realizadas', 'bold')}")
        print("-" * 30)
        ops = stats['operations']
        print(f"Archivos creados:     {ops['files_created']}")
        print(f"Archivos eliminados:  {ops['files_deleted']}")
        print(f"Directorios creados:  {ops['directories_created']}")
        print(f"Directorios eliminados: {ops['directories_deleted']}")
        print(f"Total de operaciones: {ops['total_operations']}")
        
        print(f"\n💾 {self._colorize('Información del disco', 'bold')}")
        print("-" * 30)
        disk = stats['disk']
        print(f"Archivo del disco:    {disk['disk_file']}")
        print(f"Bloques totales:      {disk['total_blocks']}")
        print(f"Bloques usados:       {disk['used_blocks']}")
        print(f"Bloques libres:       {disk['free_blocks']}")
        print(f"Tamaño de bloque:     {disk['block_size']} bytes")
        print()
    
    def cmd_find(self, args: List[str]) -> None:
        """
        Busca archivos por nombre o contenido.
        
        Uso: find <patrón> [-c para buscar en contenido]
        """
        if not args:
            self._print_error("Uso: find <patrón> [-c para buscar en contenido]")
            return
        
        pattern = args[0]
        search_content = "-c" in args
        
        results = self.fs.search_files(pattern, search_content)
        
        if not results:
            self._print_info(f"No se encontraron resultados para '{pattern}'")
            return
        
        print(f"\n🔍 {self._colorize(f'Resultados de búsqueda para: {pattern}', 'bold')}")
        print("=" * 50)
        
        for result in results:
            match_type = "📄 contenido" if result['match_type'] == 'content' else "📝 nombre"
            type_icon = "📁" if result['type'] == 'directory' else "📄"
            
            print(f"{type_icon} {result['path']} ({match_type})")
        
        print(f"\nTotal: {len(results)} resultado(s)")
    
    def cmd_history(self, args: List[str]) -> None:
        """
        Muestra el historial de comandos.
        
        Uso: history
        """
        if not self.command_history:
            self._print_info("No hay comandos en el historial")
            return
        
        print(f"\n📜 {self._colorize('Historial de comandos', 'bold')}")
        print("-" * 30)
        
        for i, cmd in enumerate(self.command_history[-20:], 1):  # Últimos 20 comandos
            print(f"{i:2d}. {cmd}")
        print()
    
    def cmd_clear(self, args: List[str]) -> None:
        """
        Limpia la pantalla.
        
        Uso: clear
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cmd_help(self, args: List[str]) -> None:
        """
        Muestra la ayuda de comandos disponibles.
        
        Uso: help [comando]
        """
        if args:
            # Ayuda específica de un comando
            cmd_name = args[0]
            if cmd_name in self.commands:
                method = self.commands[cmd_name]
                print(f"\n📖 {self._colorize(f'Ayuda para: {cmd_name}', 'bold')}")
                print("=" * 40)
                print(method.__doc__ or "Sin documentación disponible")
            else:
                self._print_error(f"Comando '{cmd_name}' no encontrado")
            return
        
        # Ayuda general
        print(f"\n📚 {self._colorize('Sistema de Archivos Simulado - Comandos Disponibles', 'bold')}")
        print("=" * 70)
        
        categories = {
            "📁 Gestión de Directorios": ['ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'tree'],
            "📄 Gestión de Archivos": ['touch', 'cat', 'echo', 'write', 'append', 'rm', 'cp', 'mv'],
            "🔍 Búsqueda e Información": ['find', 'info', 'stats'],
            "🛠️  Utilidades": ['help', 'history', 'clear', 'exit']
        }
        
        for category, commands in categories.items():
            print(f"\n{self._colorize(category, 'cyan')}")
            for cmd in commands:
                if cmd in self.commands:
                    # Extraer primera línea de la documentación
                    doc = self.commands[cmd].__doc__
                    if doc:
                        first_line = doc.strip().split('\n')[0]
                        print(f"  {cmd:<12} - {first_line}")
        
        print(f"\n💡 {self._colorize('Tip:', 'yellow')} Usa 'help <comando>' para obtener ayuda específica")
        print()
    
    def cmd_exit(self, args: List[str]) -> None:
        """
        Sale del shell.
        
        Uso: exit o quit
        """
        print(f"\n👋 {self._colorize('¡Gracias por usar el Sistema de Archivos Simulado!', 'green')}")
        self.running = False
    
    # ==========================================
    # FUNCIONES PRINCIPALES DEL SHELL
    # ==========================================
    
    def parse_command(self, command_line: str) -> tuple:
        """
        Parsea una línea de comando en comando y argumentos.
        
        Args:
            command_line (str): Línea de comando completa
            
        Returns:
            tuple: (comando, lista_de_argumentos)
        """
        # Limpiar la línea de comando
        command_line = command_line.strip()
        
        if not command_line:
            return "", []
        
        # Dividir por espacios, pero preservar comillas
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(command_line):
            char = command_line[i]
            
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                i += 1
                continue
            else:
                current_part += char
            
            i += 1
        
        if current_part:
            parts.append(current_part)
        
        if not parts:
            return "", []
        
        command = parts[0].lower()
        args = parts[1:]
        
        # Limpiar comillas de los argumentos
        cleaned_args = []
        for arg in args:
            if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                cleaned_args.append(arg[1:-1])
            else:
                cleaned_args.append(arg)
        
        return command, cleaned_args
    
    def execute_command(self, command: str, args: List[str]) -> None:
        """
        Ejecuta un comando con sus argumentos.
        
        Args:
            command (str): Nombre del comando
            args (List[str]): Lista de argumentos
        """
        # Validar entrada
        if not command:
            return
        
        # Limpiar argumentos de caracteres problemáticos
        cleaned_args = []
        for arg in args:
            if arg:  # Solo procesar argumentos no vacíos
                cleaned_arg = arg.strip()
                if cleaned_arg:  # Solo agregar si no está vacío después de limpiar
                    cleaned_args.append(cleaned_arg)
        
        if command in self.commands:
            try:
                self.commands[command](cleaned_args)
            except KeyboardInterrupt:
                self._print_warning("\nComando interrumpido")
            except Exception as e:
                self._print_error(f"Error ejecutando comando '{command}': {e}")
        elif command:
            self._print_error(f"Comando '{command}' no reconocido. Usa 'help' para ver comandos disponibles.")
    
    def run(self) -> None:
        """
        Ejecuta el bucle principal del shell.
        """
        print(f"\n🚀 {self._colorize('Bienvenido al Sistema de Archivos Simulado', 'bold')}")
        print(f"📖 Escribe '{self._colorize('help', 'cyan')}' para ver los comandos disponibles")
        print(f"🚪 Escribe '{self._colorize('exit', 'cyan')}' para salir\n")
        
        while self.running:
            try:
                # Mostrar prompt y leer comando
                command_line = input(self._get_prompt())
                
                # Añadir al historial si no está vacío
                if command_line.strip():
                    self.command_history.append(command_line.strip())
                
                # Parsear y ejecutar comando
                command, args = self.parse_command(command_line)
                self.execute_command(command, args)
                
            except KeyboardInterrupt:
                print(f"\n\n👋 {self._colorize('¡Hasta luego!', 'green')}")
                break
            except EOFError:
                print(f"\n\n👋 {self._colorize('¡Hasta luego!', 'green')}")
                break


def main():
    """
    Función principal para ejecutar el shell.
    """
    if len(sys.argv) > 1:
        disk_file = sys.argv[1]
    else:
        disk_file = "shell_disk.json"
    
    shell = OSShell(disk_file)
    shell.run()


if __name__ == "__main__":
    main()
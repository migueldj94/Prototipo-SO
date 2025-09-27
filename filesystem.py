"""
Sistema de Archivos Simulado para Prototipo de OS
==================================================

Este módulo implementa un sistema de archivos completo con:
- Estructura tipo FAT (File Allocation Table) simplificada
- Operaciones CRUD completas para archivos y directorios
- Persistencia en disco virtual usando archivos JSON
- Navegación jerárquica de directorios
- Metadatos completos (timestamps, permisos, tamaños)

Autor: Equipo de Desarrollo OS
Versión: 2.0
"""

import json
import os
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime


class FileNode:
    """
    Representa un archivo o directorio en el sistema de archivos.
    
    Esta clase encapsula toda la información necesaria para un nodo
    en el árbol de archivos, incluyendo metadatos y relaciones jerárquicas.
    """
    
    def __init__(self, name: str, is_directory: bool = False, parent: Optional['FileNode'] = None):
        """
        Inicializa un nuevo nodo de archivo o directorio.
        
        Args:
            name (str): Nombre del archivo o directorio
            is_directory (bool): True si es directorio, False si es archivo
            parent (FileNode, optional): Nodo padre en la jerarquía
        """
        self.name = name
        self.is_directory = is_directory
        self.parent = parent
        
        # Los directorios tienen hijos, los archivos no
        self.children: Dict[str, 'FileNode'] = {} if is_directory else {}
        
        # Contenido solo para archivos
        self.content: str = "" if not is_directory else ""
        
        # Metadatos del archivo/directorio
        self.size = 0
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.permissions = "rwx" if is_directory else "rw-"
        self.access_count = 0  # Contador de accesos
    
    def get_full_path(self) -> str:
        """
        Obtiene la ruta completa del archivo/directorio desde la raíz.
        
        Returns:
            str: Ruta completa (ej: "/documentos/archivo.txt")
        """
        if self.parent is None:
            return "/"
        elif self.parent.parent is None:
            return f"/{self.name}"
        else:
            return f"{self.parent.get_full_path()}/{self.name}"
    
    def update_access_time(self):
        """Actualiza el tiempo de último acceso y contador."""
        self.access_count += 1
        # En un sistema real, tendríamos access_time separado
        # Por simplicidad, usamos modified_at
    
    def get_size_recursive(self) -> int:
        """
        Calcula el tamaño total incluyendo subdirectorios.
        
        Returns:
            int: Tamaño total en bytes
        """
        if not self.is_directory:
            return self.size
        
        total_size = 0
        for child in self.children.values():
            total_size += child.get_size_recursive()
        return total_size


class VirtualDisk:
    """
    Simula un disco virtual usando archivos del sistema host.
    
    Implementa una tabla FAT simplificada que se almacena en formato JSON
    para facilitar la persistencia y el debugging.
    """
    
    def __init__(self, disk_file: str = "virtual_disk.json"):
        """
        Inicializa el disco virtual.
        
        Args:
            disk_file (str): Archivo donde se almacena el disco virtual
        """
        self.disk_file = disk_file
        self.fat_table = {}
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "total_blocks": 1000,
            "block_size": 512,
            "used_blocks": 0
        }
    
    def load_disk(self) -> bool:
        """
        Carga el disco virtual desde el archivo.
        
        Returns:
            bool: True si se cargó exitosamente, False si se creó nuevo
        """
        try:
            if os.path.exists(self.disk_file):
                with open(self.disk_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.fat_table = data.get('fat_table', {})
                    self.metadata = data.get('metadata', self.metadata)
                return True
            else:
                # Crear disco vacío
                self.fat_table = self._create_empty_fat()
                self.save_disk()
                return False
        except (json.JSONDecodeError, IOError) as e:
            # En caso de error, crear disco vacío
            self.fat_table = self._create_empty_fat()
            return False
    
    def save_disk(self) -> bool:
        """
        Guarda el disco virtual en el archivo.
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            self.metadata["last_modified"] = datetime.now().isoformat()
            data = {
                "fat_table": self.fat_table,
                "metadata": self.metadata
            }
            with open(self.disk_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def _create_empty_fat(self) -> Dict[str, Any]:
        """
        Crea una tabla FAT vacía con solo el directorio raíz.
        
        Returns:
            Dict[str, Any]: Tabla FAT inicial
        """
        return {
            "/": {
                "name": "/",
                "type": "directory",
                "size": 0,
                "created_at": datetime.now().isoformat(),
                "modified_at": datetime.now().isoformat(),
                "permissions": "rwx",
                "access_count": 0,
                "children": {},
                "content": ""
            }
        }
    
    def get_disk_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del disco virtual.
        
        Returns:
            Dict[str, Any]: Estadísticas del disco
        """
        return {
            "disk_file": self.disk_file,
            "total_blocks": self.metadata["total_blocks"],
            "used_blocks": self.metadata["used_blocks"],
            "free_blocks": self.metadata["total_blocks"] - self.metadata["used_blocks"],
            "block_size": self.metadata["block_size"]
        }


class FileSystem:
    """
    Sistema de archivos principal que gestiona todas las operaciones.
    
    Proporciona una interfaz completa para operaciones CRUD en archivos
    y directorios, con navegación jerárquica y persistencia automática.
    """
    
    def __init__(self, disk_file: str = "virtual_disk.json"):
        """
        Inicializa el sistema de archivos.
        
        Args:
            disk_file (str): Archivo del disco virtual a utilizar
        """
        self.disk = VirtualDisk(disk_file)
        self.disk.load_disk()
        
        # Construir árbol de archivos desde la tabla FAT
        self.root = self._build_tree_from_fat()
        self.current_directory = self.root
        
        # Estadísticas de operaciones
        self.stats = {
            "files_created": 0,
            "files_deleted": 0,
            "directories_created": 0,
            "directories_deleted": 0,
            "total_operations": 0
        }
    
    def _build_tree_from_fat(self) -> FileNode:
        """
        Construye el árbol de archivos desde la tabla FAT.
        
        Returns:
            FileNode: Nodo raíz del árbol de archivos
        """
        # Crear nodo raíz
        root_data = self.disk.fat_table.get("/", {})
        root = FileNode("/", is_directory=True)
        
        # Poblar el árbol recursivamente
        self._populate_node(root, root_data)
        return root
    
    def _populate_node(self, node: FileNode, data: Dict[str, Any]):
        """
        Puebla un nodo con datos de la tabla FAT recursivamente.
        
        Args:
            node (FileNode): Nodo a poblar
            data (Dict[str, Any]): Datos del nodo desde la FAT
        """
        if not data:
            return
        
        # Establecer metadatos
        node.size = data.get("size", 0)
        node.content = data.get("content", "")
        node.permissions = data.get("permissions", "rw-")
        node.access_count = data.get("access_count", 0)
        
        # Parsear fechas
        try:
            node.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
            node.modified_at = datetime.fromisoformat(data.get("modified_at", datetime.now().isoformat()))
        except ValueError:
            # Si hay error en el formato de fecha, usar fecha actual
            node.created_at = datetime.now()
            node.modified_at = datetime.now()
        
        # Poblar hijos si es directorio
        if node.is_directory and "children" in data:
            for child_name, child_data in data["children"].items():
                is_dir = child_data.get("type", "file") == "directory"
                child_node = FileNode(child_name, is_directory=is_dir, parent=node)
                node.children[child_name] = child_node
                
                # Recursión para poblar el hijo
                self._populate_node(child_node, child_data)
    
    def _update_fat_from_tree(self):
        """Actualiza la tabla FAT desde el árbol de archivos."""
        self.disk.fat_table = {"/": self._node_to_dict(self.root)}
    
    def _node_to_dict(self, node: FileNode) -> Dict[str, Any]:
        """
        Convierte un nodo del árbol a diccionario para la FAT.
        
        Args:
            node (FileNode): Nodo a convertir
            
        Returns:
            Dict[str, Any]: Representación del nodo como diccionario
        """
        result = {
            "name": node.name,
            "type": "directory" if node.is_directory else "file",
            "size": node.size,
            "created_at": node.created_at.isoformat(),
            "modified_at": node.modified_at.isoformat(),
            "permissions": node.permissions,
            "access_count": node.access_count,
            "content": node.content,
            "children": {}
        }
        
        # Agregar hijos si es directorio
        if node.is_directory:
            for child_name, child_node in node.children.items():
                result["children"][child_name] = self._node_to_dict(child_node)
        
        return result
    
    # ==========================================
    # MÉTODOS DE NAVEGACIÓN Y UTILIDADES
    # ==========================================
    
    def _get_node_by_path(self, path: str) -> Optional[FileNode]:
        """
        Obtiene un nodo por su ruta absoluta o relativa.
        
        Args:
            path (str): Ruta del archivo/directorio
            
        Returns:
            FileNode: Nodo encontrado o None si no existe
        """
        if not path or path == "/":
            return self.root
        
        # Normalizar ruta
        if path.startswith("/"):
            # Ruta absoluta
            current = self.root
            parts = [p for p in path.split("/") if p]
        else:
            # Ruta relativa
            current = self.current_directory
            parts = [p for p in path.split("/") if p]
        
        # Navegar por las partes de la ruta
        for part in parts:
            if part == "..":
                # Subir un nivel
                if current.parent:
                    current = current.parent
            elif part == ".":
                # Directorio actual, no hacer nada
                continue
            else:
                # Buscar hijo
                if current.is_directory and part in current.children:
                    current = current.children[part]
                else:
                    return None
        
        return current
    
    def _get_current_node(self) -> Optional[FileNode]:
        """
        Obtiene el nodo del directorio actual.
        
        Returns:
            FileNode: Nodo del directorio actual
        """
        return self.current_directory
    
    def _validate_filename(self, filename: str) -> Tuple[bool, str]:
        """
        Valida que un nombre de archivo sea válido.
        
        Args:
            filename (str): Nombre a validar
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        if not filename or filename.strip() == "":
            return False, "El nombre no puede estar vacío"
        
        # Limpiar el nombre
        filename = filename.strip()
        
        # Caracteres no permitidos en sistemas de archivos
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\0']
        for char in invalid_chars:
            if char in filename:
                return False, f"El nombre contiene el carácter no permitido: '{char}'"
        
        # Nombres reservados del sistema
        reserved_names = ['.', '..', 'CON', 'PRN', 'AUX', 'NUL', 
                         'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                         'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        
        if filename.upper() in reserved_names:
            return False, f"'{filename}' es un nombre reservado del sistema"
        
        # Verificar longitud máxima
        if len(filename) > 255:
            return False, "El nombre es demasiado largo (máximo 255 caracteres)"
        
        # Verificar que no termine con punto o espacio (problemático en Windows)
        if filename.endswith('.') or filename.endswith(' '):
            return False, "El nombre no puede terminar con punto o espacio"
        
        return True, ""
    
    def _save_changes(self):
        """Guarda los cambios en el disco virtual."""
        self._update_fat_from_tree()
        self.disk.save_disk()
        self.stats["total_operations"] += 1
    
    # ==========================================
    # OPERACIONES CRUD - ARCHIVOS
    # ==========================================
    
    def create_file(self, filename: str, content: str = "") -> Tuple[bool, str]:
        """
        Crea un nuevo archivo en el directorio actual.
        
        Args:
            filename (str): Nombre del archivo a crear
            content (str): Contenido inicial del archivo
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validar nombre de archivo
        is_valid, error_msg = self._validate_filename(filename)
        if not is_valid:
            return False, error_msg
        
        current = self._get_current_node()
        if not current or not current.is_directory:
            return False, "No se puede crear archivo: directorio actual inválido"
        
        # Verificar que no existe
        if filename in current.children:
            return False, f"El archivo '{filename}' ya existe"
        
        # Crear nuevo nodo de archivo
        new_file = FileNode(filename, is_directory=False, parent=current)
        new_file.content = content
        new_file.size = len(content.encode('utf-8'))
        new_file.modified_at = datetime.now()
        
        # Agregar al directorio actual
        current.children[filename] = new_file
        
        # Guardar cambios
        self.stats["files_created"] += 1
        self._save_changes()
        
        return True, f"Archivo '{filename}' creado exitosamente"
    
    def read_file(self, filename: str) -> Tuple[bool, str, Optional[str]]:
        """
        Lee el contenido de un archivo.
        
        Args:
            filename (str): Nombre del archivo a leer
            
        Returns:
            Tuple[bool, str, Optional[str]]: (éxito, mensaje, contenido)
        """
        current = self._get_current_node()
        if not current or not current.is_directory:
            return False, "Directorio actual inválido", None
        
        # Buscar archivo
        if filename not in current.children:
            return False, f"El archivo '{filename}' no existe", None
        
        file_node = current.children[filename]
        if file_node.is_directory:
            return False, f"'{filename}' es un directorio, no un archivo", None
        
        # Actualizar estadísticas de acceso
        file_node.update_access_time()
        self._save_changes()
        
        return True, f"Archivo '{filename}' leído exitosamente", file_node.content
    
    def update_file(self, filename: str, content: str) -> Tuple[bool, str]:
        """
        Actualiza el contenido de un archivo existente.
        
        Args:
            filename (str): Nombre del archivo a actualizar
            content (str): Nuevo contenido del archivo
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        current = self._get_current_node()
        if not current or not current.is_directory:
            return False, "Directorio actual inválido"
        
        # Buscar archivo
        if filename not in current.children:
            return False, f"El archivo '{filename}' no existe"
        
        file_node = current.children[filename]
        if file_node.is_directory:
            return False, f"'{filename}' es un directorio, no un archivo"
        
        # Actualizar contenido
        file_node.content = content
        file_node.size = len(content.encode('utf-8'))
        file_node.modified_at = datetime.now()
        file_node.update_access_time()
        
        # Guardar cambios
        self._save_changes()
        
        return True, f"Archivo '{filename}' actualizado exitosamente"
    
    def delete_file(self, filename: str) -> Tuple[bool, str]:
        """
        Elimina un archivo o directorio vacío.
        
        Args:
            filename (str): Nombre del archivo/directorio a eliminar
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        current = self._get_current_node()
        if not current or not current.is_directory:
            return False, "Directorio actual inválido"
        
        # Buscar archivo/directorio
        if filename not in current.children:
            return False, f"'{filename}' no existe"
        
        node_to_delete = current.children[filename]
        
        # Si es directorio, verificar que esté vacío
        if node_to_delete.is_directory:
            if node_to_delete.children:
                return False, f"El directorio '{filename}' no está vacío"
            self.stats["directories_deleted"] += 1
        else:
            self.stats["files_deleted"] += 1
        
        # Eliminar del directorio padre
        del current.children[filename]
        
        # Guardar cambios
        self._save_changes()
        
        tipo = "directorio" if node_to_delete.is_directory else "archivo"
        return True, f"{tipo.capitalize()} '{filename}' eliminado exitosamente"
    
    # ==========================================
    # OPERACIONES CRUD - DIRECTORIOS
    # ==========================================
    
    def create_directory(self, dirname: str) -> Tuple[bool, str]:
        """
        Crea un nuevo directorio en el directorio actual.
        
        Args:
            dirname (str): Nombre del directorio a crear
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validar nombre de directorio
        is_valid, error_msg = self._validate_filename(dirname)
        if not is_valid:
            return False, error_msg
        
        current = self._get_current_node()
        if not current or not current.is_directory:
            return False, "No se puede crear directorio: directorio actual inválido"
        
        # Verificar que no existe
        if dirname in current.children:
            return False, f"El directorio '{dirname}' ya existe"
        
        # Crear nuevo nodo de directorio
        new_dir = FileNode(dirname, is_directory=True, parent=current)
        
        # Agregar al directorio actual
        current.children[dirname] = new_dir
        
        # Guardar cambios
        self.stats["directories_created"] += 1
        self._save_changes()
        
        return True, f"Directorio '{dirname}' creado exitosamente"
    
    def list_directory(self, path: str = None) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Lista el contenido de un directorio.
        
        Args:
            path (str, optional): Ruta del directorio a listar (None para actual)
            
        Returns:
            Tuple[bool, str, List[Dict[str, Any]]]: (éxito, mensaje, lista_de_elementos)
        """
        if path:
            target_node = self._get_node_by_path(path)
        else:
            target_node = self._get_current_node()
        
        if not target_node:
            return False, f"El directorio '{path or 'actual'}' no existe", []
        
        if not target_node.is_directory:
            return False, f"'{path or 'actual'}' no es un directorio", []
        
        # Construir lista de elementos
        items = []
        for name, node in target_node.children.items():
            items.append({
                "name": name,
                "type": "directory" if node.is_directory else "file",
                "size": node.get_size_recursive() if node.is_directory else node.size,
                "created": node.created_at,
                "modified": node.modified_at,
                "permissions": node.permissions,
                "access_count": node.access_count
            })
        
        # Ordenar por nombre
        items.sort(key=lambda x: x["name"])
        
        return True, f"Contenido del directorio listado exitosamente", items
    
    def change_directory(self, path: str) -> Tuple[bool, str]:
        """
        Cambia el directorio actual.
        
        Args:
            path (str): Ruta del directorio destino
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        target_node = self._get_node_by_path(path)
        
        if not target_node:
            return False, f"El directorio '{path}' no existe"
        
        if not target_node.is_directory:
            return False, f"'{path}' no es un directorio"
        
        # Cambiar directorio actual
        self.current_directory = target_node
        
        # Actualizar estadísticas de acceso
        target_node.update_access_time()
        self._save_changes()
        
        return True, f"Directorio cambiado a '{target_node.get_full_path()}'"
    
    # ==========================================
    # MÉTODOS DE INFORMACIÓN Y UTILIDADES
    # ==========================================
    
    def get_current_directory(self) -> str:
        """Obtiene la ruta del directorio actual."""
        return self.current_directory.get_full_path()
    
    def file_exists(self, filename: str) -> bool:
        """
        Verifica si un archivo existe en el directorio actual.
        
        Args:
            filename (str): Nombre del archivo a verificar
            
        Returns:
            bool: True si existe, False si no
        """
        current = self._get_current_node()
        return current and filename in current.children
    
    def get_file_info(self, filename: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Obtiene información detallada de un archivo o directorio.
        
        Args:
            filename (str): Nombre del archivo/directorio
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (éxito, mensaje, información)
        """
        current = self._get_current_node()
        if not current or filename not in current.children:
            return False, f"'{filename}' no existe", None
        
        node = current.children[filename]
        
        info = {
            "name": node.name,
            "type": "directory" if node.is_directory else "file",
            "full_path": node.get_full_path(),
            "size": node.size,
            "size_recursive": node.get_size_recursive(),
            "created": node.created_at,
            "modified": node.modified_at,
            "permissions": node.permissions,
            "access_count": node.access_count
        }
        
        return True, f"Información de '{filename}' obtenida", info
    
    def copy_file(self, source: str, destination: str) -> Tuple[bool, str]:
        """
        Copia un archivo.
        
        Args:
            source (str): Nombre del archivo origen
            destination (str): Nombre del archivo destino
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Leer archivo origen
        success, msg, content = self.read_file(source)
        if not success:
            return False, f"Error leyendo archivo origen: {msg}"
        
        # Crear archivo destino
        success, msg = self.create_file(destination, content)
        if not success:
            return False, f"Error creando archivo destino: {msg}"
        
        return True, f"Archivo copiado de '{source}' a '{destination}'"
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas completas del sistema de archivos.
        
        Returns:
            Dict[str, Any]: Estadísticas del sistema
        """
        def count_nodes(node: FileNode) -> Tuple[int, int]:
            """Cuenta archivos y directorios recursivamente."""
            files = 0
            dirs = 0
            
            if node.is_directory:
                dirs += 1
                for child in node.children.values():
                    child_files, child_dirs = count_nodes(child)
                    files += child_files
                    dirs += child_dirs
            else:
                files += 1
            
            return files, dirs
        
        total_files, total_dirs = count_nodes(self.root)
        # Restar 1 del conteo de directorios para no contar la raíz
        total_dirs = max(0, total_dirs - 1)
        
        return {
            "current_directory": self.get_current_directory(),
            "total_files": total_files,
            "total_directories": total_dirs,
            "total_size_bytes": self.root.get_size_recursive(),
            "operations": self.stats.copy(),
            "disk": self.disk.get_disk_stats()
        }

    def search_files(self, pattern: str, search_content: bool = False) -> List[Dict[str, Any]]:
        """
        Busca archivos por nombre o contenido.
        
        Args:
            pattern (str): Patrón de búsqueda
            search_content (bool): Si buscar también en el contenido
            
        Returns:
            List[Dict[str, Any]]: Lista de resultados encontrados
        """
        results = []
        
        def search_recursive(node: FileNode):
            """Busca recursivamente en el árbol."""
            # Buscar en el nombre
            if pattern.lower() in node.name.lower():
                results.append({
                    "path": node.get_full_path(),
                    "type": "directory" if node.is_directory else "file",
                    "match_type": "name"
                })
            
            # Buscar en contenido si es archivo y se solicita
            if search_content and not node.is_directory:
                if pattern.lower() in node.content.lower():
                    results.append({
                        "path": node.get_full_path(),
                        "type": "file",
                        "match_type": "content"
                    })
            
            # Recursión en hijos si es directorio
            if node.is_directory:
                for child in node.children.values():
                    search_recursive(child)
        
        # Iniciar búsqueda desde la raíz
        search_recursive(self.root)
        
        return results
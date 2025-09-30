"""
SISTEMA DE ARCHIVOS SIMULADO - TERMINAL AVANZADA
===============================================

Este módulo implementa un sistema de archivos simulado completo con funcionalidades
de terminal avanzadas. Proporciona una experiencia similar a un sistema de archivos
real con persistencia de datos y comandos de terminal estándar.

Características principales:
- Creación y gestión de directorios y archivos
- Navegación por el sistema de archivos
- Comandos de terminal: ls, cd, cat, mkdir, touch, rm, tree, pwd, find
- Persistencia de datos en formato JSON
- Interfaz de usuario intuitiva con menús organizados
- Manejo de errores y validaciones completas


"""

import os
import json
import datetime
from pathlib import Path


class SistemaArchivosSimulado:
    """
    Simulador completo de sistema de archivos con funcionalidades avanzadas.
    
    Esta clase implementa un sistema de archivos virtual que simula las operaciones
    básicas de un sistema de archivos real, incluyendo:
    
    - Creación y eliminación de archivos y directorios
    - Navegación por la estructura de directorios
    - Listado de contenidos con información detallada
    - Comandos de terminal avanzados (tree, find, pwd)
    - Persistencia de datos mediante archivos JSON
    - Gestión de permisos y metadatos
    
    Attributes:
        directorio_actual (str): Ruta del directorio de trabajo actual
        sistema_archivos (dict): Estructura de datos que representa el sistema de archivos
    """
    
    def __init__(self):
        """
        Inicializar el sistema de archivos simulado.
        
        Configura el estado inicial del sistema creando:
        - Directorio raíz ("/") como punto de partida
        - Estructura de datos para almacenar archivos y directorios
        - Metadatos básicos (permisos, propietario, fechas, tamaños)
        - Carga automática de datos persistentes si existen
        """
        # Establecer el directorio de trabajo inicial
        self.directorio_actual = "/"
        
        # Inicializar la estructura del sistema de archivos con el directorio raíz
        self.sistema_archivos = {
            "/": {
                "tipo": "directorio",
                "contenido": {},
                "permisos": "rwx",
                "propietario": "usuario",
                "fecha_creacion": datetime.datetime.now().isoformat(),
                "tamaño": 0
            }
        }
        
        # Cargar datos persistentes del sistema de archivos
        self.cargar_sistema()
    
    def cargar_sistema(self):
        """
        Cargar el sistema de archivos desde un archivo JSON persistente.
        
        Intenta restaurar el estado previo del sistema de archivos desde
        el archivo 'filesystem_data.json'. Si el archivo existe y es válido,
        restaura tanto la estructura de archivos como el directorio actual.
        
        En caso de error durante la carga (archivo corrupto, permisos, etc.),
        mantiene la configuración por defecto y muestra un mensaje de advertencia.
        
        Raises:
            Exception: Captura cualquier error durante la carga del archivo JSON
        """
        try:
            # Verificar si existe el archivo de datos persistentes
            if os.path.exists("filesystem_data.json"):
                with open("filesystem_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Restaurar la estructura del sistema de archivos
                    self.sistema_archivos = data.get("sistema_archivos", self.sistema_archivos)
                    # Restaurar el directorio de trabajo actual
                    self.directorio_actual = data.get("directorio_actual", "/")
        except Exception as e:
            print(f"⚠️  Error al cargar el sistema: {e}")
    
    def guardar_sistema(self):
        """
        Guardar el estado actual del sistema de archivos en un archivo JSON.
        
        Persiste tanto la estructura completa del sistema de archivos como
        el directorio de trabajo actual en 'filesystem_data.json'. Esto permite
        mantener el estado entre sesiones del programa.
        
        El archivo se guarda con formato JSON indentado y codificación UTF-8
        para facilitar la lectura y depuración si es necesario.
        
        Raises:
            Exception: Captura errores de escritura, permisos o espacio en disco
        """
        try:
            # Preparar los datos para guardar
            data = {
                "sistema_archivos": self.sistema_archivos,
                "directorio_actual": self.directorio_actual
            }
            # Escribir los datos al archivo JSON con formato legible
            with open("filesystem_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Error al guardar el sistema: {e}")
    
    def obtener_ruta_completa(self, ruta):
        """
        Convertir una ruta relativa o absoluta en una ruta completa.
        
        Esta función normaliza las rutas para trabajar consistentemente
        con el sistema de archivos simulado:
        
        - Si la ruta comienza con "/", se considera absoluta y se devuelve tal como está
        - Si la ruta es relativa, se combina con el directorio actual
        - Maneja correctamente el directorio raíz para evitar rutas como "//"
        
        Args:
            ruta (str): Ruta relativa o absoluta a normalizar
            
        Returns:
            str: Ruta completa normalizada
            
        Examples:
            >>> # Con directorio_actual = "/home/usuario"
            >>> obtener_ruta_completa("documentos")  # "/home/usuario/documentos"
            >>> obtener_ruta_completa("/etc/config")  # "/etc/config"
            >>> # Con directorio_actual = "/"
            >>> obtener_ruta_completa("bin")  # "/bin"
        """
        if ruta.startswith("/"):
            # Ruta absoluta - devolver tal como está
            return ruta
        else:
            # Ruta relativa - combinar con directorio actual
            if self.directorio_actual == "/":
                return "/" + ruta
            else:
                return self.directorio_actual + "/" + ruta
    
    def existe_ruta(self, ruta):
        """
        Verificar si una ruta específica existe en el sistema de archivos.
        
        Comprueba la existencia de archivos o directorios en el sistema
        simulado. Acepta tanto rutas relativas como absolutas.
        
        Args:
            ruta (str): Ruta del archivo o directorio a verificar
            
        Returns:
            bool: True si la ruta existe, False en caso contrario
            
        Examples:
            >>> existe_ruta("/home")  # True si existe el directorio /home
            >>> existe_ruta("archivo.txt")  # True si existe en el directorio actual
        """
        ruta_completa = self.obtener_ruta_completa(ruta)
        return ruta_completa in self.sistema_archivos
    
    def crear_directorio(self, nombre):
        """
        Crear un nuevo directorio en el sistema de archivos simulado.
        
        Esta función crea un directorio con todos los metadatos necesarios
        y actualiza la estructura del sistema de archivos. Incluye validaciones
        para evitar duplicados y verificar la existencia del directorio padre.
        
        Args:
            nombre (str): Nombre del directorio a crear (ruta relativa o absoluta)
            
        Returns:
            bool: True si el directorio se creó exitosamente, False en caso contrario
            
        Validaciones realizadas:
        - Verifica que el directorio no exista previamente
        - Confirma que el directorio padre existe
        - Actualiza automáticamente el contenido del directorio padre
        - Guarda los cambios de forma persistente
        
        Examples:
            >>> crear_directorio("documentos")  # Crea en directorio actual
            >>> crear_directorio("/home/usuario/proyectos")  # Ruta absoluta
        """
        ruta_completa = self.obtener_ruta_completa(nombre)
        
        # Verificar si el directorio ya existe
        if self.existe_ruta(nombre):
            print(f"⚠️  El directorio '{nombre}' ya existe")
            return False
        
        # Verificar que el directorio padre existe
        ruta_padre = "/".join(ruta_completa.split("/")[:-1]) or "/"
        if not self.existe_ruta(ruta_padre):
            print(f"⚠️  El directorio padre no existe")
            return False
        
        # Crear la estructura del directorio con metadatos completos
        self.sistema_archivos[ruta_completa] = {
            "tipo": "directorio",
            "contenido": {},
            "permisos": "rwx",
            "propietario": "usuario",
            "fecha_creacion": datetime.datetime.now().isoformat(),
            "tamaño": 0
        }
        
        # Actualizar el contenido del directorio padre
        if ruta_padre in self.sistema_archivos:
            nombre_dir = ruta_completa.split("/")[-1]
            self.sistema_archivos[ruta_padre]["contenido"][nombre_dir] = "directorio"
        
        print(f"✅ Directorio '{nombre}' creado exitosamente")
        self.guardar_sistema()
        return True
    
    def crear_archivo(self, nombre, contenido=""):
        """
        Crear un nuevo archivo en el sistema de archivos simulado.
        
        Esta función crea un archivo con contenido opcional y metadatos completos.
        Incluye validaciones similares a crear_directorio y maneja automáticamente
        el cálculo del tamaño basado en el contenido.
        
        Args:
            nombre (str): Nombre del archivo a crear (ruta relativa o absoluta)
            contenido (str, optional): Contenido inicial del archivo. Por defecto ""
            
        Returns:
            bool: True si el archivo se creó exitosamente, False en caso contrario
            
        Características del archivo creado:
        - Tipo: archivo
        - Permisos: rw- (lectura y escritura)
        - Fechas de creación y modificación automáticas
        - Tamaño calculado automáticamente según el contenido
        - Actualización automática del directorio padre
        
        Examples:
            >>> crear_archivo("readme.txt", "Este es un archivo de prueba")
            >>> crear_archivo("/tmp/config.json", '{"version": "1.0"}')
        """
        ruta_completa = self.obtener_ruta_completa(nombre)
        
        # Verificar si el archivo ya existe
        if self.existe_ruta(nombre):
            print(f"⚠️  El archivo '{nombre}' ya existe")
            return False
        
        # Verificar que el directorio padre existe
        ruta_padre = "/".join(ruta_completa.split("/")[:-1]) or "/"
        if not self.existe_ruta(ruta_padre):
            print(f"⚠️  El directorio padre no existe")
            return False
        
        # Crear la estructura del archivo con metadatos completos
        self.sistema_archivos[ruta_completa] = {
            "tipo": "archivo",
            "contenido": contenido,
            "permisos": "rw-",
            "propietario": "usuario",
            "fecha_creacion": datetime.datetime.now().isoformat(),
            "fecha_modificacion": datetime.datetime.now().isoformat(),
            "tamaño": len(contenido)
        }
        
        # Actualizar el contenido del directorio padre
        if ruta_padre in self.sistema_archivos:
            nombre_archivo = ruta_completa.split("/")[-1]
            self.sistema_archivos[ruta_padre]["contenido"][nombre_archivo] = "archivo"
        
        print(f"✅ Archivo '{nombre}' creado exitosamente")
        self.guardar_sistema()
        return True
    
    def listar_directorio(self, ruta=None):
        """
        Listar el contenido de un directorio con información detallada.
        
        Muestra una lista formateada del contenido de un directorio, similar
        al comando 'ls -l' en sistemas Unix. Incluye información sobre permisos,
        tamaño, fecha de creación y tipo de cada elemento.
        
        Args:
            ruta (str, optional): Ruta del directorio a listar. Si es None,
                                 lista el directorio actual
                                 
        Información mostrada para cada elemento:
        - Tipo: 'd' para directorios, '-' para archivos
        - Permisos: rwx para directorios, rw- para archivos
        - Tamaño: en bytes para archivos, 0 para directorios
        - Fecha: fecha de creación en formato YYYY-MM-DD
        - Nombre: nombre del archivo o directorio
        
        Examples:
            >>> listar_directorio()  # Lista directorio actual
            >>> listar_directorio("/home")  # Lista directorio específico
            
        Output format:
            drwx        0 2024-01-15 documentos
            -rw-      256 2024-01-15 archivo.txt
        """
        # Determinar qué directorio listar
        if ruta is None:
            ruta = self.directorio_actual
        else:
            ruta = self.obtener_ruta_completa(ruta)
        
        # Validar que la ruta existe
        if not self.existe_ruta(ruta):
            print(f"⚠️  El directorio '{ruta}' no existe")
            return
        
        # Validar que es un directorio
        if self.sistema_archivos[ruta]["tipo"] != "directorio":
            print(f"⚠️  '{ruta}' no es un directorio")
            return
        
        # Mostrar encabezado del listado
        print(f"\nContenido de {ruta}:")
        print("-" * 50)
        
        # Obtener el contenido del directorio
        contenido = self.sistema_archivos[ruta]["contenido"]
        if not contenido:
            print("(directorio vacío)")
            return
        
        # Mostrar cada elemento con formato detallado
        for nombre, tipo in contenido.items():
            ruta_item = ruta + "/" + nombre if ruta != "/" else "/" + nombre
            item = self.sistema_archivos.get(ruta_item, {})
            
            # Extraer metadatos del elemento
            fecha = item.get("fecha_creacion", "")[:10] if item.get("fecha_creacion") else ""
            tamaño = item.get("tamaño", 0)
            permisos = item.get("permisos", "---")
            
            # Determinar símbolo de tipo
            tipo_simbolo = "d" if tipo == "directorio" else "-"
            
            # Mostrar línea formateada
            print(f"{tipo_simbolo}{permisos} {tamaño:>8} {fecha} {nombre}")
    
    def cambiar_directorio(self, ruta):
        """
        Cambiar el directorio de trabajo actual.
        
        Implementa la funcionalidad del comando 'cd' permitiendo navegar
        por la estructura de directorios. Soporta rutas absolutas, relativas
        y el directorio padre especial "..".
        
        Args:
            ruta (str): Ruta del directorio destino. Puede ser:
                       - ".." para ir al directorio padre
                       - Ruta absoluta (ej: "/home/usuario")
                       - Ruta relativa (ej: "documentos")
                       
        Funcionalidades especiales:
        - ".." navega al directorio padre
        - Valida que el destino existe y es un directorio
        - Actualiza el directorio actual y guarda el estado
        - Muestra el nuevo directorio actual tras el cambio
        
        Examples:
            >>> cambiar_directorio("documentos")  # Ir a subdirectorio
            >>> cambiar_directorio("..")  # Ir al directorio padre
            >>> cambiar_directorio("/")  # Ir al directorio raíz
        """
        # Manejo especial para directorio padre
        if ruta == "..":
            # Ir al directorio padre
            if self.directorio_actual != "/":
                self.directorio_actual = "/".join(self.directorio_actual.split("/")[:-1]) or "/"
            print(f"Directorio actual: {self.directorio_actual}")
            return
        
        # Obtener ruta completa del destino
        ruta_completa = self.obtener_ruta_completa(ruta)
        
        # Validar que la ruta existe
        if not self.existe_ruta(ruta_completa):
            print(f"⚠️  El directorio '{ruta}' no existe")
            return
        
        # Validar que es un directorio
        if self.sistema_archivos[ruta_completa]["tipo"] != "directorio":
            print(f"⚠️  '{ruta}' no es un directorio")
            return
        
        # Actualizar directorio actual y guardar estado
        self.directorio_actual = ruta_completa
        print(f"Directorio actual: {self.directorio_actual}")
        self.guardar_sistema()
    
    def mostrar_archivo(self, nombre):
        """
        Mostrar el contenido completo de un archivo.
        
        Implementa la funcionalidad del comando 'cat' mostrando todo el
        contenido de un archivo de texto. Incluye validaciones para
        asegurar que el elemento existe y es efectivamente un archivo.
        
        Args:
            nombre (str): Nombre o ruta del archivo a mostrar
            
        Validaciones realizadas:
        - Verifica que el archivo existe
        - Confirma que es un archivo (no un directorio)
        - Muestra el contenido completo con formato
        
        Examples:
            >>> mostrar_archivo("readme.txt")
            >>> mostrar_archivo("/etc/config.json")
            
        Output format:
            Contenido de archivo.txt:
            ------------------------------
            [contenido del archivo aquí]
        """
        ruta_completa = self.obtener_ruta_completa(nombre)
        
        # Validar que el archivo existe
        if not self.existe_ruta(ruta_completa):
            print(f"⚠️  El archivo '{nombre}' no existe")
            return
        
        # Validar que es un archivo
        if self.sistema_archivos[ruta_completa]["tipo"] != "archivo":
            print(f"⚠️  '{nombre}' no es un archivo")
            return
        
        # Mostrar el contenido del archivo
        contenido = self.sistema_archivos[ruta_completa]["contenido"]
        print(f"\nContenido de {nombre}:")
        print("-" * 30)
        print(contenido)
    
    def eliminar_item(self, nombre):
        """
        Eliminar un archivo o directorio del sistema de archivos.
        
        Implementa la funcionalidad del comando 'rm' permitiendo eliminar
        archivos y directorios vacíos. Incluye validaciones de seguridad
        para prevenir eliminaciones accidentales o peligrosas.
        
        Args:
            nombre (str): Nombre o ruta del elemento a eliminar
            
        Validaciones de seguridad:
        - Verifica que el elemento existe
        - Previene la eliminación del directorio raíz
        - Requiere que los directorios estén vacíos antes de eliminarlos
        - Actualiza automáticamente el directorio padre
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
            
        Examples:
            >>> eliminar_item("archivo.txt")  # Eliminar archivo
            >>> eliminar_item("directorio_vacio")  # Eliminar directorio vacío
            
        Restricciones:
        - No se puede eliminar el directorio raíz "/"
        - Los directorios deben estar vacíos para ser eliminados
        """
        ruta_completa = self.obtener_ruta_completa(nombre)
        
        # Validar que el elemento existe
        if not self.existe_ruta(ruta_completa):
            print(f"⚠️  '{nombre}' no existe")
            return False
        
        # Protección: No permitir eliminar el directorio raíz
        if ruta_completa == "/":
            print("⚠️  No se puede eliminar el directorio raíz")
            return False
        
        item = self.sistema_archivos[ruta_completa]
        
        # Validación: Si es un directorio, debe estar vacío
        if item["tipo"] == "directorio" and item["contenido"]:
            print(f"⚠️  El directorio '{nombre}' no está vacío")
            return False
        
        # Eliminar del sistema de archivos
        del self.sistema_archivos[ruta_completa]
        
        # Actualizar el directorio padre removiendo la referencia
        ruta_padre = "/".join(ruta_completa.split("/")[:-1]) or "/"
        if ruta_padre in self.sistema_archivos:
            nombre_item = ruta_completa.split("/")[-1]
            if nombre_item in self.sistema_archivos[ruta_padre]["contenido"]:
                del self.sistema_archivos[ruta_padre]["contenido"][nombre_item]
        
        # Confirmar eliminación y guardar cambios
        tipo = item["tipo"]
        print(f"✅ {tipo.capitalize()} '{nombre}' eliminado exitosamente")
        self.guardar_sistema()
        return True
    
    def obtener_info(self, nombre):
        """
        Obtener información detallada de un archivo o directorio.
        
        Implementa la funcionalidad del comando 'stat' mostrando metadatos
        completos de un elemento del sistema de archivos. Proporciona
        información técnica útil para administración y depuración.
        
        Args:
            nombre (str): Nombre o ruta del elemento a inspeccionar
            
        Información mostrada:
        - Tipo: archivo o directorio
        - Permisos: cadena de permisos (rwx)
        - Propietario: usuario propietario del elemento
        - Tamaño: tamaño en bytes
        - Fecha de creación: timestamp de creación
        - Fecha de modificación: timestamp de última modificación (archivos)
        - Número de elementos: cantidad de elementos (directorios)
        
        Examples:
            >>> obtener_info("documento.txt")
            >>> obtener_info("/home/usuario")
            
        Output format:
            Información de: documento.txt
            ------------------------------
            Tipo: archivo
            Permisos: rw-
            Propietario: usuario
            Tamaño: 1024 bytes
            Fecha creación: 2024-01-15 10:30:45
        """
        ruta_completa = self.obtener_ruta_completa(nombre)
        
        # Validar que el elemento existe
        if not self.existe_ruta(ruta_completa):
            print(f"⚠️  '{nombre}' no existe")
            return
        
        item = self.sistema_archivos[ruta_completa]
        
        # Mostrar información básica
        print(f"\nInformación de: {nombre}")
        print("-" * 30)
        print(f"Tipo: {item['tipo']}")
        print(f"Permisos: {item['permisos']}")
        print(f"Propietario: {item['propietario']}")
        print(f"Tamaño: {item['tamaño']} bytes")
        print(f"Fecha creación: {item['fecha_creacion'][:19]}")
        
        # Información específica para archivos
        if item['tipo'] == 'archivo' and 'fecha_modificacion' in item:
            print(f"Fecha modificación: {item['fecha_modificacion'][:19]}")
        
        # Información específica para directorios
        if item['tipo'] == 'directorio':
            num_items = len(item['contenido'])
            print(f"Elementos: {num_items}")

    def tree(self, ruta=None):
        """
        Mostrar la estructura de directorios en forma de árbol visual.
        
        Implementa la funcionalidad del comando 'tree' creando una
        representación visual jerárquica de la estructura de directorios
        y archivos. Utiliza caracteres especiales para crear un árbol
        gráfico fácil de leer.
        
        Args:
            ruta (str, optional): Ruta del directorio raíz para el árbol.
                                 Si es None, usa el directorio actual
                                 
        Características del árbol:
        - Usa símbolos Unicode para las ramas (├── └──)
        - Ordena elementos: directorios primero, luego archivos
        - Ordenación alfabética dentro de cada tipo
        - Recursivo: muestra toda la jerarquía
        - Formato visual claro y profesional
        
        Examples:
            >>> tree()  # Árbol del directorio actual
            >>> tree("/home")  # Árbol de directorio específico
            
        Output format:
            🌳 Estructura de /home:
            ========================================
            ├── documentos/
            │   ├── archivo1.txt
            │   └── archivo2.txt
            └── imagenes/
                └── foto.jpg
        """
        # Determinar directorio para mostrar
        if ruta is None:
            ruta_mostrar = self.directorio_actual
        else:
            ruta_mostrar = self.obtener_ruta_completa(ruta)
            # Validar que la ruta existe
            if not self.existe_ruta(ruta_mostrar):
                print(f"⚠️  '{ruta}' no existe.")
                return
            
            # Validar que es un directorio
            if self.sistema_archivos[ruta_mostrar]["tipo"] != "directorio":
                print(f"⚠️  '{ruta}' no es un directorio.")
                return
        
        # Mostrar encabezado del árbol
        print(f"\n🌳 Estructura de {ruta_mostrar}:")
        print("=" * 40)
        self._tree_recursivo(ruta_mostrar, "", True)

    def _tree_recursivo(self, ruta, prefijo, es_ultimo):
        """
        Función auxiliar recursiva para generar el árbol de directorios.
        
        Esta función privada maneja la lógica recursiva para crear la
        representación visual del árbol, gestionando los prefijos y
        símbolos apropiados para cada nivel de profundidad.
        
        Args:
            ruta (str): Ruta del directorio actual a procesar
            prefijo (str): Prefijo acumulado para la indentación
            es_ultimo (bool): Si este directorio es el último en su nivel
            
        Lógica de símbolos:
        - "├──" para elementos que no son los últimos
        - "└──" para el último elemento en un nivel
        - "│   " para continuar líneas verticales
        - "    " para espacios en ramas terminadas
        
        Ordenación:
        - Directorios aparecen antes que archivos
        - Ordenación alfabética dentro de cada tipo
        - Recursión automática para subdirectorios
        """
        # Validar que la ruta existe y es un directorio
        if ruta not in self.sistema_archivos:
            return
            
        directorio = self.sistema_archivos[ruta]
        if directorio["tipo"] != "directorio":
            return
        
        # Preparar lista de elementos para mostrar
        elementos = []
        for nombre, tipo in directorio["contenido"].items():
            ruta_elemento = ruta + "/" + nombre if ruta != "/" else "/" + nombre
            elementos.append((nombre, tipo, ruta_elemento))
        
        # Ordenar: directorios primero, luego archivos, alfabéticamente
        elementos.sort(key=lambda x: (x[1] == 'archivo', x[0].lower()))
        
        # Procesar cada elemento
        for i, (nombre, tipo, ruta_elemento) in enumerate(elementos):
            es_ultimo_elemento = i == len(elementos) - 1
            
            # Determinar símbolos para el árbol
            if es_ultimo_elemento:
                print(f"{prefijo}└── {nombre}")
                nuevo_prefijo = prefijo + "    "
            else:
                print(f"{prefijo}├── {nombre}")
                nuevo_prefijo = prefijo + "│   "
            
            # Recursión para subdirectorios
            if tipo == "directorio":
                self._tree_recursivo(ruta_elemento, nuevo_prefijo, False)

    def pwd(self):
        """
        Mostrar el directorio de trabajo actual (Print Working Directory).
        
        Implementa la funcionalidad del comando 'pwd' mostrando la ruta
        completa del directorio actual en el que se encuentra el usuario.
        Es útil para orientarse dentro de la estructura de directorios.
        
        Funcionalidad:
        - Muestra la ruta absoluta del directorio actual
        - Formato visual claro con emoji identificativo
        - No requiere parámetros
        
        Examples:
            >>> pwd()
            📍 Directorio actual: /home/usuario/documentos
            
        Output format:
            📍 Directorio actual: [ruta_completa]
        """
        print(f"\n📍 Directorio actual: {self.directorio_actual}")

    def find(self, patron, tipo=None):
        """
        Buscar archivos y directorios que coincidan con un patrón.
        
        Implementa la funcionalidad del comando 'find' realizando búsquedas
        recursivas en el sistema de archivos. Permite filtrar por tipo de
        elemento y usar patrones de búsqueda flexibles.
        
        Args:
            patron (str): Patrón de búsqueda para nombres de archivos/directorios.
                         Soporta coincidencias parciales (substring matching)
            tipo (str, optional): Filtro por tipo de elemento:
                                 - "archivo": solo buscar archivos
                                 - "directorio": solo buscar directorios
                                 - None: buscar ambos tipos
                                 
        Características de búsqueda:
        - Búsqueda recursiva desde el directorio actual
        - Coincidencia parcial en nombres (case-sensitive)
        - Filtrado opcional por tipo de elemento
        - Muestra rutas completas de los resultados
        - Contador de resultados encontrados
        
        Examples:
            >>> find("txt")  # Buscar elementos que contengan "txt"
            >>> find("config", "archivo")  # Buscar solo archivos con "config"
            >>> find("docs", "directorio")  # Buscar solo directorios con "docs"
            
        Output format:
            🔍 Buscando 'patron'...
               Tipo: archivo
            
            ✅ Encontrados 2 resultado(s):
               /home/usuario/documento.txt
               /home/usuario/notas.txt
        """
        print(f"\n🔍 Buscando '{patron}'...")
        if tipo:
            print(f"   Tipo: {tipo}")
        
        # Inicializar búsqueda recursiva
        resultados = []
        self._find_recursivo(self.directorio_actual, patron, tipo, resultados)
        
        # Mostrar resultados
        if resultados:
            print(f"\n✅ Encontrados {len(resultados)} resultado(s):")
            for resultado in resultados:
                print(f"   {resultado}")
        else:
            print("\n❌ No se encontraron resultados.")

    def _find_recursivo(self, ruta, patron, tipo_filtro, resultados):
        """
        Función auxiliar recursiva para realizar búsquedas en el sistema de archivos.
        
        Esta función privada maneja la lógica recursiva de búsqueda,
        explorando todos los directorios y subdirectorios para encontrar
        elementos que coincidan con el patrón especificado.
        
        Args:
            ruta (str): Ruta del directorio actual a explorar
            patron (str): Patrón de búsqueda para comparar nombres
            tipo_filtro (str): Filtro de tipo ("archivo", "directorio", o None)
            resultados (list): Lista acumulativa de resultados encontrados
            
        Lógica de búsqueda:
        - Explora recursivamente todos los subdirectorios
        - Compara nombres usando coincidencia parcial (substring)
        - Aplica filtros de tipo cuando se especifican
        - Acumula resultados en la lista proporcionada
        - Maneja rutas absolutas correctamente
        
        Algoritmo:
        1. Validar que la ruta existe y es un directorio
        2. Examinar cada elemento en el directorio actual
        3. Aplicar filtros de tipo si están especificados
        4. Verificar coincidencia de patrón en el nombre
        5. Agregar coincidencias a la lista de resultados
        6. Recurrir en subdirectorios para búsqueda profunda
        """
        # Validar que la ruta existe y es un directorio
        if ruta not in self.sistema_archivos:
            return
            
        directorio = self.sistema_archivos[ruta]
        if directorio["tipo"] != "directorio":
            return
        
        # Examinar cada elemento en el directorio
        for nombre, tipo in directorio["contenido"].items():
            ruta_elemento = ruta + "/" + nombre if ruta != "/" else "/" + nombre
            
            # Aplicar filtro de tipo si está especificado
            if tipo_filtro and tipo != tipo_filtro:
                continue
            
            # Verificar coincidencia de patrón (case-insensitive)
            if patron.lower() in nombre.lower():
                resultados.append(ruta_elemento)
            
            # Recursión en subdirectorios para búsqueda profunda
            if tipo == "directorio":
                self._find_recursivo(ruta_elemento, patron, tipo_filtro, resultados)

def ejecutar_filesystem():
    """Menú principal del sistema de archivos simulado"""
    fs = SistemaArchivosSimulado()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("="*70)
        print("SISTEMA DE ARCHIVOS SIMULADO - TERMINAL AVANZADA")
        print("="*70)
        print(f"📍 Directorio actual: {fs.directorio_actual}")
        print("-"*70)
        print("📁 OPERACIONES BÁSICAS:")
        print("1. Listar directorio (ls)")
        print("2. Cambiar directorio (cd)")
        print("3. Crear directorio (mkdir)")
        print("4. Crear archivo (touch)")
        print("5. Mostrar archivo (cat)")
        print("6. Eliminar archivo/directorio (rm)")
        print("7. Información de archivo (stat)")
        print()
        print("🖥️  COMANDOS DE TERMINAL:")
        print("9. Mostrar estructura en árbol (tree)")
        print("10. Mostrar directorio actual (pwd)")
        print("11. Buscar archivos/directorios (find)")
        print()
        print("8. Volver al menú principal")
        print("-"*70)
        
        opcion = input("Seleccione una opción (1-11): ").strip()
        
        if opcion == "1":
            ruta = input("Directorio a listar (Enter para actual): ").strip()
            fs.listar_directorio(ruta if ruta else None)
        
        elif opcion == "2":
            ruta = input("Directorio destino: ").strip()
            if ruta:
                fs.cambiar_directorio(ruta)
        
        elif opcion == "3":
            nombre = input("Nombre del directorio: ").strip()
            if nombre:
                fs.crear_directorio(nombre)
        
        elif opcion == "4":
            nombre = input("Nombre del archivo: ").strip()
            if nombre:
                contenido = input("Contenido inicial (opcional): ")
                fs.crear_archivo(nombre, contenido)
        
        elif opcion == "5":
            nombre = input("Nombre del archivo: ").strip()
            if nombre:
                fs.mostrar_archivo(nombre)
        
        elif opcion == "6":
            nombre = input("Nombre del archivo/directorio: ").strip()
            if nombre:
                confirmacion = input(f"¿Eliminar '{nombre}'? (s/n): ")
                if confirmacion.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                    fs.eliminar_item(nombre)
        
        elif opcion == "7":
            nombre = input("Nombre del archivo/directorio: ").strip()
            if nombre:
                fs.obtener_info(nombre)
        
        elif opcion == "8":
            break
        
        elif opcion == "9":
            ruta = input("Directorio para mostrar árbol (Enter para actual): ").strip()
            fs.tree(ruta if ruta else None)
        
        elif opcion == "10":
            fs.pwd()
        
        elif opcion == "11":
            patron = input("Patrón de búsqueda: ").strip()
            if patron:
                print("\nTipo de elemento a buscar:")
                print("1. Todos")
                print("2. Solo archivos")
                print("3. Solo directorios")
                tipo_opcion = input("Seleccione (1-3): ").strip()
                
                tipo_filtro = None
                if tipo_opcion == "2":
                    tipo_filtro = "archivo"
                elif tipo_opcion == "3":
                    tipo_filtro = "directorio"
                
                fs.find(patron, tipo_filtro)
        
        else:
            print("\n⚠️  Opción no válida. Por favor, seleccione 1-11.")
        
        if opcion != "8":
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    ejecutar_filesystem()
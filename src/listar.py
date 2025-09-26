import psutil
import os

def mostrar_procesos():
    """Función que muestra todos los procesos"""
    print("\n" + "="*50)
    print("  LISTA DE PROCESOS EN EJECUCIÓN   ")
    print("="*50)
    
    for p in psutil.process_iter(['pid', 'name']):
        name = p.info.get('name') or "<sin nombre>"
        print(f"PID: {p.info['pid']:>6} - Nombre: {name}")

def buscar_proceso():
    """Función para buscar procesos por nombre"""
    nombre = input("\nIngrese el nombre del proceso a buscar: ").lower().strip()
    print(f"\nBuscando procesos que contengan: '{nombre}'")
    print("-" * 40)
    
    encontrados = 0
    for p in psutil.process_iter(['pid', 'name']):
        name = (p.info.get('name') or "").lower()
        if nombre in name:
            print(f"PID: {p.info['pid']:>6} - Nombre: {p.info.get('name')}")
            encontrados += 1
    
    print(f"\nSe encontraron {encontrados} procesos")

def main():
    try:
        while True:
            # Limpiar pantalla (funciona en Windows y Linux/Mac)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("="*50)
            print("GESTOR DE PROCESOS DEL SISTEMA")
            print("="*50)
            print("1. Mostrar todos los procesos")
            print("2. Buscar proceso por nombre")
            print("3. Mostrar estadísticas del sistema (pendiente)")
            print("4. Salir")
            print("-"*50)
            
            opcion = input("Seleccione una opción (1-4): ").strip()
            
            if opcion == "1":
                mostrar_procesos()
            elif opcion == "2":
                buscar_proceso()
            elif opcion == "3":
                print("\nFuncionalidad en construcción.")
            elif opcion == "4":
                print("\n¡Hasta luego!")
                break
            else:
                print("\nOpción no válida. Por favor, seleccione 1-4.")
            
            input("\nPresione Enter para continuar...")
    except KeyboardInterrupt:
        print("\n\nInterrupción por teclado. Saliendo...")

if __name__ == "__main__":
    main()

from src.listar import ejecutar_gestor
from src.info import info_proceso
#from src.finalizar import matar_proceso
#from src.iniciar import iniciar_proceso

def mostrar_menu():
    print("\n===============================")
    print("         BIENVENIDO        ")
    print("===============================")
    print("1. Listar procesos")
    print("2. Ver información de un proceso")
    print("3. Matar un proceso")
    print("4. Iniciar un proceso")
    print("5. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-5): ")

        if opcion == "1":
            ejecutar_gestor()
        elif opcion == "2":
            info_proceso()
        elif opcion == "3":
            matar_proceso()
        elif opcion == "4":
            iniciar_proceso()
        elif opcion == "5":
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️  Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()

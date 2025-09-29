import psutil

def info_proceso():
    try:
        pid = int(input("Ingrese el PID del proceso: "))
        p = psutil.Process(pid)
        print("\n=== INFORMACIÓN DEL PROCESO ===")
        print(f"Nombre: {p.name()}")
        print(f"Estado: {p.status()}")
        print(f"Usuario: {p.username()}")
        print(f"CPU %: {p.cpu_percent(interval=0.1)}")
        print(f"Memoria %: {p.memory_percent():.2f}")
    except psutil.NoSuchProcess:
        print("⚠️  No existe un proceso con ese PID.")
    except ValueError:
        print("⚠️  Debe ingresar un número válido.")

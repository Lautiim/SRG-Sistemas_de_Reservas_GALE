import re
import os  # Usamos OS para limpiar la pantalla


# Limpiar a pantalla esta en utils.py


def menu() -> None:
    limpiar_pantalla()
    print("=" * 40)
    print(" SRG - Sistema de Registro de Hotelería ".center(40, " "))
    print("=" * 40)
    print("1. Gestión de Hoteles")
    print("2. Gestión de Clientes")
    print("3. Gestión de Reservas")
    print("4. Gestionar Reportes")
    print("0. Salir")
    print("=" * 40)

# Validar fechas paso a utils.py
# Gestionar Hoteles paso a gestion_hoteles.py
# Gestionar Clientes paso a gestion_clientes.py
# Gestionar Reservas paso a gestion_reservas.py
# Generar Reportes paso a reportes.py


def main() -> None:
    # Función principal que inicia la aplicación
    limpiar_pantalla()
    print("Bienvenido a SRG - Sistema de Registro de Hotelería")

    menu()
    opcion = input("Seleccione una opción: ")

    while True:
        if opcion == "1":
            gestionar_hoteles()
        elif opcion == "2":
            gestionar_clientes()
        elif opcion == "3":
            gestionar_reservas()
        elif opcion == "4":
            generar_reportes()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

        menu()
        opcion = input("Seleccione una opción: ")

if __name__ == "__main__":
    main()

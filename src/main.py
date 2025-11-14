# Importamos los módulos del sistema
import datos
import gestion_hoteles
import gestion_clientes
import gestion_reservas
import reportes
from utils import limpiar_pantalla
import os


# Nuevas importaciones para la estética
from tabulate import tabulate
from colorama import Fore, Style, init


def menu():
    """Función que muestra el menú principal del sistema con formato."""
    limpiar_pantalla()

    # Título
    titulo = " SRG - Sistema de Registro de Hotelería "
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(titulo.center(50, " "))
    print("=" * 50 + Style.RESET_ALL)

    # Datos del menú para tabulate
    menu_data = [
        [Fore.YELLOW + "1" + Style.RESET_ALL, "Gestión de Hoteles"],
        [Fore.YELLOW + "2" + Style.RESET_ALL, "Gestión de Clientes"],
        [Fore.YELLOW + "3" + Style.RESET_ALL, "Gestión de Reservas"],
        [Fore.YELLOW + "4" + Style.RESET_ALL, "Generar Reportes"],
        [Fore.RED + "0" + Style.RESET_ALL, "Salir del Sistema"],
    ]

    # Headers para la tabla
    headers = [Fore.GREEN + "Opción", Fore.GREEN + "Acción" + Style.RESET_ALL]

    # Imprimir la tabla
    print(tabulate(menu_data, headers=headers, tablefmt="heavy_outline"))


def main():
    """Función principal que inicia y controla el flujo del sistema."""
    # Inicializar colorama (autoreset=True reinicia el color después de cada print)
    init(autoreset=True)

    # Se cargan los datos iniciales desde el módulo de datos.
    hoteles, clientes, reservas = datos.cargar_datos()

    print(Fore.CYAN + Style.BRIGHT + "Bienvenido a SRG - Sistema de Registro de Hotelería")
    input(Fore.YELLOW + "Presione Enter para comenzar..." + Style.RESET_ALL)  # Pausa inicial

    while True:
        menu()  # Mostramos el menú
        opcion = input(Fore.GREEN + "\nSeleccione una opción: " + Style.RESET_ALL)

        if opcion == "1":
            # Llamamos a la función principal del módulo de hoteles
            gestion_hoteles.gestionar_hoteles(hoteles, clientes, reservas)
        elif opcion == "2":
            # Hacemos lo mismo para el módulo de clientes.
            gestion_clientes.gestionar_clientes(hoteles, clientes, reservas)
        elif opcion == "3":
            # Y para el módulo de reservas.
            gestion_reservas.gestionar_reservas(hoteles, clientes, reservas)
        elif opcion == "4":
            # Y para el módulo de reportes.
            reportes.generar_reportes(hoteles, clientes, reservas)
        elif opcion == "0":
            limpiar_pantalla()
            print(Fore.CYAN + Style.BRIGHT + "=" * 40)
            print(" Gracias por usar SRG ".center(40, "="))
            print(" Saliendo del sistema... ".center(40, " "))
            print("=" * 40)
            break  # Salimos del bucle y terminamos el programa
        else:
            print(Fore.RED + Style.BRIGHT + "Opción no válida. Intente de nuevo.")
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)


if __name__ == "__main__":
    main()

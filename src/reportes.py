# Importamos funciones necesarias de otros módulos
from datetime import datetime
from utils import limpiar_pantalla, validar_fecha
from gestion_hoteles import consultar_hoteles, buscar_hotel_por_id
from gestion_clientes import consultar_clientes, buscar_cliente_por_id
from gestion_reservas import consultar_reservas
from tabulate import tabulate
from colorama import Fore, Style, init


def buscar_reserva_x_cliente(hoteles: list, clientes: list, reservas: list):
    """Busca y muestra todas las reservas asociadas a un cliente específico por su ID.

    Pre: Recibe la lista de hoteles, clientes y reservas.

    """
    print(
        Fore.CYAN
        + Style.BRIGHT
        + "--- Buscar Reservas por Cliente ---"
        + Style.RESET_ALL
    )
    consultar_clientes(clientes)
    if not clientes:
        print(Fore.YELLOW + "No hay clientes registrados.")
        return

    while True:
        try:
            id_cliente_buscar = int(
                input(
                    Fore.GREEN
                    + "Ingrese el ID del cliente para buscar sus reservas: "
                    + Style.RESET_ALL
                )
            )
            cliente_seleccionado = buscar_cliente_por_id(id_cliente_buscar, clientes)
            if cliente_seleccionado:
                print(
                    Fore.CYAN
                    + f"Buscando reservas para: {cliente_seleccionado['nombre']} (ID: {id_cliente_buscar})"
                    + Style.RESET_ALL
                )
                break
            else:
                print(Fore.RED + "ID de cliente no válido. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    reservas_encontradas = []
    # Encabezados de tabla con color
    headers = [
        Fore.GREEN + "ID Reserva" + Style.RESET_ALL,
        Fore.GREEN + "Hotel" + Style.RESET_ALL,
        Fore.GREEN + "Habitación" + Style.RESET_ALL,
        Fore.GREEN + "Fecha Inicio" + Style.RESET_ALL,
        Fore.GREEN + "Fecha Fin" + Style.RESET_ALL,
    ]

    for reserva in reservas:
        if reserva["id_cliente"] == id_cliente_buscar:
            hotel = buscar_hotel_por_id(reserva["id_hotel"], hoteles)

            if hotel:
                nombre_hotel = hotel["nombre"]
            else:
                # Si el hotel no se encuentra, se muestra el ID en rojo
                nombre_hotel = (
                    Fore.RED
                    + f"ID {reserva['id_hotel']} (No encontrado)"
                    + Style.RESET_ALL
                )

            reservas_encontradas.append(
                [
                    reserva["id"],
                    nombre_hotel,
                    reserva["numero_habitacion"],
                    reserva["fecha_inicio"],
                    reserva["fecha_fin"],
                ]
            )

    if reservas_encontradas:
        print(
            Fore.CYAN
            + f"\nReservas encontradas para {cliente_seleccionado['nombre']}:"
            + Style.RESET_ALL
        )
        print(tabulate(reservas_encontradas, headers=headers, tablefmt="grid"))
    else:
        print(
            Fore.YELLOW
            + f"No se encontraron reservas para el cliente {cliente_seleccionado['nombre']}."
        )


def buscar_reserva_x_hotel(hoteles: list, clientes: list, reservas: list):
    """Función para buscar y mostrar reservas por hotel."""
    print(
        Fore.CYAN + Style.BRIGHT + "--- Buscar Reservas por Hotel ---" + Style.RESET_ALL
    )
    consultar_hoteles(hoteles)
    if not hoteles:
        print(Fore.YELLOW + "No hay hoteles registrados.")
        return

    while True:
        try:
            id_hotel_buscar = int(
                input(
                    Fore.GREEN
                    + "Ingrese el ID del hotel para buscar sus reservas: "
                    + Style.RESET_ALL
                )
            )
            hotel_seleccionado = buscar_hotel_por_id(id_hotel_buscar, hoteles)
            if hotel_seleccionado:
                print(
                    Fore.CYAN
                    + f"Buscando reservas para: {hotel_seleccionado['nombre']} (ID: {id_hotel_buscar})"
                    + Style.RESET_ALL
                )
                break
            else:
                print(Fore.RED + "ID de hotel no válido. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    reservas_encontradas = []
    # Encabezados de tabla con color
    headers = [
        Fore.GREEN + "ID Reserva" + Style.RESET_ALL,
        Fore.GREEN + "Cliente" + Style.RESET_ALL,
        Fore.GREEN + "Habitación" + Style.RESET_ALL,
        Fore.GREEN + "Fecha Inicio" + Style.RESET_ALL,
        Fore.GREEN + "Fecha Fin" + Style.RESET_ALL,
    ]

    for reserva in reservas:
        if reserva["id_hotel"] == id_hotel_buscar:
            cliente = buscar_cliente_por_id(reserva["id_cliente"], clientes)
            if cliente:
                nombre_cliente = cliente["nombre"]
            else:
                # Si el cliente no se encuentra, se muestra el ID en rojo
                nombre_cliente = (
                    Fore.RED
                    + f"ID {reserva['id_cliente']} (No encontrado)"
                    + Style.RESET_ALL
                )

            reservas_encontradas.append(
                [
                    reserva["id"],
                    nombre_cliente,
                    reserva["numero_habitacion"],
                    reserva["fecha_inicio"],
                    reserva["fecha_fin"],
                ]
            )

    if reservas_encontradas:
        print(
            Fore.CYAN
            + f"\nReservas encontradas para {hotel_seleccionado['nombre']}:"
            + Style.RESET_ALL
        )
        print(tabulate(reservas_encontradas, headers=headers, tablefmt="grid"))
    else:
        print(
            Fore.YELLOW
            + f"No se encontraron reservas para el hotel {hotel_seleccionado['nombre']}."
        )


def consultar_habitaciones_disponibles(hoteles: list, reservas: list):
    """Funcion las habitaciones disponibles en un hotel para un rango de fechas."""
    print(
        Fore.CYAN
        + Style.BRIGHT
        + "--- Consultar Habitaciones Disponibles ---"
        + Style.RESET_ALL
    )
    consultar_hoteles(hoteles)
    if not hoteles:
        print(Fore.YELLOW + "No hay hoteles registrados.")
        return

    # Selección de Hotel
    while True:
        try:
            id_hotel_buscar = int(
                input(
                    Fore.GREEN
                    + "Ingrese el ID del hotel para consultar disponibilidad: "
                    + Style.RESET_ALL
                )
            )
            hotel_seleccionado = buscar_hotel_por_id(id_hotel_buscar, hoteles)
            if hotel_seleccionado:
                print(
                    Fore.CYAN
                    + f"Consultando disponibilidad para: {hotel_seleccionado['nombre']} (ID: {id_hotel_buscar})"
                    + Style.RESET_ALL
                )
                break
            else:
                print(Fore.RED + "ID de hotel no válido. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    if not hotel_seleccionado.get("habitaciones"):
        print(
            Fore.YELLOW
            + f"El hotel '{hotel_seleccionado['nombre']}' no tiene habitaciones registradas."
        )
        return

    # Selección de fechas
    while True:
        fecha_inicio_str = input(
            Fore.GREEN
            + "Ingrese la fecha de inicio deseada (AAAA-MM-DD): "
            + Style.RESET_ALL
        )
        if validar_fecha(fecha_inicio_str):
            fecha_inicio_dt = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            if fecha_inicio_dt.date() >= datetime.now().date():
                break
            else:
                print(
                    Fore.RED
                    + "Error: La fecha de inicio no puede ser una fecha pasada."
                )
        else:
            print(Fore.RED + "Formato de fecha incorrecto. Use AAAA-MM-DD.")

    while True:
        fecha_fin_str = input(
            Fore.GREEN
            + "Ingrese la fecha de fin deseada (AAAA-MM-DD): "
            + Style.RESET_ALL
        )
        if validar_fecha(fecha_fin_str):
            fecha_fin_dt = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            if fecha_fin_dt > fecha_inicio_dt:
                break
            else:
                print(
                    Fore.RED
                    + "Error: La fecha de fin debe ser posterior a la fecha de inicio."
                )
        else:
            print(Fore.RED + "Formato de fecha incorrecto. Use AAAA-MM-DD.")

    # Encontrar habitaciones ocupadas en esas fechas
    habitaciones_ocupadas_numeros = set()

    for r in reservas:
        if r["id_hotel"] == id_hotel_buscar:
            reserva_inicio_dt = datetime.strptime(r["fecha_inicio"], "%Y-%m-%d")
            reserva_fin_dt = datetime.strptime(r["fecha_fin"], "%Y-%m-%d")

            if (fecha_inicio_dt < reserva_fin_dt) and (
                fecha_fin_dt > reserva_inicio_dt
            ):
                habitaciones_ocupadas_numeros.add(r["numero_habitacion"])

    # Determinar habitaciones disponibles
    habitaciones_disponibles = []
    todas_las_habitaciones_hotel = hotel_seleccionado.get("habitaciones", [])

    for hab in todas_las_habitaciones_hotel:
        if hab["numero"] not in habitaciones_ocupadas_numeros:
            habitaciones_disponibles.append(hab)

    # Mostrar resultados
    print(
        Fore.CYAN
        + f"\n--- Habitaciones Disponibles en '{hotel_seleccionado['nombre']}' entre {fecha_inicio_str} y {fecha_fin_str} ---"
        + Style.RESET_ALL
    )
    if habitaciones_disponibles:
        headers = [
            Fore.GREEN + "Número" + Style.RESET_ALL,
            Fore.GREEN + "Capacidad" + Style.RESET_ALL,
            Fore.GREEN + "Precio x Noche" + Style.RESET_ALL,
        ]
        tabla_disponibles = [
            [h["numero"], h["capacidad"], f"${h['precio']:.2f}"]
            for h in habitaciones_disponibles
        ]
        print(tabulate(tabla_disponibles, headers=headers, tablefmt="grid"))
    else:
        print(
            Fore.YELLOW + "No hay habitaciones disponibles en las fechas seleccionadas."
        )


def generar_reportes(hoteles: list, clientes: list, reservas: list) -> None:
    """Función principal para interactuar con el menú de generación de reportes (con color en solo los números)."""

    init(autoreset=True)

    while True:
        limpiar_pantalla()

        # Título
        titulo = " --- Generación de Reportes --- "
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print(titulo.center(50, " "))
        print("=" * 50 + Style.RESET_ALL)

        # Datos del menú para tabulate
        menu_data = [
            [Fore.YELLOW + "1" + Style.RESET_ALL, "Listar todos los hoteles"],
            [Fore.YELLOW + "2" + Style.RESET_ALL, "Listar todos los clientes"],
            [Fore.YELLOW + "3" + Style.RESET_ALL, "Listar todas las reservas"],
            [Fore.YELLOW + "4" + Style.RESET_ALL, "Buscar reservas por cliente"],
            [Fore.YELLOW + "5" + Style.RESET_ALL, "Buscar reservas por hotel"],
            [Fore.YELLOW + "6" + Style.RESET_ALL, "Consultar habitaciones disponibles"],
            [Fore.RED + "0" + Style.RESET_ALL, "Volver al menú principal"],
        ]

        # Headers para la tabla
        headers = [
            Fore.GREEN + "Opción" + Style.RESET_ALL,
            Fore.GREEN + "Acción" + Style.RESET_ALL,
        ]

        # Imprimir la tabla
        print(tabulate(menu_data, headers=headers, tablefmt="heavy_outline"))

        opcion = input(Fore.GREEN + "\nSeleccione una opción: " + Style.RESET_ALL)
        limpiar_pantalla()

        if opcion == "1":
            consultar_hoteles(hoteles)
        elif opcion == "2":
            consultar_clientes(clientes)
        elif opcion == "3":
            consultar_reservas(hoteles, clientes, reservas)
        elif opcion == "4":
            buscar_reserva_x_cliente(hoteles, clientes, reservas)
        elif opcion == "5":
            buscar_reserva_x_hotel(hoteles, clientes, reservas)
        elif opcion == "6":
            consultar_habitaciones_disponibles(hoteles, reservas)
        elif opcion == "0":
            break
        else:
            print(Fore.RED + "Opción inválida. Intente de nuevo.")

        input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)


if __name__ == "__main__":
    from datos import cargar_datos

    hoteles, clientes, reservas = cargar_datos()
    generar_reportes(hoteles, clientes, reservas)

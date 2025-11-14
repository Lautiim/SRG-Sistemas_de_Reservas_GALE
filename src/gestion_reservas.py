# Importamos funciones y módulos necesarios
from datetime import datetime
from utils import limpiar_pantalla, validar_fecha
import datos  # Para guardar los cambios
from gestion_clientes import consultar_clientes, buscar_cliente_por_id
from gestion_hoteles import consultar_hoteles, buscar_hotel_por_id
from tabulate import tabulate
from colorama import Fore, Style, init

# Función de validación de disponibilidad


def validar_disponibilidad_habitacion(
    id_hotel: int,
    num_habitacion: int,
    fecha_inicio_dt: datetime,
    fecha_fin_dt: datetime,
    reservas: list,
    hoteles: list,
) -> bool:
    """Valida si una habitacion está disponible (con colores en los errores)."""

    # Verificamos que la habitación exista en el hotel
    hotel = buscar_hotel_por_id(id_hotel, hoteles)
    if not hotel:
        print(Fore.RED + f"Error interno: No se encontró el hotel con ID {id_hotel}.")
        return False

    habitacion_existe = False
    for habitacion in hotel.get("habitaciones", []):
        if habitacion.get("numero") == num_habitacion:
            habitacion_existe = True
            break
    if not habitacion_existe:
        print(
            Fore.RED
            + f"Error: La habitación número {num_habitacion} no existe en el hotel '{hotel['nombre']}'."
        )
        return False

    # Verificamos si hay reservas que se solapen
    for reserva in reservas:
        if reserva["id_hotel"] == id_hotel and reserva["numero_habitacion"] == num_habitacion:
            reserva_inicio_dt = datetime.strptime(reserva["fecha_inicio"], "%Y-%m-%d")
            reserva_fin_dt = datetime.strptime(reserva["fecha_fin"], "%Y-%m-%d")

            if (fecha_inicio_dt < reserva_fin_dt) and (fecha_fin_dt > reserva_inicio_dt):
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + f"Error: La habitación {num_habitacion} ya está reservada entre {reserva['fecha_inicio']} y {reserva['fecha_fin']}."
                )
                return False

    return True


# Funciones principales del módulo


def actualizar_reserva(
    reservas: list,
    hoteles: list,
    clientes: list,
    id_reserva: int,
    id_cliente: int | None = None,
    id_hotel: int | None = None,
    numero_habitacion: int | None = None,
    fecha_inicio: str | None = None,
    fecha_fin: str | None = None,
) -> bool:
    """Actualiza una reserva validando consistencia y disponibilidad.

    - Si se cambian fechas/hotel/habitación, valida disponibilidad.
    - Si se cambia el cliente, valida que exista.
    - Retorna True si actualiza y guarda, False si falla alguna validación.
    """
    res = next((r for r in reservas if r["id"] == id_reserva), None)
    if not res:
        return False

    nuevo_id_cliente = id_cliente if id_cliente is not None else res["id_cliente"]
    if not any(c["id"] == nuevo_id_cliente for c in clientes):
        return False

    nuevo_id_hotel = id_hotel if id_hotel is not None else res["id_hotel"]
    hotel = buscar_hotel_por_id(nuevo_id_hotel, hoteles)
    if not hotel:
        return False

    nuevo_num_hab = numero_habitacion if numero_habitacion is not None else res["numero_habitacion"]
    # validar que la habitación existe en el hotel
    if not any(h.get("numero") == nuevo_num_hab for h in hotel.get("habitaciones", [])):
        return False

    nuevo_inicio = fecha_inicio if fecha_inicio is not None else res["fecha_inicio"]
    nuevo_fin = fecha_fin if fecha_fin is not None else res["fecha_fin"]

    # Validar formato de fechas
    if not (validar_fecha(nuevo_inicio) and validar_fecha(nuevo_fin)):
        return False
    ini_dt = datetime.strptime(nuevo_inicio, "%Y-%m-%d")
    fin_dt = datetime.strptime(nuevo_fin, "%Y-%m-%d")
    if fin_dt <= ini_dt:
        return False

    # Validar disponibilidad excluyendo la propia reserva
    reservas_sin_actual = [r for r in reservas if r["id"] != id_reserva]
    if not validar_disponibilidad_habitacion(
        nuevo_id_hotel, nuevo_num_hab, ini_dt, fin_dt, reservas_sin_actual, hoteles
    ):
        return False

    # aplicar cambios
    res["id_cliente"] = nuevo_id_cliente
    res["id_hotel"] = nuevo_id_hotel
    res["numero_habitacion"] = nuevo_num_hab
    res["fecha_inicio"] = nuevo_inicio
    res["fecha_fin"] = nuevo_fin

    datos.guardar_datos(hoteles, clientes, reservas)
    return True


def agregar_reserva(hoteles: list, clientes: list, reservas: list) -> None:
    """Función para agregar una nueva reserva al sistema."""
    print(Fore.CYAN + Style.BRIGHT + "--- Agregar Reserva ---" + Style.RESET_ALL)

    # Selección de Cliente
    consultar_clientes(clientes)
    if not clientes:
        print(Fore.YELLOW + "No hay clientes registrados. Debe agregar un cliente primero.")
        return
    while True:
        try:
            id_cliente_seleccionado = int(
                input(
                    Fore.GREEN + "\nIngrese el ID del cliente para la reserva: " + Style.RESET_ALL
                )
            )
            cliente_seleccionado = buscar_cliente_por_id(id_cliente_seleccionado, clientes)
            if cliente_seleccionado:
                print(
                    Fore.CYAN
                    + f"Cliente seleccionado: {cliente_seleccionado['nombre']}"
                    + Style.RESET_ALL
                )
                break
            else:
                print(Fore.RED + "ID de cliente no válido. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    # Selección de Hotel
    print("\n")
    consultar_hoteles(hoteles)
    if not hoteles:
        print(Fore.YELLOW + "No hay hoteles registrados. Debe agregar un hotel primero.")
        return
    while True:
        try:
            id_hotel_seleccionado = int(
                input(Fore.GREEN + "\nIngrese el ID del hotel para la reserva: " + Style.RESET_ALL)
            )
            hotel_seleccionado = buscar_hotel_por_id(id_hotel_seleccionado, hoteles)
            if hotel_seleccionado:
                print(
                    Fore.CYAN
                    + f"Hotel seleccionado: {hotel_seleccionado['nombre']}"
                    + Style.RESET_ALL
                )
                break
            else:
                print(Fore.RED + "ID de hotel no válido. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    # Selección de habitación
    print(Fore.CYAN + "\nHabitaciones disponibles en este hotel:" + Style.RESET_ALL)
    if hotel_seleccionado["habitaciones"]:
        headers_hab = [
            Fore.GREEN + "N° Hab" + Style.RESET_ALL,
            Fore.GREEN + "Capacidad" + Style.RESET_ALL,
            Fore.GREEN + "Precio ($)" + Style.RESET_ALL,
        ]
        tabla_hab = [
            [h["numero"], h["capacidad"], f"{h['precio']:.2f}"]
            for h in hotel_seleccionado["habitaciones"]
        ]
        print(tabulate(tabla_hab, headers=headers_hab, tablefmt="grid", stralign="center"))
    else:
        print(Fore.YELLOW + "Este hotel no tiene habitaciones registradas.")
        return

    while True:
        try:
            num_habitacion_seleccionada = int(
                input(
                    Fore.GREEN + "\nIngrese el número de la habitación deseada: " + Style.RESET_ALL
                )
            )
            habitacion_valida = any(
                hab["numero"] == num_habitacion_seleccionada
                for hab in hotel_seleccionado["habitaciones"]
            )
            if habitacion_valida:
                break
            else:
                print(
                    Fore.RED + "Número de habitación no válido para este hotel. Intente de nuevo."
                )
        except ValueError:
            print(Fore.RED + "Error: Ingrese un número válido.")

    # Selección de fechas
    while True:
        fecha_inicio_str = input(
            Fore.GREEN + "Ingrese la fecha de inicio (AAAA-MM-DD): " + Style.RESET_ALL
        )
        if validar_fecha(fecha_inicio_str):
            fecha_inicio_dt = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            break
        else:
            print(Fore.RED + "Formato de fecha incorrecto. Use AAAA-MM-DD.")

    try:
        fecha_limite_dt = fecha_inicio_dt.replace(year=fecha_inicio_dt.year + 1)
    except ValueError:
        fecha_limite_dt = fecha_inicio_dt.replace(year=fecha_inicio_dt.year + 1, day=28)

    while True:
        fecha_fin_str = input(
            Fore.GREEN + "Ingrese la fecha de fin (AAAA-MM-DD): " + Style.RESET_ALL
        )
        if validar_fecha(fecha_fin_str):
            fecha_fin_dt = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            if fecha_fin_dt <= fecha_inicio_dt:
                print(Fore.RED + "Error: La fecha de fin debe ser posterior a la fecha de inicio.")
            elif fecha_fin_dt > fecha_limite_dt:
                print(
                    Fore.RED
                    + f"Error: La reserva no puede exceder un año desde la fecha de inicio."
                )
                print(
                    Fore.RED
                    + f"La fecha de fin máxima permitida es: {fecha_limite_dt.strftime('%Y-%m-%d')}"
                )
            else:
                break
        else:
            print(Fore.RED + "Formato de fecha incorrecto. Use AAAA-MM-DD.")

    # Validar disponibilidad
    if not validar_disponibilidad_habitacion(
        id_hotel_seleccionado,
        num_habitacion_seleccionada,
        fecha_inicio_dt,
        fecha_fin_dt,
        reservas,
        hoteles,
    ):
        return  # Salimos si no está disponible

    # Crear y guardar reserva
    if reservas:
        id_reserva = reservas[-1]["id"] + 1
    else:
        id_reserva = 1

    nueva_reserva = {
        "id": id_reserva,
        "id_cliente": id_cliente_seleccionado,
        "id_hotel": id_hotel_seleccionado,
        "numero_habitacion": num_habitacion_seleccionada,
        "fecha_inicio": fecha_inicio_str,
        "fecha_fin": fecha_fin_str,
    }
    reservas.append(nueva_reserva)
    datos.guardar_datos(hoteles, clientes, reservas)
    print(Fore.GREEN + Style.BRIGHT + "\n¡Reserva agregada correctamente!" + Style.RESET_ALL)


def consultar_reservas(hoteles, clientes, reservas):
    """Función para mostrar todas las reservas existentes."""
    print(Fore.CYAN + Style.BRIGHT + "--- Reservas Existentes ---" + Style.RESET_ALL)
    if reservas:
        reservas_para_tabla = []
        headers = [
            Fore.GREEN + "ID",
            Fore.GREEN + "Cliente",
            Fore.GREEN + "Hotel",
            Fore.GREEN + "Habitación",
            Fore.GREEN + "Fecha Inicio",
            Fore.GREEN + "Fecha Fin" + Style.RESET_ALL,
        ]

        for reserva in reservas:
            cliente = buscar_cliente_por_id(reserva["id_cliente"], clientes)
            # Si el cliente fue eliminado, mostramos el ID en rojo
            nombre_cliente = (
                cliente["nombre"]
                if cliente
                else (Fore.RED + f"ID {reserva['id_cliente']} (Eliminado)" + Style.RESET_ALL)
            )

            hotel = buscar_hotel_por_id(reserva["id_hotel"], hoteles)
            # Si el hotel fue eliminado, mostramos el ID en rojo
            nombre_hotel = (
                hotel["nombre"]
                if hotel
                else (Fore.RED + f"ID {reserva['id_hotel']} (Eliminado)" + Style.RESET_ALL)
            )

            reservas_para_tabla.append(
                [
                    reserva["id"],
                    nombre_cliente,
                    nombre_hotel,
                    reserva["numero_habitacion"],
                    reserva["fecha_inicio"],
                    reserva["fecha_fin"],
                ]
            )

        # Mostramos la tabla
        print(tabulate(reservas_para_tabla, headers=headers, tablefmt="grid"))
    else:
        print(Fore.YELLOW + "No hay reservas registradas.")


def modificar_reserva(hoteles: list, clientes: list, reservas: list) -> None:
    """Interfaz interactiva para modificar una reserva existente."""
    print(Fore.CYAN + Style.BRIGHT + "--- Modificar Reserva ---" + Style.RESET_ALL)
    consultar_reservas(hoteles, clientes, reservas)
    if not reservas:
        return

    while True:
        try:
            id_mod = int(
                input(Fore.GREEN + "\nIngrese el ID de la reserva a modificar: " + Style.RESET_ALL)
            )
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    res = next((r for r in reservas if r["id"] == id_mod), None)
    if not res:
        print(Fore.RED + f"No se encontró reserva con ID {id_mod}.")
        return

    print(
        Fore.CYAN
        + f"Editando Reserva {res['id']} (Cliente {res['id_cliente']}, Hotel {res['id_hotel']}, Hab {res['numero_habitacion']}, {res['fecha_inicio']} a {res['fecha_fin']})"
        + Style.RESET_ALL
    )

    # Cliente
    nuevo_id_cliente_str = input(
        Fore.GREEN + f"Nuevo ID cliente [{res['id_cliente']}] (Enter = dejar): " + Style.RESET_ALL
    ).strip()
    nuevo_id_cliente = int(nuevo_id_cliente_str) if nuevo_id_cliente_str.isdigit() else None

    # Hotel y habitación
    nuevo_id_hotel_str = input(
        Fore.GREEN + f"Nuevo ID hotel [{res['id_hotel']}] (Enter = dejar): " + Style.RESET_ALL
    ).strip()
    nuevo_id_hotel = int(nuevo_id_hotel_str) if nuevo_id_hotel_str.isdigit() else None

    # si cambia el hotel, mostrar habitaciones del nuevo hotel
    if nuevo_id_hotel is not None:
        hotel_sel = buscar_hotel_por_id(nuevo_id_hotel, hoteles)
        if not hotel_sel:
            print(Fore.RED + "ID de hotel no válido.")
            return
        print(Fore.CYAN + "Habitaciones del nuevo hotel:" + Style.RESET_ALL)
        if hotel_sel.get("habitaciones"):
            headers = [
                Fore.GREEN + "N° Hab" + Style.RESET_ALL,
                Fore.GREEN + "Capacidad" + Style.RESET_ALL,
                Fore.GREEN + "Precio ($)" + Style.RESET_ALL,
            ]
            tabla = [
                [h["numero"], h["capacidad"], f"{h['precio']:.2f}"]
                for h in hotel_sel["habitaciones"]
            ]
            print(tabulate(tabla, headers=headers, tablefmt="grid"))
        else:
            print(Fore.YELLOW + "El hotel no tiene habitaciones registradas.")

    nuevo_num_hab_str = input(
        Fore.GREEN
        + f"Nuevo N° habitación [{res['numero_habitacion']}] (Enter = dejar): "
        + Style.RESET_ALL
    ).strip()
    nuevo_num_hab = int(nuevo_num_hab_str) if nuevo_num_hab_str.isdigit() else None

    # Fechas
    nuevo_inicio = input(
        Fore.GREEN
        + f"Nueva fecha inicio [{res['fecha_inicio']}] (AAAA-MM-DD, Enter = dejar): "
        + Style.RESET_ALL
    ).strip()
    nuevo_fin = input(
        Fore.GREEN
        + f"Nueva fecha fin [{res['fecha_fin']}] (AAAA-MM-DD, Enter = dejar): "
        + Style.RESET_ALL
    ).strip()

    inicio_val = nuevo_inicio if nuevo_inicio != "" else None
    fin_val = nuevo_fin if nuevo_fin != "" else None

    ok = actualizar_reserva(
        reservas,
        hoteles,
        clientes,
        id_mod,
        id_cliente=nuevo_id_cliente,
        id_hotel=nuevo_id_hotel,
        numero_habitacion=nuevo_num_hab,
        fecha_inicio=inicio_val,
        fecha_fin=fin_val,
    )
    if ok:
        print(Fore.GREEN + Style.BRIGHT + "Reserva actualizada correctamente.")
    else:
        print(
            Fore.RED
            + "No se pudo actualizar (validaciones de cliente/hotel/habitación/fechas o disponibilidad)."
        )


def eliminar_reserva(hoteles: list, clientes: list, reservas: list) -> None:
    """Elimina una reserva de la lista por su ID y guarda los cambios."""
    print(Fore.CYAN + Style.BRIGHT + "--- Eliminar Reserva ---" + Style.RESET_ALL)
    consultar_reservas(hoteles, clientes, reservas)

    if not reservas:
        # El mensaje de "No hay reservas" ya lo da consultar_reservas
        return

    while True:
        try:
            id_a_eliminar = int(
                input(
                    Fore.GREEN
                    + "\nIngrese el ID de la reserva que desea eliminar: "
                    + Style.RESET_ALL
                )
            )
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    reserva_encontrada = None
    indice_reserva = -1

    for i, reserva in enumerate(reservas):
        if reserva["id"] == id_a_eliminar:
            reserva_encontrada = reserva
            indice_reserva = i
            break

    if reserva_encontrada:
        cliente = buscar_cliente_por_id(reserva_encontrada["id_cliente"], clientes)
        hotel = buscar_hotel_por_id(reserva_encontrada["id_hotel"], hoteles)
        nombre_cliente = (
            cliente["nombre"]
            if cliente
            else (Fore.RED + "Cliente Desconocido/Eliminado" + Style.RESET_ALL)
        )
        nombre_hotel = (
            hotel["nombre"]
            if hotel
            else (Fore.RED + "Hotel Desconocido/Eliminado" + Style.RESET_ALL)
        )

        print(Fore.YELLOW + f"\nReserva a eliminar:")
        print(f"  Cliente: {nombre_cliente}")
        print(f"  Hotel: {nombre_hotel}")
        print(f"  Habitación: {reserva_encontrada['numero_habitacion']}")
        print(f"  Fechas: {reserva_encontrada['fecha_inicio']} a {reserva_encontrada['fecha_fin']}")

        confirmacion = input(
            Fore.RED
            + Style.BRIGHT
            + f"\n¿Está seguro que desea eliminar esta reserva (ID: {id_a_eliminar})? (s/n): "
            + Style.RESET_ALL
        )
        if confirmacion.lower() == "s":
            reservas.pop(indice_reserva)
            datos.guardar_datos(hoteles, clientes, reservas)
            print(Fore.GREEN + Style.BRIGHT + "Reserva eliminada correctamente.")
        else:
            print(Fore.YELLOW + "Eliminación cancelada.")
    else:
        print(Fore.RED + f"No se encontró ninguna reserva con el ID {id_a_eliminar}.")


def gestionar_reservas(hoteles, clientes, reservas):
    """Función principal para interactuar con el menú de gestión de reservas."""

    # Inicializamos colorama para este módulo
    init(autoreset=True)

    while True:
        limpiar_pantalla()

        # Título
        titulo = " --- Gestión de Reservas --- "
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print(titulo.center(50, " "))
        print("=" * 50 + Style.RESET_ALL)

        # Datos del menú para tabulate
        menu_data = [
            [Fore.YELLOW + "1" + Style.RESET_ALL, "Agregar Reserva"],
            [Fore.YELLOW + "2" + Style.RESET_ALL, "Consultar Reservas"],
            [Fore.YELLOW + "3" + Style.RESET_ALL, "Eliminar Reserva"],
            [Fore.YELLOW + "4" + Style.RESET_ALL, "Modificar Reserva"],
            [Fore.RED + "0" + Style.RESET_ALL, "Volver al menú principal"],
        ]

        # Headers para la tabla
        headers = [Fore.GREEN + "Opción", Fore.GREEN + "Acción" + Style.RESET_ALL]

        # Imprimir la tabla
        print(tabulate(menu_data, headers=headers, tablefmt="heavy_outline"))

        opcion = input(Fore.GREEN + "\nSeleccione una opción: " + Style.RESET_ALL)

        if opcion == "1":
            limpiar_pantalla()
            agregar_reserva(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "2":
            limpiar_pantalla()
            consultar_reservas(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "3":
            limpiar_pantalla()
            eliminar_reserva(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "4":
            limpiar_pantalla()
            modificar_reserva(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "0":
            break
        else:
            print(Fore.RED + "Opción inválida. Intente de nuevo.")
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

import datos  # Importamos el módulo completo para acceder a guardar_datos
from utils import limpiar_pantalla
from tabulate import tabulate
from colorama import Fore, Style, init


def buscar_hotel_por_id(id_hotel: int, hoteles: list) -> dict | None:
    """Función para buscar un hotel por su ID."""
    for hotel in hoteles:
        if hotel["id"] == id_hotel:
            return hotel
    return None


def agregar_hotel(hoteles, clientes, reservas) -> None:
    """Funcion para agregar un nuevo hotel a la lista de hoteles y guarda los cambios."""

    print(Fore.CYAN + Style.BRIGHT + "--- Agregar Hotel ---" + Style.RESET_ALL)
    nombre_hotel = input(Fore.GREEN + "Ingrese el nombre del hotel: " + Style.RESET_ALL)
    nombre_hotel = nombre_hotel.lower().title()
    ubicacion = input(
        Fore.GREEN + "Ingrese la ciudad donde se encuentra el hotel: " + Style.RESET_ALL
    )

    lista_habitaciones = []

    while True:
        try:
            num_habitaciones_a_agregar = int(
                input(
                    Fore.GREEN
                    + "¿Cuántas habitaciones desea agregar a este hotel?: "
                    + Style.RESET_ALL
                )
            )
            if num_habitaciones_a_agregar < 0:
                print(Fore.RED + "Por favor, ingrese un número positivo.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un número válido.")

    for i in range(num_habitaciones_a_agregar):
        print(Fore.CYAN + f"\n--- Agregando Habitación {i+1} ---" + Style.RESET_ALL)

        # Número de la habitación
        while True:
            try:
                numero = int(
                    input(Fore.GREEN + f"Número de la habitación {i+1}: " + Style.RESET_ALL)
                )
                if any(h["numero"] == numero for h in lista_habitaciones):
                    print(
                        Fore.RED
                        + f"Error: Ya existe una habitación con el número {numero} en este hotel."
                    )
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un número válido.")

        # Capacidad de la habitación
        while True:
            try:
                capacidad = int(
                    input(Fore.GREEN + f"Capacidad de la habitación {numero}: " + Style.RESET_ALL)
                )
                if capacidad <= 0:
                    print(Fore.RED + "La capacidad debe ser mayor a cero.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un número válido.")

        # Precio por noche
        while True:
            try:
                precio = float(
                    input(
                        Fore.GREEN
                        + f"Precio por noche de la habitación {numero}: "
                        + Style.RESET_ALL
                    )
                )
                if precio <= 0:
                    print(Fore.RED + "El precio debe ser mayor a cero.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Error: Ingrese un número válido.")

        lista_habitaciones.append({"numero": numero, "capacidad": capacidad, "precio": precio})

    # Calculamos el próximo ID disponible
    if hoteles:
        id_hotel = max(h["id"] for h in hoteles) + 1
    else:
        id_hotel = 1

    nuevo_hotel = {
        "id": id_hotel,
        "nombre": nombre_hotel,
        "ubicacion": ubicacion,
        "habitaciones": lista_habitaciones,
    }
    hoteles.append(nuevo_hotel)

    datos.guardar_datos(hoteles, clientes, reservas)
    print(Fore.GREEN + Style.BRIGHT + "\n¡Hotel agregado correctamente!" + Style.RESET_ALL)


def actualizar_hotel(
    hoteles: list,
    id_hotel: int,
    *,
    clientes: list | None = None,
    reservas: list | None = None,
    nombre: str | None = None,
    ubicacion: str | None = None,
) -> bool:
    """Actualiza campos básicos del hotel (nombre, ubicación)."""
    hotel = buscar_hotel_por_id(id_hotel, hoteles)
    if not hotel:
        return False
    if nombre is not None and nombre != "":
        hotel["nombre"] = nombre
    if ubicacion is not None and ubicacion != "":
        hotel["ubicacion"] = ubicacion

    if clientes is not None and reservas is not None:
        datos.guardar_datos(hoteles, clientes, reservas)
    return True


def consultar_hoteles(hoteles: list) -> None:
    """Funcion para mostrar la lista de hoteles registrados."""
    print(Fore.CYAN + Style.BRIGHT + "--- Hoteles Registrados ---" + Style.RESET_ALL)
    if hoteles:
        for hotel in hoteles:
            # Imprimimos la cabecera del hotel
            print(
                Fore.CYAN
                + Style.BRIGHT
                + f"\nID: {hotel['id']} | Nombre: {hotel['nombre']} | Ubicación: {hotel['ubicacion']}"
                + Style.RESET_ALL
            )

            if hotel["habitaciones"]:
                # Preparamos los datos y cabeceras para tabulate
                headers = [
                    Fore.GREEN + "N° Hab" + Style.RESET_ALL,
                    Fore.GREEN + "Capacidad" + Style.RESET_ALL,
                    Fore.GREEN + "Precio ($)" + Style.RESET_ALL,
                ]
                tabla_hab = [
                    [h["numero"], h["capacidad"], f"{h['precio']:.2f}"]
                    for h in hotel["habitaciones"]
                ]
                # Imprimimos la tabla de habitaciones
                print(tabulate(tabla_hab, headers=headers, tablefmt="grid", stralign="center"))
            else:
                print(Fore.YELLOW + "  El hotel no tiene habitaciones registradas.")
    else:
        print(Fore.YELLOW + "No hay hoteles registrados.")


def modificar_hotel(hoteles: list, clientes: list, reservas: list) -> None:
    """Interfaz interactiva para modificar datos básicos de un hotel."""
    print(Fore.CYAN + Style.BRIGHT + "--- Modificar Hotel ---" + Style.RESET_ALL)
    consultar_hoteles(hoteles)
    if not hoteles:
        return

    while True:
        try:
            id_mod = int(
                input(Fore.GREEN + "\nIngrese el ID del hotel a modificar: " + Style.RESET_ALL)
            )
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    hotel = buscar_hotel_por_id(id_mod, hoteles)
    if not hotel:
        print(Fore.RED + f"No se encontró hotel con ID {id_mod}.")
        return

    print(
        Fore.CYAN
        + f"Editando: {hotel['nombre']} (Ubicación: {hotel.get('ubicacion', 'N/A')})"
        + Style.RESET_ALL
    )
    nuevo_nombre = input(
        Fore.GREEN + f"Nuevo nombre [{hotel['nombre']}] (Enter = dejar): " + Style.RESET_ALL
    ).strip()
    nueva_ubicacion = input(
        Fore.GREEN
        + f"Nueva ubicación [{hotel.get('ubicacion', '')}] (Enter = dejar): "
        + Style.RESET_ALL
    ).strip()

    ok = actualizar_hotel(
        hoteles,
        id_mod,
        clientes=clientes,
        reservas=reservas,
        nombre=(nuevo_nombre if nuevo_nombre != "" else None),
        ubicacion=(nueva_ubicacion if nueva_ubicacion != "" else None),
    )
    if ok:
        print(Fore.GREEN + Style.BRIGHT + "Hotel actualizado correctamente.")
    else:
        print(Fore.RED + "No se pudo actualizar (ID inválido).")


def agregar_habitacion_a_hotel(
    hoteles: list,
    id_hotel: int,
    numero: int,
    capacidad: int,
    precio: float,
    *,
    clientes: list | None = None,
    reservas: list | None = None,
) -> bool:
    """Agrega una habitación al hotel indicado si el número no existe.

    Retorna True si se agregó, False si el hotel no existe o el número ya está en uso.
    """
    hotel = buscar_hotel_por_id(id_hotel, hoteles)
    if not hotel:
        return False
    if any(h.get("numero") == numero for h in hotel.get("habitaciones", [])):
        return False
    if capacidad <= 0 or precio <= 0:
        return False
    hotel.setdefault("habitaciones", []).append(
        {"numero": int(numero), "capacidad": int(capacidad), "precio": float(precio)}
    )
    if clientes is not None and reservas is not None:
        datos.guardar_datos(hoteles, clientes, reservas)
    return True


def actualizar_habitacion_de_hotel(
    hoteles: list,
    id_hotel: int,
    numero: int,
    *,
    capacidad: int | None = None,
    precio: float | None = None,
    clientes: list | None = None,
    reservas: list | None = None,
) -> bool:
    """Actualiza capacidad y/o precio de una habitación existente en un hotel.

    No cambia el número de habitación para evitar inconsistencias con reservas.
    Retorna True si actualizó, False en caso contrario.
    """
    hotel = buscar_hotel_por_id(id_hotel, hoteles)
    if not hotel:
        return False
    for hab in hotel.get("habitaciones", []):
        if hab.get("numero") == numero:
            if capacidad is not None:
                if capacidad <= 0:
                    return False
                hab["capacidad"] = int(capacidad)
            if precio is not None:
                if precio <= 0:
                    return False
                hab["precio"] = float(precio)
            if clientes is not None and reservas is not None:
                datos.guardar_datos(hoteles, clientes, reservas)
            return True
    return False


def eliminar_habitacion_de_hotel(
    hoteles: list,
    id_hotel: int,
    numero: int,
    *,
    clientes: list | None = None,
    reservas: list | None = None,
) -> bool:
    """Elimina una habitación de un hotel si no tiene reservas asociadas.

    Retorna True si elimina. Retorna False si no existe el hotel/habitación
    o si hay reservas que referencian esa habitación.
    """
    hotel = buscar_hotel_por_id(id_hotel, hoteles)
    if not hotel:
        return False

    # Verificar existencia de la habitación
    idx = -1
    for i, hab in enumerate(hotel.get("habitaciones", [])):
        if hab.get("numero") == numero:
            idx = i
            break
    if idx == -1:
        return False

    # Si hay reservas, no permitir eliminar
    if reservas is not None:
        tiene_reservas = any(
            r
            for r in reservas
            if r.get("id_hotel") == id_hotel and r.get("numero_habitacion") == numero
        )
        if tiene_reservas:
            return False

    # Eliminar y guardar
    hotel["habitaciones"].pop(idx)
    if clientes is not None and reservas is not None:
        datos.guardar_datos(hoteles, clientes, reservas)
    return True


def modificar_habitaciones_hotel(hoteles: list, clientes: list, reservas: list) -> None:
    """Interfaz para agregar o modificar habitaciones de un hotel."""
    print(Fore.CYAN + Style.BRIGHT + "--- Modificar Habitaciones de un Hotel ---" + Style.RESET_ALL)
    consultar_hoteles(hoteles)
    if not hoteles:
        return

    # Seleccionar hotel
    while True:
        try:
            id_hotel = int(
                input(
                    Fore.GREEN
                    + "\nIngrese el ID del hotel a editar habitaciones: "
                    + Style.RESET_ALL
                )
            )
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    hotel = buscar_hotel_por_id(id_hotel, hoteles)
    if not hotel:
        print(Fore.RED + f"No se encontró hotel con ID {id_hotel}.")
        return

    print(
        Fore.CYAN
        + f"Editando habitaciones de: {hotel['nombre']} (ID {hotel['id']})"
        + Style.RESET_ALL
    )

    # Submenú
    print(
        tabulate(
            [
                [Fore.YELLOW + "1" + Style.RESET_ALL, "Agregar habitación"],
                [Fore.YELLOW + "2" + Style.RESET_ALL, "Modificar habitación existente"],
                [Fore.YELLOW + "3" + Style.RESET_ALL, "Eliminar habitación"],
                [Fore.RED + "0" + Style.RESET_ALL, "Volver"],
            ],
            headers=[
                Fore.GREEN + "Opción" + Style.RESET_ALL,
                Fore.GREEN + "Acción" + Style.RESET_ALL,
            ],
            tablefmt="heavy_outline",
        )
    )

    opcion = input(Fore.GREEN + "\nSeleccione una opción: " + Style.RESET_ALL).strip()

    if opcion == "1":
        # Agregar
        try:
            numero = int(input(Fore.GREEN + "Número de habitación nueva: " + Style.RESET_ALL))
            capacidad = int(input(Fore.GREEN + "Capacidad: " + Style.RESET_ALL))
            precio = float(input(Fore.GREEN + "Precio por noche: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Valores inválidos. Operación cancelada.")
            return
        if agregar_habitacion_a_hotel(
            hoteles, id_hotel, numero, capacidad, precio, clientes=clientes, reservas=reservas
        ):
            print(Fore.GREEN + Style.BRIGHT + "Habitación agregada correctamente.")
        else:
            print(
                Fore.RED + "No se pudo agregar (ID inválido, número duplicado o valores inválidos)."
            )

    elif opcion == "2":
        # Modificar existente
        try:
            numero = int(input(Fore.GREEN + "Número de habitación a modificar: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Número inválido.")
            return

        # Buscar datos actuales
        hab_actual = next(
            (h for h in hotel.get("habitaciones", []) if h.get("numero") == numero), None
        )
        if not hab_actual:
            print(Fore.RED + "No existe esa habitación en el hotel.")
            return
        print(
            Fore.CYAN
            + f"Actual: Capacidad {hab_actual['capacidad']} | Precio {hab_actual['precio']:.2f}"
            + Style.RESET_ALL
        )

        cap_str = input(Fore.GREEN + "Nueva capacidad (Enter = dejar): " + Style.RESET_ALL).strip()
        precio_str = input(Fore.GREEN + "Nuevo precio (Enter = dejar): " + Style.RESET_ALL).strip()

        cap_val = int(cap_str) if cap_str.isdigit() else None
        precio_val = None
        if precio_str != "":
            try:
                precio_val = float(precio_str)
            except ValueError:
                print(Fore.RED + "Precio inválido.")
                return

        if actualizar_habitacion_de_hotel(
            hoteles,
            id_hotel,
            numero,
            capacidad=cap_val,
            precio=precio_val,
            clientes=clientes,
            reservas=reservas,
        ):
            print(Fore.GREEN + Style.BRIGHT + "Habitación actualizada correctamente.")
        else:
            print(Fore.RED + "No se pudo actualizar (ID inválido o valores inválidos).")

    elif opcion == "3":
        # Eliminar habitación
        try:
            numero = int(input(Fore.GREEN + "Número de habitación a eliminar: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "Número inválido.")
            return

        if eliminar_habitacion_de_hotel(
            hoteles, id_hotel, numero, clientes=clientes, reservas=reservas
        ):
            print(Fore.GREEN + Style.BRIGHT + "Habitación eliminada correctamente.")
        else:
            print(
                Fore.RED
                + "No se pudo eliminar (ID inválido, habitación inexistente o tiene reservas asociadas)."
            )

    else:
        # Volver u opción inválida
        if opcion != "0":
            print(Fore.YELLOW + "Opción no válida. Volviendo...")


def eliminar_hotel(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para eliminar un hotel de la lista por su ID o nombre y guardar los cambios."""
    print(Fore.CYAN + Style.BRIGHT + "--- Eliminar Hotel ---" + Style.RESET_ALL)
    consultar_hoteles(hoteles)

    if not hoteles:
        # El mensaje de "No hay hoteles" ya lo da consultar_hoteles
        return

    entrada = input(
        Fore.GREEN + "\nIngrese el ID o el nombre del hotel que desea eliminar: " + Style.RESET_ALL
    )
    if not entrada:
        print(Fore.RED + "Entrada vacía. Operación cancelada.")
        return

    hotel_encontrado = None

    try:
        id_a_eliminar = int(entrada)
        hotel_encontrado = buscar_hotel_por_id(id_a_eliminar, hoteles)
        if not hotel_encontrado:
            print(Fore.RED + f"No se encontró ningún hotel con el ID {id_a_eliminar}.")
            return
    except ValueError:
        nombre_buscar = entrada.lower()
        coincidencias = [h for h in hoteles if h["nombre"].lower() == nombre_buscar]

        if len(coincidencias) == 0:
            print(Fore.RED + f"No se encontró ningún hotel con el nombre '{entrada}'.")
            return
        elif len(coincidencias) == 1:
            hotel_encontrado = coincidencias[0]
        else:
            print(
                Fore.YELLOW
                + f"Se encontraron {len(coincidencias)} hoteles con el nombre '{entrada}':"
                + Style.RESET_ALL
            )
            for h in coincidencias:
                print(
                    f"  ID: {h['id']} | Nombre: {h['nombre']} | Ubicación: {h.get('ubicacion', 'N/A')}"
                )

            while True:
                try:
                    id_elegido = int(
                        input(
                            Fore.GREEN
                            + "Ingrese el ID del hotel que desea eliminar de las opciones anteriores: "
                            + Style.RESET_ALL
                        )
                    )
                except ValueError:
                    print(Fore.RED + "Error: Ingrese un ID numérico válido.")
                    continue

                hotel_encontrado = next((h for h in coincidencias if h["id"] == id_elegido), None)

                if hotel_encontrado:
                    break
                else:
                    print(Fore.RED + "ID no válido. Elija un ID de la lista mostrada.")

    # Confirmación
    confirmacion = input(
        Fore.RED
        + Style.BRIGHT
        + f"\n¿Está seguro que desea eliminar el hotel '{hotel_encontrado['nombre']}' (ID: {hotel_encontrado['id']})? (s/n): "
        + Style.RESET_ALL
    )
    if confirmacion.lower() == "s":
        hoteles.remove(hotel_encontrado)
        datos.guardar_datos(hoteles, clientes, reservas)
        print(Fore.GREEN + Style.BRIGHT + "Hotel eliminado correctamente.")
    else:
        print(Fore.YELLOW + "Eliminación cancelada.")


def gestionar_hoteles(hoteles: list, clientes: list, reservas: list) -> None:
    """Función principal para interactuar con el menú de gestión de hoteles."""

    # Inicializamos colorama para este módulo
    init(autoreset=True)

    while True:
        limpiar_pantalla()

        # Título
        titulo = " --- Gestión de Hoteles --- "
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print(titulo.center(50, " "))
        print("=" * 50 + Style.RESET_ALL)

        # Datos del menú para tabulate
        menu_data = [
            [Fore.YELLOW + "1" + Style.RESET_ALL, "Agregar Hotel"],
            [Fore.YELLOW + "2" + Style.RESET_ALL, "Consultar Hoteles"],
            [Fore.YELLOW + "3" + Style.RESET_ALL, "Eliminar Hotel"],
            [Fore.YELLOW + "4" + Style.RESET_ALL, "Modificar Hotel"],
            [Fore.YELLOW + "5" + Style.RESET_ALL, "Modificar Habitaciones"],
            [Fore.RED + "0" + Style.RESET_ALL, "Volver al menú principal"],
        ]

        # Headers para la tabla
        headers = [Fore.GREEN + "Opción", Fore.GREEN + "Acción" + Style.RESET_ALL]

        # Imprimir la tabla
        print(tabulate(menu_data, headers=headers, tablefmt="heavy_outline"))

        opcion = input(Fore.GREEN + "\nSeleccione una opción: " + Style.RESET_ALL)

        if opcion == "1":
            limpiar_pantalla()
            agregar_hotel(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

        elif opcion == "2":
            limpiar_pantalla()
            consultar_hoteles(hoteles)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

        elif opcion == "3":
            limpiar_pantalla()
            eliminar_hotel(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "4":
            limpiar_pantalla()
            modificar_hotel(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "5":
            limpiar_pantalla()
            modificar_habitaciones_hotel(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

        elif opcion == "0":
            break

        else:
            print(Fore.RED + "Opción inválida. Intente de nuevo.")
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

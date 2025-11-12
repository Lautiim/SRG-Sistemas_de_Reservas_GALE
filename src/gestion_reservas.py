# Importamos funciones y módulos necesarios
from datetime import datetime
from utils import limpiar_pantalla, validar_fecha
import datos  # Para guardar los cambios
from gestion_clientes import consultar_clientes
from gestion_hoteles import consultar_hoteles


def buscar_cliente_por_id(id_cliente: int, clientes: list) -> dict:
    """Función para buscar un cliente por su ID.

    Pre: Recibe el ID del cliente y la lista de clientes.
    """
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return None


def buscar_hotel_por_id(id_hotel: int, hoteles: list) -> dict:
    """Función para buscar un hotel por su ID.

    Pre: Recibe el ID del hotel y la lista de hoteles.
    """
    for hotel in hoteles:
        if hotel["id"] == id_hotel:
            return hotel
    return None


def validar_disponibilidad_habitacion(
    id_hotel: int,
    num_habitacion: int,
    fecha_inicio_dt: datetime,
    fecha_fin_dt: datetime,
    reservas: list,
    hoteles: list,
) -> bool:
    """Funcion para validar si una habitacion de un hotel está disponible en un rango de fechas dado.

    Pre:
        id_hotel (int): ID del hotel.
        num_habitacion (int): Número de la habitación a verificar.
        fecha_inicio_dt (datetime): Fecha de inicio de la reserva deseada.
        fecha_fin_dt (datetime): Fecha de fin de la reserva deseada.
        reservas (list): Lista de todas las reservas existentes.
        hoteles (list): Lista de todos los hoteles (para verificar que la habitación exista).

    Post: Devuelve True si la habitación existe en el hotel y está disponible, False en caso contrario.
    """
    # Verificamos que la habitación exista en el hotel
    hotel = buscar_hotel_por_id(id_hotel, hoteles)
    if not hotel:
        print(f"Error interno: No se encontró el hotel con ID {id_hotel}.")
        return False  # Hotel no encontrado

    # Verificamos si la habitación existe en el hotel
    habitacion_existe = False
    for habitacion in hotel.get("habitaciones", []):
        if habitacion.get("numero") == num_habitacion:
            habitacion_existe = True
            break
    if not habitacion_existe:
        print(
            f"Error: La habitación número {num_habitacion} no existe en el hotel '{hotel['nombre']}'."
        )
        return False  # Habitación no encontrada en este hotel

    # Verificamos si hay reservas que se solapen con las fechas deseadas para esa habitación
    for reserva in reservas:
        # Consideramos reservas de la misma habitación en el mismo hotel
        if (
            reserva["id_hotel"] == id_hotel
            and reserva["numero_habitacion"] == num_habitacion
        ):  # Si coincide hotel y habitación
            # Convertimos las fechas de la reserva existente a datetime para comparar las fechas
            reserva_inicio_dt = datetime.strptime(reserva["fecha_inicio"], "%Y-%m-%d")
            reserva_fin_dt = datetime.strptime(reserva["fecha_fin"], "%Y-%m-%d")

            # Comprobamos si hay solapamiento de fechas
            # Si fecha de inicio es antes de fin existente y fecha de fin es después de inicio existente
            if (fecha_inicio_dt < reserva_fin_dt) and (
                fecha_fin_dt > reserva_inicio_dt
            ):
                print(
                    f"Error: La habitación {num_habitacion} ya está reservada entre {reserva['fecha_inicio']} y {reserva['fecha_fin']}."
                )
                return False  # Se cruzan las fechas, no está disponible

    # Si pasa todas las verificaciones, la habitación existe y está disponible
    return True


def agregar_reserva(hoteles: list, clientes: list, reservas: list) -> None:
    """Función para agregar una nueva reserva al sistema.

    Pre: Recibe las listas de hoteles, clientes y reservas.
    """
    print("--- Agregar Reserva ---")

    # --- Selección de Cliente ---
    consultar_clientes(clientes)  # Mostramos clientes para ayudar a la selección
    if not clientes:
        print("No hay clientes registrados. Debe agregar un cliente primero.")
        return
    while True:
        try:  # Bucle hasta que se seleccione un cliente válido
            id_cliente_seleccionado = int(
                input("Ingrese el ID del cliente para la reserva: ")
            )
            cliente_seleccionado = buscar_cliente_por_id(
                id_cliente_seleccionado, clientes
            )
            if cliente_seleccionado:
                print(f"Cliente seleccionado: {cliente_seleccionado['nombre']}")
                break
            else:
                print("ID de cliente no válido. Intente de nuevo.")
        except ValueError:
            print("Error: Ingrese un ID numérico válido.")

    # --- Selección de Hotel ---
    consultar_hoteles(hoteles)  # Mostramos hoteles
    if not hoteles:
        print("No hay hoteles registrados. Debe agregar un hotel primero.")
        return
    while True:
        try:  # Bucle hasta que se seleccione un hotel válido
            id_hotel_seleccionado = int(
                input("Ingrese el ID del hotel para la reserva: ")
            )
            hotel_seleccionado = buscar_hotel_por_id(id_hotel_seleccionado, hoteles)
            if hotel_seleccionado:
                print(f"Hotel seleccionado: {hotel_seleccionado['nombre']}")
                break
            else:
                print("ID de hotel no válido. Intente de nuevo.")
        except ValueError:
            print("Error: Ingrese un ID numérico válido.")

    # --- Selección de Habitación ---
    print("\nHabitaciones disponibles en este hotel:")
    if hotel_seleccionado["habitaciones"]:  # Verificamos que haya habitaciones
        for hab in hotel_seleccionado["habitaciones"]:  # Si hay, las listamos
            print(
                f"  - Número: {hab['numero']}, Capacidad: {hab['capacidad']}, Precio: ${hab['precio']:.2f}"
            )
    else:
        print("Este hotel no tiene habitaciones registradas.")
        return

    while True:
        try:
            num_habitacion_seleccionada = int(
                input("Ingrese el número de la habitación deseada: ")
            )
            # Verificamos si el número de habitación existe en el hotel seleccionado
            habitacion_valida = False
            for hab in hotel_seleccionado[
                "habitaciones"
            ]:  # Recorremos las habitaciones
                if hab["numero"] == num_habitacion_seleccionada:  # Si coincide
                    habitacion_valida = True
                    break
            if habitacion_valida:
                break
            else:
                print(
                    "Número de habitación no válido para este hotel. Intente de nuevo."
                )
        except ValueError:
            print("Error: Ingrese un número válido.")

    # --- Selección de Fechas ---
    while True:  # Bucle hasta que se ingresen fechas válidas
        fecha_inicio_str = input("Ingrese la fecha de inicio (AAAA-MM-DD): ")
        if validar_fecha(fecha_inicio_str):
            fecha_inicio_dt = datetime.strptime(
                fecha_inicio_str, "%Y-%m-%d"
            )  # Convertimos a datetime para comparaciones
            break
        else:
            print("Formato de fecha incorrecto. Use AAAA-MM-DD.")
    
    # Calculamos la fecha límite (un año después de la fecha de inicio)
    try:
        fecha_limite_dt = fecha_inicio_dt.replace(year=fecha_inicio_dt.year + 1)
    except ValueError:
        # Maneja el caso de año bisiesto
        fecha_limite_dt = fecha_inicio_dt.replace(
            year=fecha_inicio_dt.year + 1, day=28
        )

    while True:
        fecha_fin_str = input("Ingrese la fecha de fin (AAAA-MM-DD): ")
        if validar_fecha(fecha_fin_str):
            fecha_fin_dt = datetime.strptime(
                fecha_fin_str, "%Y-%m-%d"
            )  # Convertimos a datetime para comparaciones
            if fecha_fin_dt <= fecha_inicio_dt:
                print("Error: La fecha de fin debe ser posterior a la fecha de inicio.")
            elif fecha_fin_dt > fecha_limite_dt:
                print(f"Error: La reserva no puede exceder un año desde la fecha de inicio.")
                print(f"La fecha de fin máxima permitida es: {fecha_limite_dt.strftime('%Y-%m-%d')}")
            else:
                break  # Las fechas son válidas
        else:
            print("Formato de fecha incorrecto. Use AAAA-MM-DD.")

    # --- Validar Disponibilidad ---
    if not validar_disponibilidad_habitacion(
        id_hotel_seleccionado,
        num_habitacion_seleccionada,
        fecha_inicio_dt,
        fecha_fin_dt,
        reservas,
        hoteles,
    ):
        # El mensaje de error ya se mostró dentro de la función validar_disponibilidad
        return  # Salimos si no está disponible

    # --- Crear y Guardar Reserva ---
    if reservas:
        id_reserva = reservas[-1]["id"] + 1  # Nuevo ID es el último + 1
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
    print("\n¡Reserva agregada correctamente!")


def consultar_reservas(hoteles, clientes, reservas):
    """Función para mostrar todas las reservas existentes.

    Pre: Recibe las listas de hoteles, clientes y reservas.
    """
    print("--- Reservas Existentes ---")
    if reservas:
        reservas_para_tabla = []
        headers = ["ID", "Cliente", "Hotel", "Habitación", "Fecha Inicio", "Fecha Fin"]

        for reserva in reservas:  # Recorremos las reservas
            # Buscamos nombres para mostrar
            cliente = buscar_cliente_por_id(reserva["id_cliente"], clientes)

            if cliente:
                nombre_cliente = cliente[
                    "nombre"
                ]  # Usamos el nombre si encontramos el cliente
            else:
                nombre_cliente = f"ID {reserva.get('id_cliente', 'No encontrado')}"  # Usamos ID si no encontramos el cliente

            hotel = buscar_hotel_por_id(reserva["id_hotel"], hoteles)
            if hotel:
                nombre_hotel = hotel[
                    "nombre"
                ]  # Usamos el nombre si encontramos el hotel
            else:
                nombre_hotel = f"ID {reserva.get('id_hotel', 'No encontrado')}"  # Usamos ID si no encontramos el hotel

            # Preparamos la fila para la tabla
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

        try:
            # Intentamos usar tabulate para mostrar la tabla de forma bonita
            from tabulate import tabulate

            print(tabulate(reservas_para_tabla, headers=headers, tablefmt="grid"))
        except ImportError:  # Si no está instalado, mostramos de forma simple
            print("(Librería 'tabulate' no encontrada. Mostrando en formato simple.)")
            for fila in reservas_para_tabla:
                # Imprime cada elemento de la fila separado por " | "
                print(
                    " | ".join(map(str, fila))
                )  # Convertimos todo a str para evitar errores, y unimos con " | "
    else:
        print("No hay reservas registradas.")


def eliminar_reserva(hoteles: list, clientes: list, reservas: list) -> None:
    """Elimina una reserva de la lista por su ID y guarda los cambios.

    Pre: Recibe las listas de hoteles, clientes y reservas.
    """
    print("--- Eliminar Reserva ---")
    consultar_reservas(
        hoteles, clientes, reservas
    )  # Mostramos las reservas para ver IDs

    if not reservas:  # Si no hay reservas, no tiene sentido continuar
        print("No hay reservas para eliminar.")
        return

    while True:  # Bucle hasta que se ingrese un ID válido
        try:
            id_a_eliminar = int(
                input("Ingrese el ID de la reserva que desea eliminar: ")
            )  # Pedimos ID de la reserva a eliminar
            break
        except ValueError:
            print("Error: Ingrese un ID numérico válido.")

    reserva_encontrada = None
    indice_reserva = -1

    for i, reserva in enumerate(reservas):  # Buscamos la reserva por ID
        if reserva["id"] == id_a_eliminar:  # Si coincide
            reserva_encontrada = reserva
            indice_reserva = i
            break

    if reserva_encontrada:
        cliente = buscar_cliente_por_id(reserva_encontrada["id_cliente"], clientes)
        hotel = buscar_hotel_por_id(reserva_encontrada["id_hotel"], hoteles)
        nombre_cliente = cliente["nombre"] if cliente else "Desconocido"
        nombre_hotel = hotel["nombre"] if hotel else "Desconocido"

        print(f"\nReserva a eliminar:")
        print(f"  Cliente: {nombre_cliente}")
        print(f"  Hotel: {nombre_hotel}")
        print(f"  Habitación: {reserva_encontrada['numero_habitacion']}")
        print(
            f"  Fechas: {reserva_encontrada['fecha_inicio']} a {reserva_encontrada['fecha_fin']}"
        )

        confirmacion = input(
            f"¿Está seguro que desea eliminar esta reserva (ID: {id_a_eliminar})? (s/n): "
        )
        if confirmacion.lower() == "s":
            reservas.pop(indice_reserva)  # Eliminamos la reserva de la lista
            datos.guardar_datos(hoteles, clientes, reservas)  # Guardamos los cambios
            print("Reserva eliminada correctamente.")
        else:
            print("Eliminación cancelada.")
    else:
        print(f"No se encontró ninguna reserva con el ID {id_a_eliminar}.")


def gestionar_reservas(hoteles, clientes, reservas):
    """Función principal para interactuar con el menú de gestión de reservas.

    Pre: Recibe las listas de hoteles, clientes y reservas.
    """
    while True:
        limpiar_pantalla()
        print("=" * 40)
        print("     --- Gestión de Reservas ---      ".center(40, " "))
        print("=" * 40)
        print("1. Agregar Reserva")
        print("2. Consultar Reservas")
        print("3. Eliminar Reserva")
        print("0. Volver al menú principal")
        print("=" * 40)

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            limpiar_pantalla()
            agregar_reserva(hoteles, clientes, reservas)
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            limpiar_pantalla()
            consultar_reservas(hoteles, clientes, reservas)
            input("\nPresione Enter para continuar...")
        elif opcion == "3":
            limpiar_pantalla()
            eliminar_reserva(hoteles, clientes, reservas)
            input("\nPresione Enter para continuar...")
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

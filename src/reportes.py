# Importamos funciones necesarias de otros módulos
from datetime import datetime
from utils import limpiar_pantalla, validar_fecha
from gestion_hoteles import consultar_hoteles, buscar_hotel_por_id
from gestion_clientes import consultar_clientes, buscar_cliente_por_id
from gestion_reservas import consultar_reservas
from tabulate import tabulate


def buscar_reserva_x_cliente(hoteles: list, clientes: list, reservas: list):
    """
    Busca y muestra todas las reservas asociadas a un cliente específico por su ID.

    Pre: Recibe la lista de hoteles, clientes y reservas.
    """
    print("--- Buscar Reservas por Cliente ---")
    consultar_clientes(clientes)  # Mostramos clientes para facilitar selección
    if not clientes:
        print("No hay clientes registrados.")
        return

    while True:
        try:
            id_cliente_buscar = int(
                input("Ingrese el ID del cliente para buscar sus reservas: ")
            )
            cliente_seleccionado = buscar_cliente_por_id(id_cliente_buscar, clientes)
            if cliente_seleccionado:  # Si el cliente existe
                print(
                    f"Buscando reservas para: {cliente_seleccionado['nombre']} (ID: {id_cliente_buscar})"
                )
                break
            else:
                print("ID de cliente no válido. Intente de nuevo.")
        except ValueError:
            print("Error: Ingrese un ID numérico válido.")

    reservas_encontradas = []  # Lista para almacenar reservas encontradas
    headers = ["ID Reserva", "Hotel", "Habitación", "Fecha Inicio", "Fecha Fin"]

    for reserva in reservas:  # Recorremos todas las reservas
        if (
            reserva["id_cliente"] == id_cliente_buscar
        ):  # Si la reserva pertenece al cliente buscado
            hotel = buscar_hotel_por_id(reserva["id_hotel"], hoteles)

            if hotel:
                nombre_hotel = hotel["nombre"]
            else:
                nombre_hotel = f"ID {reserva['id_hotel']} (No encontrado)"

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
        print(f"\nReservas encontradas para {cliente_seleccionado['nombre']}:")
        try:
            print(tabulate(reservas_encontradas, headers=headers, tablefmt="grid"))
        except ImportError:
            print("(Librería 'tabulate' no encontrada. Mostrando en formato simple.)")
            print(" | ".join(headers))
            for fila in reservas_encontradas:
                print(" | ".join(map(str, fila)))
    else:
        print(
            f"No se encontraron reservas para el cliente {cliente_seleccionado['nombre']}."
        )


def buscar_reserva_x_hotel(hoteles: list, clientes: list, reservas: list):
    """Función para buscar y mostrar reservas por hotel.

    Pre: Recibe la lista de hoteles, clientes y reservas.
    """
    print("--- Buscar Reservas por Hotel ---")
    consultar_hoteles(hoteles)  # Mostramos hoteles para facilitar selección
    if not hoteles:
        print("No hay hoteles registrados.")
        return

    while True:
        try:
            id_hotel_buscar = int(
                input("Ingrese el ID del hotel para buscar sus reservas: ")
            )
            hotel_seleccionado = buscar_hotel_por_id(id_hotel_buscar, hoteles)
            if hotel_seleccionado:
                print(
                    f"Buscando reservas para: {hotel_seleccionado['nombre']} (ID: {id_hotel_buscar})"
                )
                break
            else:
                print("ID de hotel no válido. Intente de nuevo.")
        except ValueError:
            print("Error: Ingrese un ID numérico válido.")

    reservas_encontradas = []
    headers = ["ID Reserva", "Cliente", "Habitación", "Fecha Inicio", "Fecha Fin"]

    for reserva in reservas:
        if reserva["id_hotel"] == id_hotel_buscar:
            cliente = buscar_cliente_por_id(reserva["id_cliente"], clientes)
            if cliente:
                nombre_cliente = cliente["nombre"]
            else:
                nombre_cliente = f"ID {reserva['id_cliente']} (No encontrado)"
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
        print(f"\nReservas encontradas para {hotel_seleccionado['nombre']}:")
        try:
            print(tabulate(reservas_encontradas, headers=headers, tablefmt="grid"))
        except ImportError:
            print("(Librería 'tabulate' no encontrada. Mostrando en formato simple.)")
            print(" | ".join(headers))
            for fila in reservas_encontradas:
                print(" | ".join(map(str, fila)))
    else:
        print(
            f"No se encontraron reservas para el hotel {hotel_seleccionado['nombre']}."
        )


def consultar_habitaciones_disponibles(hoteles: list, reservas: list):
    """Funcion las habitaciones disponibles en un hotel para un rango de fechas.

    Pre:
        hoteles (list): Lista de todos los hoteles.
        reservas (list): Lista de todas las reservas.
    """
    print("--- Consultar Habitaciones Disponibles ---")
    consultar_hoteles(hoteles) # Mostramos hoteles para facilitar selección
    if not hoteles:
        print("No hay hoteles registrados.")
        return

    # --- Selección de Hotel ---
    while True:
        try:
            id_hotel_buscar = int(input("Ingrese el ID del hotel para consultar disponibilidad: "))
            hotel_seleccionado = buscar_hotel_por_id(id_hotel_buscar, hoteles)
            if hotel_seleccionado:
                print(f"Consultando disponibilidad para: {hotel_seleccionado['nombre']} (ID: {id_hotel_buscar})")
                break
            else:
                print("ID de hotel no válido. Intente de nuevo.")
        except ValueError:
            print("Error: Ingrese un ID numérico válido.")

    if not hotel_seleccionado.get('habitaciones'):
        print(f"El hotel '{hotel_seleccionado['nombre']}' no tiene habitaciones registradas.")
        return

    # --- Selección de Fechas ---
    while True:
        fecha_inicio_str = input("Ingrese la fecha de inicio deseada (AAAA-MM-DD): ")
        if validar_fecha(fecha_inicio_str):
            fecha_inicio_dt = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
            # Validar que no sea una fecha pasada
            if fecha_inicio_dt.date() >= datetime.now().date():
                 break
            else:
                 print("Error: La fecha de inicio no puede ser una fecha pasada.")
        else:
            print("Formato de fecha incorrecto. Use AAAA-MM-DD.")

    while True:
        fecha_fin_str = input("Ingrese la fecha de fin deseada (AAAA-MM-DD): ")
        if validar_fecha(fecha_fin_str):
            fecha_fin_dt = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
            if fecha_fin_dt > fecha_inicio_dt:
                break
            else:
                print("Error: La fecha de fin debe ser posterior a la fecha de inicio.")
        else:
            print("Formato de fecha incorrecto. Use AAAA-MM-DD.")

    # --- Encontrar Habitaciones Ocupadas en esas Fechas ---
    habitaciones_ocupadas_numeros = set() # Usamos un set para guardar los números de habitación ocupados

    for r in reservas:
        # Solo consideramos reservas del hotel seleccionado
        if r['id_hotel'] == id_hotel_buscar:
            reserva_inicio_dt = datetime.strptime(r['fecha_inicio'], '%Y-%m-%d')
            reserva_fin_dt = datetime.strptime(r['fecha_fin'], '%Y-%m-%d')

            # Comprobamos si hay solapamiento (si la reserva existente choca con las fechas buscadas)
            if (fecha_inicio_dt < reserva_fin_dt) and (fecha_fin_dt > reserva_inicio_dt):
                habitaciones_ocupadas_numeros.add(r['numero_habitacion'])

    # --- Determinar Habitaciones Disponibles ---
    habitaciones_disponibles = []
    todas_las_habitaciones_hotel = hotel_seleccionado.get('habitaciones', [])

    for hab in todas_las_habitaciones_hotel:
        # Si el número de la habitación NO está en el set de ocupadas, está disponible
        if hab['numero'] not in habitaciones_ocupadas_numeros:
            habitaciones_disponibles.append(hab)

    # --- Mostrar Resultados ---
    print(f"\n--- Habitaciones Disponibles en '{hotel_seleccionado['nombre']}' entre {fecha_inicio_str} y {fecha_fin_str} ---")
    if habitaciones_disponibles:
        try:
            from tabulate import tabulate # Intentamos importar tabulate aquí
            headers = ["Número", "Capacidad", "Precio x Noche"]
            tabla_disponibles = [[h['numero'], h['capacidad'], f"${h['precio']:.2f}"] for h in habitaciones_disponibles]
            print(tabulate(tabla_disponibles, headers=headers, tablefmt="grid"))
        except ImportError: # Si falla la importación de tabulate
            print("(Librería 'tabulate' no encontrada. Mostrando en formato simple.)")
            print("Número | Capacidad | Precio x Noche")
            for h in habitaciones_disponibles:
                print(f"{h['numero']:<6} | {h['capacidad']:<9} | ${h['precio']:.2f}")
    else:
        print("No hay habitaciones disponibles en las fechas seleccionadas.")


def generar_reportes(hoteles: list, clientes: list, reservas: list) -> None:
    """Función principal para interactuar con el menú de generación de reportes.

    Pre: Recibe las listas de hoteles, clientes y reservas.
    """
    while True:
        limpiar_pantalla()
        print("=" * 40)
        print("   --- Generación de Reportes ---     ".center(40, " "))
        print("=" * 40)
        print("1. Listar todos los hoteles")
        print("2. Listar todos los clientes")
        print("3. Listar todas las reservas")
        print("4. Buscar reservas por cliente")
        print("5. Buscar reservas por hotel")
        print("6. Consultar habitaciones disponibles")
        print("0. Volver al menú principal")
        print("=" * 40)

        opcion = input("Seleccione una opción: ")
        limpiar_pantalla()  # Limpiamos después de pedir la opción

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
            print("Opción inválida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    from datos import cargar_datos

    hoteles, clientes, reservas = cargar_datos()
    generar_reportes(hoteles, clientes, reservas)

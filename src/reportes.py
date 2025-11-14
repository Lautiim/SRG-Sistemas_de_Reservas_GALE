# Importaciones organizadas por grupos: estándar, terceros, locales
from datetime import datetime
import os

from colorama import Fore, Style, init
from tabulate import tabulate

# Soportar importación como paquete (src.*) y ejecución directa
try:
    from . import datos  # type: ignore
    from .gestion_clientes import buscar_cliente_por_id, consultar_clientes  # type: ignore
    from .gestion_hoteles import buscar_hotel_por_id, consultar_hoteles  # type: ignore
    from .gestion_reservas import consultar_reservas  # type: ignore
    from .utils import limpiar_pantalla, validar_fecha  # type: ignore
except ImportError:  # pragma: no cover
    import datos
    from gestion_clientes import buscar_cliente_por_id, consultar_clientes
    from gestion_hoteles import buscar_hotel_por_id, consultar_hoteles
    from gestion_reservas import consultar_reservas
    from utils import limpiar_pantalla, validar_fecha


def _pedir_fecha_inicio() -> tuple[str, datetime]:
    """Solicita una fecha de inicio válida (no pasada)."""
    while True:
        fecha_str = input(
            Fore.GREEN + "Ingrese la fecha de inicio (AAAA-MM-DD): " + Style.RESET_ALL
        )
        if not validar_fecha(fecha_str):
            print(Fore.RED + "Formato de fecha incorrecto. Use AAAA-MM-DD.")
            continue
        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
        if fecha_dt.date() < datetime.now().date():
            print(Fore.RED + "Error: La fecha de inicio no puede ser una fecha pasada.")
            continue
        return fecha_str, fecha_dt


def _pedir_fecha_fin(fecha_inicio_dt: datetime) -> tuple[str, datetime]:
    """Solicita una fecha de fin válida (posterior al inicio)."""
    while True:
        fecha_str = input(Fore.GREEN + "Ingrese la fecha de fin (AAAA-MM-DD): " + Style.RESET_ALL)
        if not validar_fecha(fecha_str):
            print(Fore.RED + "Formato de fecha incorrecto. Use AAAA-MM-DD.")
            continue
        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
        if fecha_dt <= fecha_inicio_dt:
            print(Fore.RED + "Error: La fecha de fin debe ser posterior a la fecha de inicio.")
            continue
        return fecha_str, fecha_dt


def buscar_reserva_x_cliente(hoteles: list, clientes: list, reservas: list):
    """Busca y muestra todas las reservas asociadas a un cliente específico por su ID.

    Pre: Recibe la lista de hoteles, clientes y reservas.

    Post: Muestra por pantalla las reservas del cliente
    o un mensaje si no hay reservas.
    """
    print(Fore.CYAN + Style.BRIGHT + "--- Buscar Reservas por Cliente ---" + Style.RESET_ALL)
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
                msg_buscar_cliente = (
                    f"Buscando reservas para: {cliente_seleccionado['nombre']} "
                    f"(ID: {id_cliente_buscar})"
                )
                print(Fore.CYAN + msg_buscar_cliente + Style.RESET_ALL)
                break
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
                    Fore.RED + f"ID {reserva['id_hotel']} (No encontrado)" + Style.RESET_ALL
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
        msg_reservas_cliente = f"\nReservas encontradas para {cliente_seleccionado['nombre']}:"
        print(Fore.CYAN + msg_reservas_cliente + Style.RESET_ALL)
        print(
            tabulate(
                reservas_encontradas,
                headers=headers,
                tablefmt="grid",
            )
        )
    else:
        print(
            Fore.YELLOW
            + f"No se encontraron reservas para el cliente {cliente_seleccionado['nombre']}."
        )


def buscar_reserva_x_hotel(hoteles: list, clientes: list, reservas: list):
    """Función para buscar y mostrar reservas por hotel."""
    print(Fore.CYAN + Style.BRIGHT + "--- Buscar Reservas por Hotel ---" + Style.RESET_ALL)
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
                msg_buscar_hotel = (
                    f"Buscando reservas para: {hotel_seleccionado['nombre']} "
                    f"(ID: {id_hotel_buscar})"
                )
                print(Fore.CYAN + msg_buscar_hotel + Style.RESET_ALL)
                break
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
                    Fore.RED + f"ID {reserva['id_cliente']} (No encontrado)" + Style.RESET_ALL
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
        msg_reservas_hotel = f"\nReservas encontradas para {hotel_seleccionado['nombre']}:"
        print(Fore.CYAN + msg_reservas_hotel + Style.RESET_ALL)
        print(
            tabulate(
                reservas_encontradas,
                headers=headers,
                tablefmt="grid",
            )
        )
    else:
        print(
            Fore.YELLOW
            + f"No se encontraron reservas para el hotel {hotel_seleccionado['nombre']}."
        )


def consultar_habitaciones_disponibles(hoteles: list, reservas: list):
    """Función que muestra las habitaciones disponibles en un hotel para un rango de fechas."""
    print(Fore.CYAN + Style.BRIGHT + "--- Consultar Habitaciones Disponibles ---" + Style.RESET_ALL)
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
                msg_consulta_disp = (
                    f"Consultando disponibilidad para: {hotel_seleccionado['nombre']} "
                    f"(ID: {id_hotel_buscar})"
                )
                print(Fore.CYAN + msg_consulta_disp + Style.RESET_ALL)
                break
            print(Fore.RED + "ID de hotel no válido. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    if not hotel_seleccionado.get("habitaciones"):
        msg_sin_habs = (
            "El hotel '" + hotel_seleccionado["nombre"] + "' no tiene habitaciones registradas."
        )
        print(Fore.YELLOW + msg_sin_habs)
        return

    # Selección de fechas
    fecha_inicio_str, fecha_inicio_dt = _pedir_fecha_inicio()
    fecha_fin_str, fecha_fin_dt = _pedir_fecha_fin(fecha_inicio_dt)

    # Encontrar habitaciones ocupadas en esas fechas
    habitaciones_ocupadas_numeros = set()

    for r in reservas:
        if r["id_hotel"] == id_hotel_buscar:
            reserva_inicio_dt = datetime.strptime(r["fecha_inicio"], "%Y-%m-%d")
            reserva_fin_dt = datetime.strptime(r["fecha_fin"], "%Y-%m-%d")

            if (fecha_inicio_dt < reserva_fin_dt) and (fecha_fin_dt > reserva_inicio_dt):
                habitaciones_ocupadas_numeros.add(r["numero_habitacion"])

    # Determinar habitaciones disponibles
    habitaciones_disponibles = []
    todas_las_habitaciones_hotel = hotel_seleccionado.get("habitaciones", [])

    for hab in todas_las_habitaciones_hotel:
        if hab["numero"] not in habitaciones_ocupadas_numeros:
            habitaciones_disponibles.append(hab)

    # Mostrar resultados
    titulo_disponibles = (
        "\n--- Habitaciones Disponibles en '"
        + hotel_seleccionado["nombre"]
        + "' entre "
        + fecha_inicio_str
        + " y "
        + fecha_fin_str
        + " ---"
    )
    print(Fore.CYAN + titulo_disponibles + Style.RESET_ALL)
    if habitaciones_disponibles:
        headers = [
            Fore.GREEN + "Número" + Style.RESET_ALL,
            Fore.GREEN + "Capacidad" + Style.RESET_ALL,
            Fore.GREEN + "Precio x Noche" + Style.RESET_ALL,
        ]
        tabla_disponibles = [
            [h["numero"], h["capacidad"], f"${h['precio']:.2f}"] for h in habitaciones_disponibles
        ]
        print(
            tabulate(
                tabla_disponibles,
                headers=headers,
                tablefmt="grid",
            )
        )
    else:
        print(Fore.YELLOW + "No hay habitaciones disponibles en las fechas seleccionadas.")


def exportar_clientes_csv(clientes: list, ruta_archivo: str) -> None:
    """
    Función para exportar la lista de clientes a un archivo CSV.

    Pre: Recibe la lista de clientes y la ruta del archivo CSV donde se guardarán los datos.

    Post: Crea un archivo CSV con los datos de los clientes.
    """

    print(f"Exportando clientes a {ruta_archivo}...")
    # Si no existen clientes, no se crea el archivo
    if not clientes:
        print("No hay clientes para exportar.")
        return
    # Creamos el archivo CSV y escribimos las columnas que deseamos exportar
    fieldnames = ["id", "nombre", "dni", "telefono"]
    delimitador = ","  # Delimitador estándar para CSV
    try:
        # Usamos 'w' (write) y newline='' para evitar saltos de línea extra
        with open(ruta_archivo, "w", encoding="utf-8") as file:
            # Escribimos el encabezado manualmente
            # Une la lista de fieldnames: "id,nombre,dni,telefono"
            file.write(delimitador.join(fieldnames) + "\n")

            for cliente in clientes:
                # Creamos una lista de strings para esta fila
                fila_lista = [
                    str(cliente.get("id", "")),
                    str(cliente.get("nombre", "")),
                    str(cliente.get("dni", "")),
                    str(cliente.get("telefono", "")),
                ]
                # Unimos la lista con comas y agregamos un salto de línea
                file.write(delimitador.join(fila_lista) + "\n")

        print(f"Archivo '{ruta_archivo}' creado con éxito.")

    except OSError as e:  # Errores de acceso al archivo
        print(f"Error al escribir el archivo CSV: {e}")


def exportar_reservas_csv(reservas: list, ruta_archivo: str) -> None:
    """
    Función para exportar la lista de reservas a un archivo CSV.

    Pre: Recibe la lista de reservas y la ruta del archivo CSV donde se guardarán los datos.

    Post: Crea un archivo CSV con los datos de las reservas.
    """
    print(f"Exportando reservas a {ruta_archivo}...")
    if not reservas:
        print("No hay reservas para exportar.")
        return
    # Creamos los encabezados que deseamos exportar en el csv
    fieldnames = ["id", "id_cliente", "id_hotel", "numero_habitacion", "fecha_inicio", "fecha_fin"]
    delimitador = ","  # Delimitador estándar para CSV

    try:
        # Usamos 'w' (write) y newline='' para evitar saltos de línea extra
        with open(ruta_archivo, "w", encoding="utf-8") as file:
            # Escribimos el encabezado manualmente
            file.write(delimitador.join(fieldnames) + "\n")
            for reserva in reservas:
                # Creamos una lista de strings para esta fila
                fila_lista = [
                    str(reserva.get("id", "")),
                    str(reserva.get("id_cliente", "")),
                    str(reserva.get("id_hotel", "")),
                    str(reserva.get("numero_habitacion", "")),
                    str(reserva.get("fecha_inicio", "")),
                    str(reserva.get("fecha_fin", "")),
                ]
                # Unimos la lista con comas y agregamos un salto de línea
                file.write(delimitador.join(fila_lista) + "\n")
        print(f"Archivo '{ruta_archivo}' creado con éxito.")

    except OSError as e:
        print(f"Error al escribir el archivo CSV: {e}")


def exportar_hoteles_csv(hoteles: list, ruta_hoteles: str, ruta_habitaciones: str) -> None:
    """
    Función para exportar la lista de hoteles a un archivo CSV.

    Pre: Recibe la lista de hoteles y la ruta del archivo CSV donde se guardarán los datos.

    Post: Crea un archivo CSV con los datos de los hoteles.
    """
    print(f"Exportando hoteles a {ruta_hoteles}...")
    if not hoteles:
        print("No hay hoteles para exportar.")
        return
    # Creamos los encabezados principales de hoteles para exportar
    fieldnames_hoteles = ["id", "nombre", "ubicacion"]
    delimitador = ","  # Delimitador estándar para CSV

    # Recorremos la lista de hoteles para extraer los datos principales
    try:
        # Usamos 'w' (write) y newline='' para evitar saltos de línea extra
        with open(ruta_hoteles, "w", encoding="utf-8") as file:
            file.write(delimitador.join(fieldnames_hoteles) + "\n")
            for hotel in hoteles:
                # Creamos una lista de strings para esta fila
                fila_lista = [
                    str(hotel.get("id", "")),
                    str(hotel.get("nombre", "")),
                    str(hotel.get("ubicacion", "")),
                ]
                # Unimos la lista con comas y agregamos un salto de línea
                file.write(delimitador.join(fila_lista) + "\n")

        print(f"Archivo '{ruta_hoteles}' creado con éxito.")

    except OSError as e:
        print(f"Error al escribir el archivo {ruta_hoteles}: {e}")

    # Ahora exportamos las habitaciones de cada hotel a otro archivo CSV
    print(f"Exportando habitaciones a {ruta_habitaciones}...")
    fieldnames_habitaciones = ["id_hotel", "numero", "capacidad", "precio"]
    # Creamos una lista para almacenar las habitaciones en formato CSV
    habitaciones_csv = []

    # Recorremos la lista de hoteles para extraer las habitaciones
    for hotel in hoteles:
        # Obtenemos el ID del hotel actual
        id_hotel = hotel.get("id")
        # Recorremos las habitaciones del hotel actual
        for habitaciones in hotel.get("habitaciones", []):
            # Por cada habitación que encuentra, crea un nuevo diccionario
            # y lo agrega a la lista habitaciones_csv.
            habitaciones_csv.append(
                {
                    # Agregamos los datos de la habitación correspondiente
                    "id_hotel": id_hotel,
                    "numero": habitaciones.get("numero"),
                    "capacidad": habitaciones.get("capacidad"),
                    "precio": habitaciones.get("precio"),
                }
            )

    if not habitaciones_csv:
        print("No se encontraron habitaciones para exportar.")
        return

    try:
        # Usamos 'w' (write) y newline='' para evitar saltos de línea extra
        with open(ruta_habitaciones, "w", encoding="utf-8") as file:
            file.write(delimitador.join(fieldnames_habitaciones) + "\n")
            for habitacion in habitaciones_csv:
                # Creamos una lista de strings para esta fila
                fila_lista = [
                    str(habitacion.get("id_hotel", "")),
                    str(habitacion.get("numero", "")),
                    str(habitacion.get("capacidad", "")),
                    str(habitacion.get("precio", "")),
                ]
                # Unimos la lista con comas y agregamos un salto de línea
                file.write(delimitador.join(fila_lista) + "\n")

        print(f"Archivo '{ruta_habitaciones}' creado con éxito.")
    except OSError as e:
        print(f"Error al escribir el archivo {ruta_habitaciones}: {e}")


def exportar_datos_csv(hoteles: list, clientes: list, reservas: list) -> None:
    """
    Función principal para gestionar la exportación de todos los datos a CSV.
    Maneja la lógica de rutas y llama a las funciones de exportación.
    Pre: Recibe las listas de hoteles, clientes y reservas.

    Post: Exporta los datos a archivos CSV en las rutas especificadas.
    """
    limpiar_pantalla()
    print("=" * 40)
    print("   --- Exportando datos a CSV ---     ".center(40, " "))
    print("=" * 40)

    try:
        # 1. Crear carpeta 'csv' si no existe
        ruta_csv = os.path.join(datos.RUTA_DATA, "csv")
        if not os.path.exists(ruta_csv):
            os.makedirs(ruta_csv)

        # 2. Definir las rutas dentro de la carpeta csv
        ruta_clientes_csv = os.path.join(ruta_csv, "clientes_export.csv")
        ruta_reservas_csv = os.path.join(ruta_csv, "reservas_export.csv")
        ruta_hoteles_csv = os.path.join(ruta_csv, "hoteles_export.csv")
        ruta_habitaciones_csv = os.path.join(ruta_csv, "habitaciones_export.csv")

        # 3. Llamar a las funciones de exportación (que están en este mismo archivo)
        exportar_clientes_csv(clientes, ruta_clientes_csv)
        exportar_reservas_csv(reservas, ruta_reservas_csv)
        exportar_hoteles_csv(hoteles, ruta_hoteles_csv, ruta_habitaciones_csv)

        print("\n¡Datos exportados exitosamente en la carpeta 'data/csv/'!")

    except OSError as e:  # Errores de filesystem
        print(f"\nError de E/S al exportar: {e}")

    input("\nPresione Enter para continuar...")


def generar_reportes(hoteles: list, clientes: list, reservas: list) -> None:
    """Función principal para interactuar con el menú de generación de reportes."""

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
            [Fore.MAGENTA + "7" + Style.RESET_ALL, "Exportar datos a CSV"],
            [Fore.RED + "0" + Style.RESET_ALL, "Volver al menú principal"],
        ]

        # Headers para la tabla
        headers = [
            Fore.GREEN + "Opción" + Style.RESET_ALL,
            Fore.GREEN + "Acción" + Style.RESET_ALL,
        ]

        # Imprimir la tabla
        print(
            tabulate(
                menu_data,
                headers=headers,
                tablefmt="heavy_outline",
            )
        )

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
        elif opcion == "7":
            exportar_datos_csv(hoteles, clientes, reservas)
        elif opcion == "0":
            break
        else:
            print(Fore.RED + "Opción inválida. Intente de nuevo.")

        input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)


if __name__ == "__main__":  # Ejecutable directo para pruebas manuales
    _hoteles, _clientes, _reservas = datos.cargar_datos()
    generar_reportes(_hoteles, _clientes, _reservas)

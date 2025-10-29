# Importamos funciones necesarias de otros módulos
from utils import limpiar_pantalla
from gestion_hoteles import consultar_hoteles, buscar_hotel_por_id
from gestion_clientes import consultar_clientes, buscar_cliente_por_id
from gestion_reservas import consultar_reservas
from tabulate import tabulate
from datos import cargar_datos
import os 
import csv


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
    """
    (Futura implementación) Muestra las habitaciones disponibles en un hotel para un rango de fechas.
    """
    print("Funcionalidad de consulta de habitaciones disponibles próximamente.")


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
        print("6. Consultar habitaciones disponibles (Próximamente)")
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
    hoteles, clientes, reservas = cargar_datos()
    generar_reportes(hoteles, clientes, reservas)

def exportar_clientes_csv(clientes: list, ruta_archivo: str) -> None:
    """Función para exportar la lista de clientes a un archivo CSV.

    Pre: Recibe la lista de clientes y la ruta del archivo CSV donde se guardarán los datos.

    Post: Crea un archivo CSV con los datos de los clientes.
    """

    # Si no existen clientes, no se crea el archivo
    if not clientes:
        print("No hay clientes para exportar.")
        return
    # Creamos el archivo CSV y escribimos las columnas que deseamos exportar
    fieldnames = ['id', 'nombre', 'dni', 'telefono']
    try:
        # Usamos 'w' (write) y newline='' para evitar saltos de línea extra
        with open(ruta_archivo, 'w', newline='', encoding='utf-8') as file:
            # Creamos el escritor de diccionarios
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()      # Escribe la fila de encabezado (id, nombre, dni, telefono)
            writer.writerows(clientes)

        print(f"Archivo '{ruta_archivo}' creado con éxito.")
    
    except IOError as e:
        print(f"Error al escribir el archivo CSV: {e}")
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}")
    
def exportar_reservas_csv(reservas: list, ruta_archivo: str) -> None:
    """Función para exportar la lista de reservas a un archivo CSV.

    Pre: Recibe la lista de reservas y la ruta del archivo CSV donde se guardarán los datos.

    Post: Crea un archivo CSV con los datos de las reservas.
    """

def exportar_hoteles_csv(hoteles: list, ruta_hoteles: str, ruta_habitaciones: str) -> None:
    """Función para exportar la lista de hoteles a un archivo CSV.

    Pre: Recibe la lista de hoteles y la ruta del archivo CSV donde se guardarán los datos.

    Post: Crea un archivo CSV con los datos de los hoteles.
    """

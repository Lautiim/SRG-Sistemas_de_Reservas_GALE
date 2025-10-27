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

def generar_reportes() -> None:
    """Funcionalidad para generar reportes

    Al ser invocada, esta funcion permite al usuario ver las opciones
    para generar reportes.
    """
    while True:
        limpiar_pantalla()
        print("=" * 40)
        print("   --- Generación de Reportes ---     ".center(40, " "))
        print("=" * 40)
        print("1. Consultar hoteles")
        print("2. Consultar clientes")
        print("3. Consultar reservas")
        print("4. Consultar reservas por cliente")
        print("5. Consultar reservas por hotel")
        print("6. Consultar habitaciones disponibles en un hotel")
        print("0. Volver al menú principal")
        print("=" * 40)

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            limpiar_pantalla()
            consultar_hoteles()
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            limpiar_pantalla()
            consultar_clientes()
            input("\nPresione Enter para continuar...")
        elif opcion == "3":
            limpiar_pantalla()
            consultar_reservas()
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            limpiar_pantalla()
            buscar_reserva_x_cliente()
            input("\nPresione Enter para continuar...")
        elif opcion == "5":
            limpiar_pantalla()
            buscar_reserva_x_hotel()
            input("\nPresione Enter para continuar...")
        elif opcion == "6":
            limpiar_pantalla()
            print("Funcionalidad en desarrollo.. :D")
            input("\nPresione Enter para continuar...")
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
            input("\nPresione Enter para continuar...")


def buscar_reserva_x_cliente() -> (
    None
):  # Esta funcion fue renombrada, se usara mas adelante en la seccion de reportes. Actualmente no se invoca en ningun lado
    """Funcionalidad para buscar las reservas de un cliente

    Al ser invocada, esta funcion permite al usuario ingresar el nombre
    de un cliente para buscar reservas a su nombre.
    """
    print("--- Buscar Reservas por Cliente ---")
    reservas_cliente = []  # Lista que almacenara las reservas del cliente

    # Solicitamos el nombre del cliente
    nombre_cliente = input("Ingrese el nombre del cliente para buscar sus reservas: ")
    ID_cliente = validar_cliente(nombre_cliente)

    if ID_cliente == 0:  # Si no encontramos al cliente, informamos por pantalla
        print("No se encontró un cliente con ese nombre")
    else:  # Si encontramos al cliente, buscamos por reservas con su ID
        for reserva in reservas:
            if ID_cliente == reserva["ID_cliente"]:
                reservas_cliente.append(
                    reserva
                )  # Si encontramos una reserva que coincida, la agregamos a la lista

        # Si hay reservas, las mostramos por pantalla
        if reservas_cliente:
            print(f"Reservas encontradas para {nombre_cliente}:")
            for reserva in reservas_cliente:
                print(reserva)
        else:  # En caso de no haber reservas, lo informamos igualmente
            print("No se encontraron reservas para ese cliente")


def buscar_reserva_x_hotel() -> None:
    """Funcionalidad para buscar las reservas de un hotel

    Al ser invocada, esta funcion permite al usuario ingresar el nombre
    de un hotel para buscar reservas asociadas a ese hotel.
    """
    print("--- Buscar Reservas por Hotel ---")
    reservas_hotel = []  # Lista que almacenara las reservas del hotel

    # Solicitamos el nombre del hotel
    nombre_hotel = input("Ingrese el nombre del hotel para buscar sus reservas: ")
    ID_hotel = validar_hotel(nombre_hotel)

    if ID_hotel == 0:  # Si no encontramos al hotel, informamos por pantalla
        print("No se encontró un hotel con ese nombre")
    else:  # Si encontramos al hotel, buscamos por reservas con su ID
        for reserva in reservas:
            if ID_hotel == reserva["ID_hotel"]:
                reservas_hotel.append(
                    reserva
                )  # Si encontramos una reserva que coincida, la agregamos a la lista

        # Si hay reservas, las mostramos por pantalla
        if reservas_hotel:
            print(f"Reservas encontradas para {nombre_hotel}:")
            for reserva in reservas_hotel:
                print(reserva)
        else:  # En caso de no haber reservas, lo informamos igualmente
            print("No se encontraron reservas para ese hotel")


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


# Datos de ejemplo para pruebas
hoteles = [
    {
        "ID": 1,
        "Nombre": "Hotel Sol",
        "Ubicacion": "Ciudad",
        "Cantidad de Habitaciones": 20,
    },
    {
        "ID": 2,
        "Nombre": "Hotel Luna",
        "Ubicacion": "Playa",
        "Cantidad de Habitaciones": 30,
    },
    {
        "ID": 3,
        "Nombre": "Hotel Montaña",
        "Ubicacion": "Montaña",
        "Cantidad de Habitaciones": 15,
    },
    {
        "ID": 4,
        "Nombre": "Hotel Costa",
        "Ubicacion": "Costa",
        "Cantidad de Habitaciones": 25,
    },
]
clientes = [
    {"ID": 1, "Nombre": "Juan Perez", "DNI": "12345678", "Telefono": "1111-1111"},
    {"ID": 2, "Nombre": "Maria Rodriguez", "DNI": "87654321", "Telefono": "2222-2222"},
    {"ID": 3, "Nombre": "Carlos Gomez", "DNI": "45678912", "Telefono": "3333-3333"},
    {"ID": 4, "Nombre": "Laura Torres", "DNI": "98765432", "Telefono": "4444-4444"},
]
reservas = [
    {
        "ID": 1,
        "ID_cliente": 1,
        "ID_hotel": 1,
        "Numero Habitacion": 101,
        "Fecha Inicio": "01/01/2024",
        "Fecha Fin": "05/01/2024",
    },
    {
        "ID": 2,
        "ID_cliente": 2,
        "ID_hotel": 2,
        "Numero Habitacion": 202,
        "Fecha Inicio": "10/01/2024",
        "Fecha Fin": "15/01/2024",
    },
    {
        "ID": 3,
        "ID_cliente": 3,
        "ID_hotel": 1,
        "Numero Habitacion": 103,
        "Fecha Inicio": "15/01/2024",
        "Fecha Fin": "20/01/2024",
    },
    {
        "ID": 4,
        "ID_cliente": 1,
        "ID_hotel": 3,
        "Numero Habitacion": 304,
        "Fecha Inicio": "22/02/2024",
        "Fecha Fin": "25/02/2024",
    },
    {
        "ID": 5,
        "ID_cliente": 1,
        "ID_hotel": 4,
        "Numero Habitacion": 405,
        "Fecha Inicio": "01/03/2024",
        "Fecha Fin": "10/03/2024",
    },
]

if __name__ == "__main__":
    main()

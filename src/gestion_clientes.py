# Importamos las funciones necesarias de otros módulos
from utils import limpiar_pantalla
from tabulate import tabulate
import datos  # Importamos el módulo completo para acceder a guardar_datos

from colorama import Fore, Style, init

# Funciones de búsqueda y validación (Helpers)


def buscar_cliente_por_id(id_cliente: int, clientes: list) -> dict | None:
    """Función para buscar un cliente por su ID."""
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return None


def cliente_existente(dni: str, clientes: list) -> bool:
    """Función para validar si un cliente con el DNI dado ya existe."""
    for cliente in clientes:
        if cliente["dni"] == dni:
            return True
    return False


# Funciones principales del módulo


def agregar_cliente(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para agregar un nuevo cliente a la lista de clientes."""
    print(Fore.CYAN + Style.BRIGHT + "--- Agregar Cliente ---" + Style.RESET_ALL)

    # Pedimos los datos del nuevo cliente
    nombre = input(
        Fore.GREEN + "Ingrese el nombre completo del cliente: " + Style.RESET_ALL
    )

    # Validación de DNI
    while True:
        dni = input(
            Fore.GREEN + "Ingrese el DNI del cliente (solo números): " + Style.RESET_ALL
        )
        if dni.isdigit():
            if cliente_existente(dni, clientes):
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + f"\nError: Ya existe un cliente con el DNI {dni}. No se puede agregar."
                )
                input(
                    Fore.YELLOW
                    + "\nPresione Enter para volver al menú de clientes..."
                    + Style.RESET_ALL
                )
                return
            break
        else:
            print(Fore.RED + "Error: El DNI debe contener solo números.")

    telefono = input(
        Fore.GREEN + "Ingrese el número de teléfono del cliente: " + Style.RESET_ALL
    )

    # Calculamos el próximo ID disponible
    if clientes:
        id_cliente = clientes[-1]["id"] + 1
    else:
        id_cliente = 1

    nuevo_cliente = {
        "id": id_cliente,
        "nombre": nombre,
        "dni": str(dni),
        "telefono": str(telefono),
    }
    clientes.append(nuevo_cliente)
    datos.guardar_datos(hoteles, clientes, reservas)
    print(
        Fore.GREEN
        + Style.BRIGHT
        + "\n¡Cliente agregado correctamente!"
        + Style.RESET_ALL
    )


def consultar_clientes(clientes: list) -> None:
    """Funcion para mostrar la lista de clientes registrados."""
    print(Fore.CYAN + Style.BRIGHT + "--- Clientes Registrados ---" + Style.RESET_ALL)
    if clientes:
        try:
            # Preparamos los headers con color
            headers = [
                Fore.GREEN + "ID" + Style.RESET_ALL,
                Fore.GREEN + "Nombre" + Style.RESET_ALL,
                Fore.GREEN + "DNI" + Style.RESET_ALL,
                Fore.GREEN + "Teléfono" + Style.RESET_ALL,
            ]

            # Preparamos los datos de la tabla
            tabla_clientes = [
                [cliente["id"], cliente["nombre"], cliente["dni"], cliente["telefono"]]
                for cliente in clientes
            ]
            print(tabulate(tabla_clientes, headers=headers, tablefmt="grid"))

        except ImportError:
            print(
                Fore.YELLOW
                + "(Librería 'tabulate' no encontrada. Mostrando en formato simple.)"
            )
            for cliente in clientes:
                print(
                    f"ID: {cliente['id']} | Nombre: {cliente['nombre']} | DNI: {cliente['dni']} | Teléfono: {cliente['telefono']}"
                )
    else:
        print(Fore.YELLOW + "No hay clientes registrados.")


def eliminar_cliente(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para eliminar un cliente de la lista de clientes."""
    print(Fore.CYAN + Style.BRIGHT + "--- Eliminar Cliente ---" + Style.RESET_ALL)
    consultar_clientes(clientes)

    if not clientes:
        # El mensaje de "No hay clientes" ya lo da consultar_clientes
        return

    while True:
        try:
            id_a_eliminar = int(
                input(
                    Fore.GREEN
                    + "\nIngrese el ID del cliente que desea eliminar: "
                    + Style.RESET_ALL
                )
            )
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    cliente_encontrado = None
    indice_cliente = -1
    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_a_eliminar:
            cliente_encontrado = cliente
            indice_cliente = i
            break

    if cliente_encontrado:
        # Buscamos si el cliente tiene reservas asociadas
        reservas_asociadas = [r for r in reservas if r["id_cliente"] == id_a_eliminar]

        print(
            f"\nCliente a eliminar: ID: {cliente_encontrado['id']}, Nombre: {cliente_encontrado['nombre']}, DNI: {cliente_encontrado['dni']}"
        )
        if reservas_asociadas:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + f"¡Atención! Este cliente tiene {len(reservas_asociadas)} reserva(s) asociada(s)."
                + Style.RESET_ALL
            )

            opcion_reservas = input(
                Fore.GREEN
                + "¿Desea eliminar también las reservas asociadas? (s/n): "
                + Style.RESET_ALL
            )
            if opcion_reservas.lower() == "s":
                reservas[:] = [r for r in reservas if r["id_cliente"] != id_a_eliminar]
                print(Fore.YELLOW + "Las reservas asociadas serán eliminadas.")
            else:
                print(
                    Fore.YELLOW
                    + "Las reservas asociadas se mantendrán (esto puede causar inconsistencias)."
                )

        confirmacion = input(
            Fore.RED
            + Style.BRIGHT
            + f"¿Está seguro que desea eliminar este cliente? (s/n): "
            + Style.RESET_ALL
        )
        if confirmacion.lower() == "s":
            clientes.pop(indice_cliente)
            datos.guardar_datos(hoteles, clientes, reservas)
            print(Fore.GREEN + Style.BRIGHT + "Cliente eliminado correctamente.")
        else:
            print(Fore.YELLOW + "Eliminación cancelada.")
    else:
        print(Fore.RED + f"No se encontró ningún cliente con el ID {id_a_eliminar}.")


def gestionar_clientes(hoteles: list, clientes: list, reservas: list) -> None:
    """Función principal para interactuar con el menú de gestión de clientes."""

    # Inicializamos colorama para este módulo
    init(autoreset=True)

    while True:
        limpiar_pantalla()

        # Título
        titulo = " --- Gestión de Clientes --- "
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print(titulo.center(50, " "))
        print("=" * 50 + Style.RESET_ALL)

        menu_data = [
            [Fore.YELLOW + "1" + Style.RESET_ALL, "Agregar Cliente"],
            [Fore.YELLOW + "2" + Style.RESET_ALL, "Consultar Clientes"],
            [Fore.YELLOW + "3" + Style.RESET_ALL, "Eliminar Cliente"],
            [Fore.RED + "0" + Style.RESET_ALL, "Volver al menú principal"],
        ]

        # Headers para la tabla
        headers = [Fore.GREEN + "Opción", Fore.GREEN + "Acción" + Style.RESET_ALL]

        # Imprimir la tabla
        print(tabulate(menu_data, headers=headers, tablefmt="heavy_outline"))

        opcion = input(Fore.GREEN + "\nSeleccione una opción: " + Style.RESET_ALL)

        if opcion == "1":
            limpiar_pantalla()
            agregar_cliente(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "2":
            limpiar_pantalla()
            consultar_clientes(clientes)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "3":
            limpiar_pantalla()
            eliminar_cliente(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "0":
            break
        else:
            print(Fore.RED + "Opción inválida. Intente de nuevo.")
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

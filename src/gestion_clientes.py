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


def actualizar_cliente(
    clientes: list,
    id_cliente: int,
    hoteles: list | None = None,
    reservas: list | None = None,
    nombre: str | None = None,
    dni: str | None = None,
    telefono: str | None = None,
) -> bool:
    """Actualiza los datos de un cliente existente.

    - Valida unicidad de DNI (excluyendo el cliente actual).
    - Campos None no se modifican.

    Retorna True si actualizó, False si hubo problema (no existe o DNI duplicado).
    """
    cliente = buscar_cliente_por_id(id_cliente, clientes)
    if not cliente:
        return False

    if dni is not None:
        if any(c["dni"] == dni and c["id"] != id_cliente for c in clientes):
            return False

    if nombre is not None and nombre != "":
        cliente["nombre"] = nombre
    if dni is not None and dni != "":
        cliente["dni"] = str(dni)
    if telefono is not None and telefono != "":
        cliente["telefono"] = str(telefono)

    # Guardar si nos dieron listas completas
    if hoteles is not None and reservas is not None:
        datos.guardar_datos(hoteles, clientes, reservas)
    return True


def agregar_cliente(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para agregar un nuevo cliente a la lista de clientes."""
    print(Fore.CYAN + Style.BRIGHT + "--- Agregar Cliente ---" + Style.RESET_ALL)

    # Pedimos los datos del nuevo cliente
    nombre = input(Fore.GREEN + "Ingrese el nombre completo del cliente: " + Style.RESET_ALL)

    # Validación de DNI
    while True:
        dni = input(Fore.GREEN + "Ingrese el DNI del cliente (solo números): " + Style.RESET_ALL)
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

    telefono = input(Fore.GREEN + "Ingrese el número de teléfono del cliente: " + Style.RESET_ALL)

    # Calculamos el próximo ID disponible
    if clientes:
        id_cliente = max(cliente["id"] for cliente in clientes) + 1
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
    print(Fore.GREEN + Style.BRIGHT + "\n¡Cliente agregado correctamente!" + Style.RESET_ALL)


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
            print(Fore.YELLOW + "(Librería 'tabulate' no encontrada. Mostrando en formato simple.)")
            for cliente in clientes:
                print(
                    f"ID: {cliente['id']} | Nombre: {cliente['nombre']} | DNI: {cliente['dni']} | Teléfono: {cliente['telefono']}"
                )
    else:
        print(Fore.YELLOW + "No hay clientes registrados.")


def modificar_cliente(hoteles: list, clientes: list, reservas: list) -> None:
    """Interfaz interactiva para modificar un cliente."""
    print(Fore.CYAN + Style.BRIGHT + "--- Modificar Cliente ---" + Style.RESET_ALL)
    consultar_clientes(clientes)
    if not clientes:
        return

    while True:
        try:
            id_mod = int(
                input(Fore.GREEN + "\nIngrese el ID del cliente a modificar: " + Style.RESET_ALL)
            )
            break
        except ValueError:
            print(Fore.RED + "Error: Ingrese un ID numérico válido.")

    cliente = buscar_cliente_por_id(id_mod, clientes)
    if not cliente:
        print(Fore.RED + f"No se encontró cliente con ID {id_mod}.")
        return

    print(Fore.CYAN + f"Editando a: {cliente['nombre']} (DNI {cliente['dni']})")
    nuevo_nombre = input(
        Fore.GREEN + f"Nuevo nombre [{cliente['nombre']}] (Enter = dejar): " + Style.RESET_ALL
    ).strip()
    nuevo_dni = input(
        Fore.GREEN + f"Nuevo DNI [{cliente['dni']}] (Enter = dejar): " + Style.RESET_ALL
    ).strip()
    nuevo_tel = input(
        Fore.GREEN + f"Nuevo Teléfono [{cliente['telefono']}] (Enter = dejar): " + Style.RESET_ALL
    ).strip()

    # Normalizar entradas vacías a None para no modificar
    nombre_val = nuevo_nombre if nuevo_nombre != "" else None
    dni_val = nuevo_dni if nuevo_dni != "" else None
    tel_val = nuevo_tel if nuevo_tel != "" else None

    if dni_val is not None and not dni_val.isdigit():
        print(Fore.RED + "El DNI debe contener solo números.")
        return

    ok = actualizar_cliente(
        clientes,
        id_mod,
        hoteles=hoteles,
        reservas=reservas,
        nombre=nombre_val,
        dni=dni_val,
        telefono=tel_val,
    )
    if ok:
        print(Fore.GREEN + Style.BRIGHT + "Cliente actualizado correctamente.")
    else:
        print(Fore.RED + "No se pudo actualizar (ID inválido o DNI duplicado).")


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
            [Fore.YELLOW + "4" + Style.RESET_ALL, "Modificar Cliente"],
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
        elif opcion == "4":
            limpiar_pantalla()
            modificar_cliente(hoteles, clientes, reservas)
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)
        elif opcion == "0":
            break
        else:
            print(Fore.RED + "Opción inválida. Intente de nuevo.")
            input(Fore.YELLOW + "\nPresione Enter para continuar..." + Style.RESET_ALL)

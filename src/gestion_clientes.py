# Importamos las funciones necesarias de otros módulos
from utils import limpiar_pantalla
from tabulate import tabulate
import datos  # Importamos el módulo completo para acceder a guardar_datos


def cliente_existente(dni: str, clientes: list) -> bool:
    """Función para validar si un cliente con el DNI dado ya existe.

    Pre: Recibe un string con el DNI y una lista de clientes.

    Post: Devuelve True si el cliente ya existe, False en caso contrario.
    """
    for cliente in clientes:  # Recorremos la lista de clientes
        if cliente["dni"] == dni:
            return True  # Ya existe
    return False  # No existe


def agregar_cliente(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para agregar un nuevo cliente a la lista de clientes.

    Pre: Recibe las listas actuales de hoteles, clientes y reservas.

    Post: Agrega un nuevo cliente a la lista y guarda los cambios.
    """
    print("--- Agregar Cliente ---")

    # Pedimos los datos del nuevo cliente
    nombre = input("Ingrese el nombre completo del cliente: ")

    # Validación de DNI
    while True:
        dni = input("Ingrese el DNI del cliente (solo números): ")
        if dni.isdigit():  # Verificamos que solo contenga dígitos
            # Verificar si el DNI ya existe
            if cliente_existente(dni, clientes):
                print(
                    f"Error: Ya existe un cliente con el DNI {dni}. No se puede agregar."
                )  # Mensaje de error si existe
                input("\nPresione Enter para volver al menú de clientes...")
                return  # Repetimos el ciclo para pedir otro DNI
            break  # Si es dígito y no existe, salimos del bucle
        else:
            print("Error: El DNI debe contener solo números.")

    # Validación de Teléfono con numeros, guiones y espacios
    telefono = input("Ingrese el número de teléfono del cliente: ")

    # Calculamos el próximo ID disponible
    if clientes:
        id_cliente = clientes[-1]["id"] + 1  # Asignamos el siguiente ID disponible
    else:
        id_cliente = 1

    dni_str = str(dni)  # Convertimos el DNI a string para almacenarlo
    telefono_str = str(telefono)  # Convertimos el teléfono a string para almacenarlo

    nuevo_cliente = {
        "id": id_cliente,
        "nombre": nombre,
        "dni": dni_str,  # Guardamos como string
        "telefono": telefono_str,  # Guardamos como string
    }
    clientes.append(nuevo_cliente)
    datos.guardar_datos(hoteles, clientes, reservas)  # Guardamos los cambios
    print("\n¡Cliente agregado correctamente!")


def consultar_clientes(clientes: list) -> None:
    """Funcion para mostrar la lista de clientes registrados.

    Pre: Recibe la lista actual de clientes.
    """
    print("--- Clientes Registrados ---")
    if clientes:
        # Usamos tabulate para mostrar en formato tabla
        try:
            # Preparamos los datos para tabulate
            headers = ["ID", "Nombre", "DNI", "Teléfono"]
            tabla_clientes = [
                [cliente["id"], cliente["nombre"], cliente["dni"], cliente["telefono"]]
                for cliente in clientes
            ]
            print(tabulate(tabla_clientes, headers=headers, tablefmt="grid"))
        except ImportError:
            # Si no está tabulate, mostramos de forma simple
            print("(Librería 'tabulate' no encontrada. Mostrando en formato simple.)")
            for cliente in clientes:
                print(
                    f"ID: {cliente['id']} | Nombre: {cliente['nombre']} | DNI: {cliente['dni']} | Teléfono: {cliente['telefono']}"
                )
    else:
        print("No hay clientes registrados.")


def eliminar_cliente(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para eliminar un cliente de la lista de clientes.

    Pre: Recibe las listas actuales de hoteles, clientes y reservas.
    """
    print("--- Eliminar Cliente ---")
    consultar_clientes(clientes)  # Mostramos los clientes para ver IDs

    if not clientes:  # Si no hay clientes, no hay nada que eliminar
        print("No hay clientes para eliminar.")
        return

    while True:
        try:
            id_a_eliminar = int(input("Ingrese el ID del cliente que desea eliminar: "))
            break
        except ValueError:
            print("Error: Ingrese un ID numérico válido.")

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
                f"¡Atención! Este cliente tiene {len(reservas_asociadas)} reserva(s) asociada(s)."
            )

            opcion_reservas = input(
                "¿Desea eliminar también las reservas asociadas? (s/n): "
            )
            if opcion_reservas.lower() == "s":
                # Se utiliza usando listas por comprensión para eliminar las reservas asociadas
                # Se actualiza la lista original de reservas por una lista filtrada que excluye las reservas del cliente eliminado
                reservas[:] = [r for r in reservas if r["id_cliente"] != id_a_eliminar]
                print("Las reservas asociadas serán eliminadas.")
            else:
                print("Las reservas asociadas se mantendrán.")

        confirmacion = input(f"¿Está seguro que desea eliminar este cliente? (s/n): ")
        if confirmacion.lower() == "s":
            # Eliminamos usando el índice para mayor seguridad
            # Eliminamos el cliente usando pop en lugar de del para eliminar por índice
            clientes.pop(indice_cliente)
            datos.guardar_datos(hoteles, clientes, reservas)  # Guardamos los cambios
            print("Cliente eliminado correctamente.")
        else:
            print("Eliminación cancelada.")
    else:
        print(f"No se encontró ningún cliente con el ID {id_a_eliminar}.")


def gestionar_clientes(hoteles: list, clientes: list, reservas: list) -> None:
    """Función principal para interactuar con el menú de gestión de clientes.

    Pre: Recibe las listas actuales de hoteles, clientes y reservas.
    """
    while True:
        limpiar_pantalla()
        print("=" * 40)
        print("      --- Gestión de Clientes ---     ".center(40, " "))
        print("=" * 40)
        print("1. Agregar Cliente")
        print("2. Consultar Clientes")
        print("3. Eliminar Cliente")
        print("0. Volver al menú principal")
        print("=" * 40)

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            limpiar_pantalla()
            agregar_cliente(hoteles, clientes, reservas)
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            limpiar_pantalla()
            consultar_clientes(clientes)
            input("\nPresione Enter para continuar...")
        elif opcion == "3":
            limpiar_pantalla()
            eliminar_cliente(hoteles, clientes, reservas)
            input("\nPresione Enter para continuar...")
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

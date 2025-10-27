from utils import limpiar_pantalla
import datos  # Importamos el módulo completo para acceder a guardar_datos


def agregar_hotel(hoteles, clientes, reservas) -> None:
    """Funcion para agregar un nuevo hotel a la lista de hoteles y guarda los cambios.

    Pre: Recibe las listas actuales de hoteles, clientes y reservas.

    Post: Agrega un nuevo hotel a la lista y guarda los datos actualizados.
    """
    print("--- Agregar Hotel ---")
    nombre_hotel = input("Ingrese el nombre del hotel: ")  # Pedimos el nombre del hotel
    nombre_hotel = (
        nombre_hotel.lower().title()
    )  # Formateamos el nombre del hotel para que la primera letra de cada palabra sea mayúscula
    ubicacion = input(
        "Ingrese la ciudad donde se encuentra el hotel: "
    )  # Pedimos la ubicación del hotel

    # Pedimos las habitaciones del hotel, para eso vamos a necesitar una lista de habitaciones
    lista_habitaciones = []

    while True:
        try:
            # Pedimos la cantidad de habitaciones a agregar
            num_habitaciones_a_agregar = int(
                input("¿Cuántas habitaciones desea agregar a este hotel?: ")
            )

            if (
                num_habitaciones_a_agregar < 0
            ):  # Si la cantidad es negativa, mostramos un error
                print("Por favor, ingrese un número positivo.")
                continue
            break
        except (
            ValueError
        ):  # Si el usuario ingresa algo que no sea un número, mostramos un error
            print("Error: Ingrese un número válido.")

    for i in range(
        num_habitaciones_a_agregar
    ):  # Recorremos la cantidad de habitaciones a agregar
        print(f"\n--- Agregando Habitación {i+1} ---")

        # Pedimos el nuumero de la habitación
        while True:
            try:
                numero = int(
                    input(f"Número de la habitación {i+1}: ")
                )  # Pedimos el número de la habitación

                # Verificamos que no exista otra habitación con el mismo número en el hotel
                if any(
                    h["numero"] == numero for h in lista_habitaciones
                ):  # Si existe una habitación con el mismo número, mostramos un error
                    print(
                        f"Error: Ya existe una habitación con el número {numero} en este hotel."
                    )
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número válido.")

        # Pedimos la capacidad de la habitación
        while True:
            try:
                capacidad = int(
                    input(f"Capacidad de la habitación {numero}: ")
                )  # Se pide la capacidad de la habitación
                if (
                    capacidad <= 0
                ):  # Si la capacidad es menor o igual a cero, mostramos un error
                    print("La capacidad debe ser mayor a cero.")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número válido.")

        # Pedimos el precio por noche de la habitación
        while True:
            try:
                precio = float(
                    input(f"Precio por noche de la habitación {numero}: ")
                )  # Se pide el precio por noche de la habitación
                if (
                    precio <= 0
                ):  # Si el precio es menor o igual a cero, mostramos un error
                    print("El precio debe ser mayor a cero.")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número válido.")

        # Agregamos la habitación a la lista de habitaciones del hotel
        lista_habitaciones.append(
            {"numero": numero, "capacidad": capacidad, "precio": precio}
        )

    # Calculamos el próximo ID disponible
    if hoteles:
        id_hotel = (
            max(h["id"] for h in hoteles) + 1
        )  # El ID va a ser el máximo ID actual + 1
    else:
        id_hotel = 1  # Si no hay hoteles, el id es uno

    # Se crea el nuevo hotel con su información
    nuevo_hotel = {
        "id": id_hotel,
        "nombre": nombre_hotel,
        "ubicacion": ubicacion,
        "habitaciones": lista_habitaciones,
    }
    hoteles.append(nuevo_hotel)  # Agregamos el nuevo hotel a la lista de hoteles

    datos.guardar_datos(hoteles, clientes, reservas)  # Guardamos los cambios
    print("\n¡Hotel agregado correctamente!")


def consultar_hoteles(hoteles: list) -> None:
    """Funcion para mostrar la lista de hoteles registrados.

    Pre: Recibe la lista actual de hoteles.
    """
    print("--- Hoteles Registrados ---")
    if hoteles:  # Si hay hoteles registrados
        for hotel in hoteles:  # Recorremos la lista de hoteles
            print(
                f"\nID: {hotel['id']} | Nombre: {hotel['nombre']} | Ubicación: {hotel['ubicacion']}"
            )  # Mostramos la información básica del hotel
            print("  Habitaciones:")
            if hotel["habitaciones"]:  # Si el hotel tiene habitaciones registradas
                for hab in hotel[
                    "habitaciones"
                ]:  # Mostramos la información de cada habitación
                    print(
                        f"    - Número: {hab['numero']}, Capacidad: {hab['capacidad']}, Precio: ${hab['precio']:.2f}"
                    )
            else:
                print("El hotel no tiene habitaciones registradas.")
    else:
        print("No hay hoteles registrados.")


def eliminar_hotel(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para eliminar un hotel de la lista por su ID o nombre y guardar los cambios.

    Pre: Recibe las listas actuales de hoteles, clientes y reservas.
    """
    print("--- Eliminar Hotel ---")
    consultar_hoteles(hoteles)  # Mostramos los hoteles para que el usuario vea los IDs

    if not hoteles:  # Si no hay hoteles, no tiene sentido seguir
        print("No hay hoteles para eliminar.")
        return  # Devuelve None

    entrada = input(
        "Ingrese el ID o el nombre del hotel que desea eliminar: "
    )  # Pedimos el ID o nombre del hotel a eliminar, se elimina espacios en blanco al inicio y final
    if not entrada:  # Si la entrada está vacía, mostramos un error
        print("Entrada vacía. Operación cancelada.")
        return  # Devuelve None

    # Intentamos interpretar como ID numérico
    hotel_encontrado = None

    try:
        id_a_eliminar = int(entrada)  # Convertimos la entrada a entero
        for hotel in hoteles:  # Recorremos la lista de hoteles
            if (
                hotel["id"] == id_a_eliminar
            ):  # Si encontramos el hotel con el ID ingresado
                hotel_encontrado = hotel  # Lo guardamos
                break
        if not hotel_encontrado:  # Si no, se le informa al usuario
            print(f"No se encontró ningún hotel con el ID {id_a_eliminar}.")
            return  # Devuelve None
    except ValueError:  # Si no se puede convertir a entero
        # Buscamos por nombre, sin diferenciar entre mayusculas y minusculas, no case-sensitive
        nombre_buscar = (
            entrada.lower()
        )  # Convertimos la entrada a minusculas y la guardamos
        coincidencias = [
            h for h in hoteles if h["nombre"].lower() == nombre_buscar
        ]  # Buscamos por coincidencias en la lista hoteles y las almacenamos

        if len(coincidencias) == 0:  # Si no hay coincidencias. Informamos al usuario
            print(f"No se encontró ningún hotel con el nombre '{entrada}'.")
            return  # Devuelve None
        elif len(coincidencias) == 1:  # Si hay una sola coincidencia
            hotel_encontrado = coincidencias[0]
        else:
            # Si hay varias coincidencias, mostramos opciones para que el usuario elija por ID
            print(
                f"Se encontraron {len(coincidencias)} hoteles con el nombre '{entrada}':"
            )  # Informamos la cantidad de hoteles encontrados
            for h in coincidencias:
                print(
                    f"  ID: {h['id']} | Nombre: {h['nombre']} | Ubicación: {h.get('ubicacion', 'N/A')}"
                )  # Mostramos la informacion de los hoteles encontrados

            while True:
                try:
                    # Solicitamos al usuario que ingrese el ID del hotel que desea eliminar
                    id_elegido = int(
                        input(
                            "Ingrese el ID del hotel que desea eliminar de las opciones anteriores: "
                        )
                    )
                except ValueError:  # Si el usuario ingresa algo que no es un número
                    print("Error: Ingrese un ID numérico válido.")
                    continue

                # Buscamos el hotel con el ID elegido entre las coincidencias encontradas
                hotel_encontrado = next(
                    (h for h in coincidencias if h["id"] == id_elegido), None
                )

                # Si encontramos el hotel, salimos del bucle
                if hotel_encontrado:
                    break
                else:  # Si no, se informa al usuario el ID no valido y se vuelve a solicitar
                    print("ID no válido. Elija un ID de la lista mostrada.")

    # Solicitamos confirmación antes de eliminar el hotel
    confirmacion = input(
        f"¿Está seguro que desea eliminar el hotel '{hotel_encontrado['nombre']}' (ID: {hotel_encontrado['id']})? (s/n): "
    )
    if confirmacion.lower() == "s":  # Si el usuario confirma
        hoteles.remove(hotel_encontrado)  # Eliminamos el hotel de la lista
        datos.guardar_datos(
            hoteles, clientes, reservas
        )  # Guardamos los cambios en el archivo
        print("Hotel eliminado correctamente.")
    else:
        print("Eliminación cancelada.")


def gestionar_hoteles(hoteles: list, clientes: list, reservas: list) -> None:
    """Función principal para interactuar con el menú de gestión de hoteles.

    Pre: Recibe las listas actuales de hoteles, clientes y reservas.
    """
    while True:
        limpiar_pantalla()
        print("=" * 40)
        print("      --- Gestión de Hoteles ---      ".center(40, " "))
        print("=" * 40)
        print("1. Agregar hotel")
        print("2. Consultar hoteles")
        print("3. Eliminar hotel")
        print("0. Volver al menú principal")
        print("=" * 40)

        opcion = input("Ingrese la opción que quiere ejecutar: ")
        if opcion == "1":
            limpiar_pantalla()
            # Llamamos a agregar_hotel pasando las listas existentes
            agregar_hotel(hoteles, clientes, reservas)
            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            limpiar_pantalla()
            consultar_hoteles(hoteles)  # Solo necesita la lista de hoteles
            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            limpiar_pantalla()
            # Pasamos las listas para que eliminar_hotel pueda guardarlas
            eliminar_hotel(hoteles, clientes, reservas)
            input("\nPresione Enter para continuar...")

        elif opcion == "0":
            break

        else:
            print("Opción inválida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

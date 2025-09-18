import re

def menu():
    # Muestra las opciones del menú principal
    print("1. Gestion de Hoteles")
    print("2. Gestion de Clientes")
    print("3. Gestion de Reservas")
    print("4. Gestionar Reportes")
    print("0. Salir")

def validar_cliente(nombre_cliente: str) -> int:
    """Funcion para validar si un cliente existe

    Pre: Recibe un string con el nombre del cliente que se debe buscar

    Post: Retorna el ID del cliente si se encontro, o 0 si no se encontro
    
    """
    # Recorremos la lista de clientes buscando un cliente con dicho nombre
    for cliente in clientes:
        if cliente["Nombre"] == nombre_cliente: # Si se encuentra el cliente, la funcion devuelve su ID
            return cliente["ID"]
    return 0

def validar_hotel(nombre_hotel: str) -> int:
    """Funcion para validar si un hotel existe

    Pre: Recibe un string con el nombre del hotel que se debe buscar

    Post: Retorna el ID del hotel si se encontro, o 0 si no se encontro
    
    """
    # Recorremos la lista de hoteles buscando un hotel con dicho nombre
    for hotel in hoteles:
        if hotel["Nombre"] == nombre_hotel: # Si se encuentra el hotel, la funcion devuelve su ID
            return hotel["ID"]
    return 0

def validar_fecha(fecha: str) -> bool:
    """Funcion para validar que una fecha tenga el formato correcto

    Pre: Recibe un string con la fecha a validar

    Post: Retorna un booleano de valor True si la fecha es valida, o False si no lo es

    Se realiza a partir de expresiones regulares, que se basan en las siguientes reglas:
    El formato debe ser DD/MM/AAAA
        Teniendo en cuenta que:
        DD puede ser un numero del 01 al 31 -
        MM puede ser un numero del 01 al 12 - 
        AAAA puede ser un numero del 1000 al 9999
    """
    # Definimos el patron que debe cumplir la fecha
    patron = r"^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/[1-9]\d{3}$"
    if not re.match(patron, fecha):
        return False

    # Validamos dias segun mes y año bisiesto
    dia, mes, anio = map(int, fecha.split("/"))
    
    if mes == 2: # Febrero, puede variar si es bisiesto o no
        # Un año es bisiesto si es divisible por 4, pero no por 100, a menos que sea divisible por 400
        es_bisiesto = (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0))
        
        if es_bisiesto and dia > 29: # Si es bisiesto, febrero tiene 29 dias
            return False
        if not es_bisiesto and dia > 28: # Si no es bisiesto, febrero tiene 28 dias
            return False
    
    elif mes in [4, 6, 9, 11] and dia > 30: # Abril, Junio, Septiembre y Noviembre tienen 30 dias
        return False
    elif dia > 31: # Los demas meses tienen 31 dias
        return False
    return True

def gestionar_hoteles():
    while True:
        print("\n--- Gestión de Hoteles ---")
        print("1. Agregar hotel")
        print("2. Consultar hoteles")
        print("3. Eliminar hotel")
        print("4. Salir al menu principal")

        opcion = int(input("Ingrese la opcion que quiere llevar a cabo: "))
        if opcion == 1:
            agregar_hotel()
        elif opcion == 2:
            consultar_hotel()
        elif opcion == 3:
            eliminar_hotel()
        elif opcion == 4:
            break
        else:
            print("Valor invalido")



def agregar_hotel():
    hotel = input("Ingrese el nombre del hotel: ")
    localidad = input("Ingrese la ciudad donde se encuentra el hotel: ")
    habitaciones = int(input("Ingrese la cantidad de habitaciones que tiene el hotel: "))
    id_hotel = len(hoteles) + 1
    hoteles.append({"ID":id_hotel,"Nombre":hotel,"Ubicacion":localidad,"Cantidad de Habitaciones":habitaciones})
    print("Hotel agregado correctamente")
    
def consultar_hotel():
    for hotel in hoteles:
        if len(hotel) > 0:
            print(hotel)
        else:
            print("No hay hoteles registrados")

def eliminar_hotel():
    borrar = input("Ingrese el hotel a eliminar: ")
    for hotel in hoteles:
        if borrar == hotel["Nombre"]:
            hoteles.remove(hotel)
            print("Hotel eliminado exitosamente")

def gestionar_clientes():
    # TODO: Implementar la funcionalidad para gestionar clientes
    print("Funcionalidad para gestionar clientes (pendiente de implementar)")

def gestionar_reservas():
    """Funcionalidad para gestionar reservas

    Al ser invocada, esta funcion permite al usuario ver las opciones
    para agregar, buscar o eliminar reservas.
    """

    while True:
         print("\n--- Gestión de Reservas ---")
         print("1. Agregar Reserva")
         print("2. Consultar Reservas")
         print("3. Eliminar Reserva")
         print("0. Volver al menu principal")

         opcion = input("Seleccione una opcion: ")
         if opcion == "1":
            agregar_reserva()
         elif opcion == "2":
            consultar_reservas()
         elif opcion == "3":
            eliminar_reserva()
         elif opcion == "0":
            break
         else:
            print("Opcion invalida")

def agregar_reserva():
    """Funcionalidad para agregar reservas

    Al ser invocada, esta funcion permite al usuario ingresar los datos
    para crear una nueva reserva.
    """
    cliente = validar_cliente(input("Ingrese el nombre del cliente: "))
    if cliente == 0:
        print("No se encontro un cliente con ese nombre. Primero debe agregar el cliente.")
        return # Usamos un return para salir de la funcion
    
    hotel = validar_hotel(input("Ingrese el nombre del hotel: "))
    if hotel == 0:
        print("No se encontro un hotel con ese nombre. Primero debe agregar el hotel.")
        return # Usamos un return para salir de la funcion

    # TODO validar que la habitacion exista en el hotel anteriormente indicado
    numero_habitacion = input("Ingrese el numero de habitacion: ")

    # TODO validar que la habitacion no este reservada en las fechas indicadas
    fecha_entrada = input("Ingrese la fecha de entrada (DD/MM/AAAA): ")
    while not validar_fecha(fecha_entrada): # Validamos que la fecha tenga el formato correcto invocando la funcion validar_fecha
        print("Fecha invalida. Intente de nuevo.")
        fecha_entrada = input("Ingrese la fecha de entrada (DD/MM/AAAA): ")

    fecha_salida = input("Ingrese la fecha de salida (DD/MM/AAAA): ")
    while not validar_fecha(fecha_salida): # Validamos que la fecha tenga el formato correcto invocando la funcion validar_fecha
        print("Fecha invalida. Intente de nuevo.")
        fecha_salida = input("Ingrese la fecha de salida (DD/MM/AAAA): ")

    # Agregamos la nueva reserva a la lista de reservas si todo fue correcto
    id_reserva = len(reservas) + 1 # Se genera un ID para la reserva sumando 1 a la cantidad de reservas actuales
    reservas.append({"ID": id_reserva, "ID_cliente":cliente,"ID_hotel":hotel,"Numero Habitacion":numero_habitacion,"Fecha Inicio":fecha_entrada,"Fecha Fin":fecha_salida})

    print("Reserva agregada correctamente")

def buscar_reserva_x_cliente(): # Esta funcion fue renombrada, se usara mas adelante en la seccion de reportes. Actualmente no se invoca en ningun lado
    """Funcionalidad para buscar las reservas de un cliente

    Al ser invocada, esta funcion permite al usuario ingresar el nombre
    de un cliente para buscar reservas a su nombre.
    """
    reservas_cliente = [] # Lista que almacenara las reservas del cliente

    # Solicitamos el nombre del cliente
    nombre_cliente = input("Ingrese el nombre del cliente para buscar sus reservas: ")
    ID_cliente = validar_cliente(nombre_cliente)

    if ID_cliente == 0: # Si no encontramos al cliente, informamos por pantalla
        print("No se encontro un cliente con ese nombre")
    else: # Si encontramos al cliente, buscamos por reservas con su ID
        for reserva in reservas:
            if ID_cliente == reserva["ID_cliente"]:
                reservas_cliente.append(reserva) # Si encontramos una reserva que coincida, la agregamos a la lista
    
        # Si hay reservas, las mostramos por pantalla
        if reservas_cliente:
            print(f"Reservas encontradas para {nombre_cliente}:")
            for reserva in reservas_cliente:
                print(reserva)
        else: # En caso de no haber reservas, lo informamos igualmente
            print("No se encontraron reservas para ese cliente")

def consultar_reservas():
    """Funcionalidad para buscar las reservas existentes

    Al ser invocada se muestra por pantalla la lista de reservas existentes
    """
    if reservas: # Si existen reservas, se muestran por pantalla
        print("Reservas existentes:")
        for reserva in reservas:
            # Buscar el nombre del cliente por ID
            nombre_cliente = "Desconocido"
            for cliente in clientes:
                if cliente["ID"] == reserva["ID_cliente"]:
                    nombre_cliente = cliente["Nombre"]
                    break

            # Buscar el nombre del hotel por ID
            nombre_hotel = "Desconocido"
            for hotel in hoteles:
                if hotel["ID"] == reserva["ID_hotel"]:
                    nombre_hotel = hotel["Nombre"]
                    break

            print(f"Cliente: {nombre_cliente} ({reserva['ID_cliente']}), Hotel: {nombre_hotel} ({reserva['ID_hotel']}), Habitación: {reserva['Numero Habitacion']}, Fecha Inicio: {reserva['Fecha Inicio']}, Fecha Fin: {reserva['Fecha Fin']}")
    else:
        print("No hay reservas existentes.")

def eliminar_reserva():
    """Funcionalidad para eliminar reservas de un cliente

    Al ser invocada, esta funcion permite al usuario ingresar el id de una reserva
    para eliminar la misma.
    """
    confirmacion = False # Esta variable almacena la confirmacion del usuario para eliminar la reserva, por defecto False

    # Solicitamos el ID de la reserva a eliminar
    id_reserva = int(input("Ingrese el ID de la reserva que desea eliminar: "))

    # Recorremos reservas buscand una reserva con el ID indicado
    for reserva in reservas: 
        if id_reserva == reserva["ID"]: # Si se encuentra la reserva, se pide confirmacion al usuario para eliminarla
            confirmacion = input(f"Esta seguro que desea eliminar la reserva {reserva}? (s/n): ")
            if confirmacion.lower() == "s": # Para evitar problemas convertimos la respuesta a minusculas, si es "s" se elimina la reserva
                reservas.remove(reserva)
                print("Reserva eliminada correctamente.")
            break
    else:
        print("No se encontro una reserva con ese ID.")

def generar_reportes():
    # TODO: Implementar la funcionalidad para generar reportes
    print("Funcionalidad para generar reportes (pendiente de implementar)")

def main():
    # Función principal que inicia la aplicación
    print("Bienvenido a SRG - Sistema de Registro de Hoteleria")
    
    menu()
    opcion = input("Seleccione una opcion: ")

    while True:
        if opcion == '1':
            gestionar_hoteles()
        elif opcion == '2':
            gestionar_clientes()
        elif opcion == '3':
            gestionar_reservas()
        elif opcion == '4':
            generar_reportes()
        elif opcion == '0':
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion no valida. Intente de nuevo.")
        
        menu()
        opcion = input("Seleccione una opcion: ")

# Datos de ejemplo para pruebas
hoteles = [
    {"ID": 1, "Nombre": "Hotel Sol", "Ubicacion": "Ciudad", "Cantidad de Habitaciones": 20},
    {"ID": 2, "Nombre": "Hotel Luna", "Ubicacion": "Playa", "Cantidad de Habitaciones": 30},
    {"ID": 3, "Nombre": "Hotel Montaña", "Ubicacion": "Montaña", "Cantidad de Habitaciones": 15},
    {"ID": 4, "Nombre": "Hotel Costa", "Ubicacion": "Costa", "Cantidad de Habitaciones": 25}
]
clientes = [
    {"ID": 1, "Nombre": "Juan Perez", "DNI": "12345678", "Telefono": "1111-1111"},
    {"ID": 2, "Nombre": "Maria Rodriguez", "DNI": "87654321", "Telefono": "2222-2222"},
    {"ID": 3, "Nombre": "Carlos Gomez", "DNI": "45678912", "Telefono": "3333-3333"},
    {"ID": 4, "Nombre": "Laura Torres", "DNI": "98765432", "Telefono": "4444-4444"}
]
reservas = [
    {"ID": 1, "ID_cliente": 1, "ID_hotel": 1, "Numero Habitacion": 101, "Fecha Inicio": "01/01/2024", "Fecha Fin": "05/01/2024"},
    {"ID": 2, "ID_cliente": 2, "ID_hotel": 2, "Numero Habitacion": 202, "Fecha Inicio": "10/01/2024", "Fecha Fin": "15/01/2024"},
    {"ID": 3, "ID_cliente": 3, "ID_hotel": 1, "Numero Habitacion": 103, "Fecha Inicio": "15/01/2024", "Fecha Fin": "20/01/2024"},
    {"ID": 4, "ID_cliente": 1, "ID_hotel": 3, "Numero Habitacion": 304, "Fecha Inicio": "22/02/2024", "Fecha Fin": "25/02/2024"},
    {"ID": 5, "ID_cliente": 1, "ID_hotel": 4, "Numero Habitacion": 405, "Fecha Inicio": "01/03/2024", "Fecha Fin": "10/03/2024"}
]

if __name__ == "__main__":
    main()
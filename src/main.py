def menu():
    # Muestra las opciones del menú principal
    print("1. Gestion de Hoteles")
    print("2. Gestion de Clientes")
    print("3. Gestion de Reservas")
    print("4. Gestionar Reportes")
    print("0. Salir")

def gestionar_hoteles():
    # TODO: Implementar la funcionalidad para gestionar hoteles
    print("Funcionalidad para gestionar hoteles (pendiente de implementar)")

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
         print("2. Buscar Reserva")
         print("3. Eliminar Reserva")
         print("0. Volver al menu principal")

         opcion = input("Seleccione una opcion: ")
         if opcion == "1":
            agregar_reserva()
         elif opcion == "2":
            buscar_reserva()
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
    cliente = input("Ingrese el nombre del cliente: ")

    hotel = input("Ingrese el nombre del hotel: ")
    fecha_entrada = input("Ingrese la fecha de entrada (DD/MM/AAAA): ")
    fecha_salida = input("Ingrese la fecha de salida (DD/MM/AAAA): ")

    reservas.append({"ID_cliente":cliente,"ID_hotel":hotel,"Fecha Entrada":fecha_entrada,"Fecha Salida":fecha_salida})
    
    print("Reserva agregada correctamente")

def buscar_reserva():
    """Funcionalidad para buscar las reservas de un cliente

    Al ser invocada, esta funcion permite al usuario ingresar el nombre
    de un cliente para buscar reservas a su nombre.
    """
    reservas_cliente = []

    nombre_cliente = input("Ingrese el nombre del cliente para buscar su/sus reserva/s: ")

    for reserva in reservas:
        if nombre_cliente == reserva["Cliente"]:
            reservas_cliente.append(reserva)
    
    if reservas_cliente:
        print(f"Reservas encontradas para {nombre_cliente}:")
        for reserva in reservas_cliente:
            print(reserva)
    else:
        print("No se encontraron reservas para ese cliente")

def eliminar_reserva(): # TODO: Implementar la funcionalidad para eliminar reservas
   borrar = input("Ingrese el nombre del cliente para eliminar su/sus reserva/s: ")

   for reserva in reservas:
      if borrar == reserva["Cliente"]:
         reservas.remove(reserva)
         print("Reserva eliminada correctamente")
         break
   else:
      print("No se encontro una reserva para ese cliente")

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
    {"ID": 3, "Nombre": "Carlos Gomez", "DNI": "45678912", "Telefono": "3333-3333"}
]
reservas = [
    {"ID": 1, "ID_cliente": 1, "ID_hotel": 1, "Fecha Entrada": "01/01/2024", "Fecha Salida": "05/01/2024"},
    {"ID": 2, "ID_cliente": 2, "ID_hotel": 2, "Fecha Entrada": "10/01/2024", "Fecha Salida": "15/01/2024"},
    {"ID": 3, "ID_cliente": 3, "ID_hotel": 1, "Fecha Entrada": "15/01/2024", "Fecha Salida": "20/01/2024"},
    {"ID": 4, "ID_cliente": 1, "ID_hotel": 3, "Fecha Entrada": "22/02/2024", "Fecha Salida": "25/02/2024"},
    {"ID": 5, "ID_cliente": 1, "ID_hotel": 4, "Fecha Entrada": "01/03/2024", "Fecha Salida": "10/03/2024"}
]

if __name__ == "__main__":
    main()
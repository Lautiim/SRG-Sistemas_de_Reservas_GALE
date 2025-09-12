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
    # TODO: Implementar la funcionalidad para gestionar reservas
    print("Funcionalidad para gestionar reservas (pendiente de implementar)")

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

if __name__ == "__main__":
    main()
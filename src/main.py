def registrar_hotel():
    print("Funcionalidad para registrar hotel (pendiente de implementar)")

def menu():
    print("1. Registrar Cliente")
    print("2. Registrar Habitacion")
    print("3. Registrar Reserva")
    print("4. Salir")

def main():
    print("Binevenido a SRG - Sistema de Registro de Hoteleria")

    menu()
    opcion = input("Seleccione una opcion: ")
    
    if opcion == "1":
        registrar_hotel()

if __name__ == "__main__":
    main()
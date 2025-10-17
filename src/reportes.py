def generar_reportes() -> None:
    """Funcion para interactuar con el menú de generación de reportes.
    
    Al ser invocada, esta funcion permite al usuario ver las opciones
    para generar reportes.
    """
    while True:
        limpiar_pantalla()
        print("="*40)
        print("   --- Generación de Reportes ---     ".center(40, " "))
        print("="*40)
        print("1. Consultar hoteles")
        print("2. Consultar clientes")
        print("3. Consultar reservas")
        print("4. Consultar reservas por cliente")
        print("5. Consultar reservas por hotel")
        print("6. Consultar habitaciones disponibles en un hotel")
        print("0. Volver al menú principal")
        print("="*40)

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
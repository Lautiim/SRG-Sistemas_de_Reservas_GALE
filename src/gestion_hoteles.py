def gestionar_hoteles() -> None:
    """Funcion para interactuar con el menú de gestión de hoteles.

    Al ser invocada, esta funcion permite al usuario ver las opciones
    para agregar, buscar o eliminar hoteles.
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

        opcion = int(input("Ingrese la opción que quiere llevar a cabo: "))
        if opcion == 1:
            limpiar_pantalla()
            agregar_hotel()
            input("\nPresione Enter para continuar...")
        elif opcion == 2:
            limpiar_pantalla()
            consultar_hoteles()
            input("\nPresione Enter para continuar...")
        elif opcion == 3:
            limpiar_pantalla()
            eliminar_hotel()
            input("\nPresione Enter para continuar...")
        elif opcion == 0:
            break
        else:
            print("Valor inválido")
            input("\nPresione Enter para continuar...")

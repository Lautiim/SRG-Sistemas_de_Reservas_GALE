def gestionar_clientes() -> None:
    """Funcion para interactuar con el menú de gestión de clientes.

    Al ser invocada, esta funcion permite al usuario ver las opciones
    para agregar, buscar o eliminar clientes.
    """
    while True:
        limpiar_pantalla()
        print("="*40)
        print("      --- Gestión de Clientes ---     ".center(40, " "))
        print("="*40)
        print("1. Agregar Cliente")
        print("2. Consultar cliente")
        print("3. Eliminar cliente")
        print("0. Volver al menú principal")
        print("="*40)

        opcion = int(input("Seleccione una opción: "))
        if opcion == 1:
            limpiar_pantalla()
            agregar_cliente()
            input("\nPresione Enter para continuar...")
        elif opcion == 2:
            limpiar_pantalla()
            consultar_clientes()
            input("\nPresione Enter para continuar...")
        elif opcion == 3:
            limpiar_pantalla()
            eliminar_cliente()
            input("\nPresione Enter para continuar...")
        elif opcion == 0:
            break
        else:
            print("Opción inválida")
            input("\nPresione Enter para continuar...")

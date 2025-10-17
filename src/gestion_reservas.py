def gestionar_reservas() -> None:
   """Funcion para interactuar con el menú de gestión de reservas.

   Al ser invocada, esta funcion permite al usuario ver las opciones
   para agregar, buscar o eliminar reservas.
   """
   while True:
         limpiar_pantalla()
         print("="*40)
         print("     --- Gestión de Reservas ---      ".center(40, " "))
         print("="*40)
         print("1. Agregar Reserva")
         print("2. Consultar Reservas")
         print("3. Eliminar Reserva")
         print("0. Volver al menú principal")
         print("="*40)

         opcion = input("Seleccione una opción: ")
         if opcion == "1":
            limpiar_pantalla()
            agregar_reserva()
            input("\nPresione Enter para continuar...")
         elif opcion == "2":
            limpiar_pantalla()
            consultar_reservas()
            input("\nPresione Enter para continuar...")
         elif opcion == "3":
            limpiar_pantalla()
            eliminar_reserva()
            input("\nPresione Enter para continuar...")
         elif opcion == "0":
            break
         else:
            print("Opción inválida")
            input("\nPresione Enter para continuar...")
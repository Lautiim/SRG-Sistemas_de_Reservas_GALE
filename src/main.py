# Importamos los módulos del sistema
import datos
import gestion_hoteles
import gestion_clientes
import gestion_reservas
import reportes
from utils import limpiar_pantalla
import os

def menu():
    """Función que muestra el menú principal del sistema."""
    limpiar_pantalla()
    print("=" * 40)
    print(" SRG - Sistema de Registro de Hotelería ".center(40, " "))
    print("=" * 40)
    print("1. Gestión de Hoteles")
    print("2. Gestión de Clientes")
    print("3. Gestión de Reservas")
    print("4. Generar Reportes")
    print("5. Exportar datos a CSV")
    print("0. Salir")
    print("=" * 40)

def main():
    """Función principal que inicia y controla el flujo del sistema."""
    # Se cargan los datos iniciales desde el módulo de datos.
    hoteles, clientes, reservas = datos.cargar_datos()

    print("Bienvenido a SRG - Sistema de Registro de Hotelería")
    input("Presione Enter para comenzar...") # Pausa inicial

    while True:
        menu() # Mostramos el menú
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Llamamos a la función principal del módulo de hoteles,
            # pasándole las listas de datos para que pueda usarlas y modificarlas.
            gestion_hoteles.gestionar_hoteles(hoteles, clientes, reservas)
        elif opcion == "2":
            # Hacemos lo mismo para el módulo de clientes.
            gestion_clientes.gestionar_clientes(hoteles, clientes, reservas)
        elif opcion == "3":
            # Y para el módulo de reservas.
            gestion_reservas.gestionar_reservas(hoteles, clientes, reservas)
        elif opcion == "4":
            # Y para el módulo de reportes.
            reportes.generar_reportes(hoteles, clientes, reservas)
        elif opcion == "5":
            # Y para la exportación a CSV.
            reportes.exportar_datos_csv(hoteles, clientes, reservas)
        elif opcion == "0":
            limpiar_pantalla()
            print("=" * 40)
            print(" Gracias por usar SRG ".center(40, "="))
            print(" Saliendo del sistema... ".center(40, " "))
            print("=" * 40)
            break # Salimos del bucle y terminamos el programa
        else:
            print("Opción no válida. Intente de nuevo.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
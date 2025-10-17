import os
from datetime import datetime

def limpiar_pantalla() -> None:
    """Funcion para limpiar la pantalla de la consola.

    Funciona tanto en Windows ("cls") como en Unix ("clear").
    """
    os.system("cls" if os.name == "nt" else "clear") # Si el sistema operativo es Windows, usa "cls", sino usa "clear"

def validar_fecha(fecha_str: str) -> bool:
    """Funcion para validar si una cadena de texto es una fecha válida en formato 'YYYY-MM-DD'.

    Pre: Recibe un string con la fecha a validar

    Post: Retorna un booleano de valor True si la fecha es valida, o False si no lo es
    """
    try:
        # Convierte el String en un objeto datetime, si no puede, lanza una excepcion
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    # Pruebas de las funciones
    limpiar_pantalla()
    print("Prueba de la función limpiar_pantalla()")
    input("Presiona Enter para continuar...")

    fechas_a_probar = ["2023-10-15", "2023-02-30", "15-10-2023", "2023/10/15", "2023-13-01"]
    for fecha in fechas_a_probar:
        es_valida = validar_fecha(fecha)
        print(f"La fecha '{fecha}' es válida: {es_valida}")
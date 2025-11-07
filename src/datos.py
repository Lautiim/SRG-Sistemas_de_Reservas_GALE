import json
import os
import datos
from utils import limpiar_pantalla
from reportes import exportar_clientes_csv, exportar_reservas_csv, exportar_hoteles_csv



def leer_archivo(ruta: str) -> list:
    """Función para leer un archivo JSON

    Pre: Recibe la ruta del archivo JSON a leer en formato string

    Post: Devuelve una lista con los datos del archivo JSON.
    En caso de error (archivo no existe o corrupto), devuelve una lista vacía.
    """
    try:  # Intentamos abrir el archivo
        with open(
            ruta, "r", encoding="utf-8"
        ) as archivo:  # Abrimos el archivo en modo lectura con UTF-8
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):  # Si no existe o está corrupto
        return []  # Devolvemos una lista vacía


def cargar_datos() -> tuple[list, list, list]:
    """Función para cargar los datos desde los archivos JSON en /data.

    Post: Devuelve una tupla con la información de hoteles, clientes y reservas.
    """
    # Comprobamos que el directorio con los datos exista
    try:
        os.makedirs(RUTA_DATA, exist_ok=True)  # Creamos el directorio si no existe
    except OSError:
        # Si no se puede crear el directorio, se devuelven listas vacías
        return [], [], []

    hoteles = leer_archivo(RUTA_ARCHIVO_HOTELES)  # Leemos los datos de hoteles
    clientes = leer_archivo(RUTA_ARCHIVO_CLIENTES)  # Leemos los datos de clientes
    reservas = leer_archivo(RUTA_ARCHIVO_RESERVAS)  # Leemos los datos de reservas

    return hoteles, clientes, reservas


def escribir_archivo(ruta: str, datos: list) -> None:
    """Función para escribir una lista de datos en un archivo JSON.

    Pre: Recibe un string con la ruta del archivo y los datos a escribir en forma de lista

    Post: Escribe los datos en el archivo JSON especificado.
    En caso de error, imprime un mensaje indicando el problema.
    """
    try:  # Intentamos abrir el archivo
        with open(
            ruta, "w", encoding="utf-8"
        ) as f:  # Abrimos el archivo en modo escritura con UTF-8
            json.dump(
                datos, f, indent=4, ensure_ascii=False
            )  # Escribimos los datos en formato JSON, con indentación. dump convierte el objeto Python en JSON
    except IOError as error:  # Si hay un error de entrada/salida
        print(f"Error al guardar '{ruta}': {error}")


def guardar_datos(hoteles: list, clientes: list, reservas: list) -> None:
    """Funcion para guardar las listas de hoteles, clientes y reservas en los JSON correspondientes.

    Pre: Recibe tres listas, con los datos de hoteles, clientes y reservas.

    Post: Guarda los datos en los archivos JSON en la ruta correspondiente.
    """
    try:
        os.makedirs(RUTA_DATA, exist_ok=True)
    except OSError as error:
        print(f"No se pudo asegurar el directorio de datos '{RUTA_DATA}': {error}")
        return

    escribir_archivo(RUTA_ARCHIVO_HOTELES, hoteles)
    escribir_archivo(RUTA_ARCHIVO_CLIENTES, clientes)
    escribir_archivo(RUTA_ARCHIVO_RESERVAS, reservas)


# Definimos las rutas de los archivos de datos
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Directorio de este archivo, src/
RUTA_DATA = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data")
)  # Ruta del directorio /data

RUTA_ARCHIVO_HOTELES = os.path.join(
    RUTA_DATA, "hoteles.json"
)  # Ruta del archivo hoteles.json
RUTA_ARCHIVO_CLIENTES = os.path.join(
    RUTA_DATA, "clientes.json"
)  # Ruta del archivo clientes.json
RUTA_ARCHIVO_RESERVAS = os.path.join(
    RUTA_DATA, "reservas.json"
)  # Ruta del archivo reservas.json

if __name__ == "__main__":
    print("RUTA_DATA:", RUTA_DATA)
    print("RUTA_ARCHIVO_HOTELES:", RUTA_ARCHIVO_HOTELES)
    print("RUTA_ARCHIVO_CLIENTES:", RUTA_ARCHIVO_CLIENTES)
    print("RUTA_ARCHIVO_RESERVAS:", RUTA_ARCHIVO_RESERVAS)

    
def exportar_datos_csv(hoteles: list, clientes: list, reservas: list) -> None:
   
    """
    Función principal para gestionar la exportación de todos los datos a CSV.
    Maneja la lógica de rutas y llama a las funciones de exportación.
    Pre: Recibe las listas de hoteles, clientes y reservas.
    
    Post: Exporta los datos a archivos CSV en las rutas especificadas.
    """
    limpiar_pantalla()
    print("=" * 40)
    print("   --- Exportando datos a CSV ---     ".center(40, " "))
    print("=" * 40)
    
    try:
        # 1. Definir las rutas (usando datos.RUTA_DATA)
        ruta_clientes_csv = os.path.join(datos.RUTA_DATA, "clientes_export.csv")
        ruta_reservas_csv = os.path.join(datos.RUTA_DATA, "reservas_export.csv")
        ruta_hoteles_csv = os.path.join(datos.RUTA_DATA, "hoteles_export.csv")
        ruta_habitaciones_csv = os.path.join(datos.RUTA_DATA, "habitaciones_export.csv")

        # 2. Llamar a las funciones de exportación (que están en este mismo archivo)
        exportar_clientes_csv(clientes, ruta_clientes_csv)
        exportar_reservas_csv(reservas, ruta_reservas_csv)
        exportar_hoteles_csv(hoteles, ruta_hoteles_csv, ruta_habitaciones_csv)
        
        print(f"\n¡Datos exportados exitosamente en la carpeta '{datos.RUTA_DATA}'!")
    
    except Exception as e:
        print(f"\nOcurrió un error general al exportar: {e}")
    
    input("\nPresione Enter para continuar...")
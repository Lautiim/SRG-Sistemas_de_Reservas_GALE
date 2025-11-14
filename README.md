# SRG (Sistemas de Reservas GALE)

Trabajo final de **Algoritmia y Estructura de Datos**  
UADE Costa Argentina - 2025

## Descripción
Sistema de gestión de reservas para hoteles en **Python**. Mantiene datos en memoria (sin BD). Incluye creación, consulta, modificación y exportación de información de hoteles, clientes y reservas.

## Requisitos
- Soporta Python 3.12 y versiones posteriores
- Entorno virtual recomendado

## Funcionalidades Principales
- Clientes: alta, listado, búsqueda, modificación.
- Hoteles: alta, listado, modificación.
- Habitaciones por hotel: agregar, actualizar, eliminar (protege si hay reservas).
- Reservas: crear, listar, buscar por cliente/hotel, modificar (fechas, habitación, cliente, hotel).
- Reportes: habitaciones disponibles, búsquedas combinadas.
- Exportación CSV: clientes, hoteles, reservas (carpeta `csv/`).
- Validaciones: fechas (YYYY-MM-DD), conflictos de reservas, unicidad de DNI y número de habitación.
- Menús interactivos por consola.

## Estructura
```
src/
  datos.py
  gestion_clientes.py
  gestion_hoteles.py
  gestion_reservas.py
  reportes.py
  utils.py
tests/
  test_main.py
  test_modificaciones.py
.github/workflows/ci.yml
```

## Calidad de Código
- Formateo: Black.
- Linter: Pylint (para correcciones de import order, else redundantes, excepciones amplias).
- CI: GitHub Actions (Ubuntu, Windows, macOS) ejecuta black --check, pylint y pytest.

## Instalación Rápida
```powershell
python -m venv .venv
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Uso
```powershell
python src\main.py
```

## Pruebas
```powershell
python -m pytest -q
```

## Lint/Formato
```powershell
black src tests
pylint src tests
```

## Exportación CSV
Genera archivos en carpeta `csv/`. Se crea automáticamente si no existe.


## Integrantes
- Axel Aguilar
- Emanuel Grossi
- Gianluca Chia
- Lautaro Salto

## Enlaces
- Trello: https://trello.com/b/LePKo6J6/srg-sistemas-de-reservas-gale
- Drive: https://drive.google.com/drive/u/0/folders/1_R_JRjaMFSzTjN6Y907UZiyd5XfOL9k6
- Repo: https://github.com/Lautiim/SRG-Sistemas_de_Reservas_GALE
- Python Docs: https://docs.python.org/3

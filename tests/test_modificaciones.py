import pytest
from src.gestion_clientes import actualizar_cliente
from src.gestion_hoteles import (
    actualizar_hotel,
    agregar_habitacion_a_hotel,
    actualizar_habitacion_de_hotel,
    eliminar_habitacion_de_hotel,
)
from src.gestion_reservas import actualizar_reserva


@pytest.fixture
def data_sample():
    hoteles = [
        {
            "id": 1,
            "nombre": "Hotel Sol",
            "ubicacion": "Ciudad",
            "habitaciones": [
                {"numero": 101, "capacidad": 2, "precio": 100.0},
                {"numero": 102, "capacidad": 2, "precio": 110.0},
            ],
        },
        {
            "id": 2,
            "nombre": "Hotel Mar",
            "ubicacion": "Playa",
            "habitaciones": [
                {"numero": 201, "capacidad": 3, "precio": 150.0},
            ],
        },
    ]
    clientes = [
        {"id": 1, "nombre": "Juan Perez", "dni": "12345678", "telefono": "111"},
        {"id": 2, "nombre": "Ana Gomez", "dni": "87654321", "telefono": "222"},
    ]
    reservas = [
        {
            "id": 1,
            "id_cliente": 1,
            "id_hotel": 1,
            "numero_habitacion": 101,
            "fecha_inicio": "2024-01-10",
            "fecha_fin": "2024-01-15",
        },
        {
            "id": 2,
            "id_cliente": 2,
            "id_hotel": 1,
            "numero_habitacion": 102,
            "fecha_inicio": "2024-01-12",
            "fecha_fin": "2024-01-14",
        },
    ]
    return hoteles, clientes, reservas


def test_actualizar_cliente_nombre_y_dni(data_sample):
    hoteles, clientes, reservas = data_sample
    ok = actualizar_cliente(
        clientes, 1, hoteles=hoteles, reservas=reservas, nombre="Juan P.", dni="11223344"
    )
    assert ok is True
    assert clientes[0]["nombre"] == "Juan P."
    assert clientes[0]["dni"] == "11223344"


def test_actualizar_cliente_dni_duplicado_falla(data_sample):
    hoteles, clientes, reservas = data_sample
    # intenta poner el DNI del cliente 2 en el cliente 1
    ok = actualizar_cliente(clientes, 1, hoteles=hoteles, reservas=reservas, dni=clientes[1]["dni"])
    assert ok is False


def test_actualizar_hotel_nombre(data_sample):
    hoteles, clientes, reservas = data_sample
    ok = actualizar_hotel(
        hoteles, 1, clientes=clientes, reservas=reservas, nombre="Hotel Sol Deluxe"
    )
    assert ok is True
    assert hoteles[0]["nombre"] == "Hotel Sol Deluxe"


def test_actualizar_reserva_cambiar_fechas_sin_solapamiento(data_sample):
    hoteles, clientes, reservas = data_sample
    ok = actualizar_reserva(
        reservas,
        hoteles,
        clientes,
        1,
        fechas=("2024-01-16", "2024-01-18"),
    )
    assert ok is True
    r = next(r for r in reservas if r["id"] == 1)
    assert r["fecha_inicio"] == "2024-01-16"
    assert r["fecha_fin"] == "2024-01-18"


def test_actualizar_reserva_solapamiento_falla(data_sample):
    hoteles, clientes, reservas = data_sample
    # Mover reserva 1 a un rango que se solapa con la reserva 2
    # En la misma habitación 102, que ya tiene otra reserva del 12 al 14
    ok = actualizar_reserva(
        reservas,
        hoteles,
        clientes,
        1,
        numero_habitacion=102,
        fechas=("2024-01-12", "2024-01-13"),
    )
    assert ok is False


# --- Habitaciones: agregar y modificar ---


def test_agregar_habitacion_ok(data_sample):
    hoteles, clientes, reservas = data_sample
    ok = agregar_habitacion_a_hotel(
        hoteles, 2, numero=202, capacidad=2, precio=120.0, clientes=clientes, reservas=reservas
    )
    assert ok is True
    hotel = next(h for h in hoteles if h["id"] == 2)
    assert any(
        hab["numero"] == 202 and hab["capacidad"] == 2 and hab["precio"] == 120.0
        for hab in hotel["habitaciones"]
    )


def test_agregar_habitacion_numero_duplicado_falla(data_sample):
    hoteles, _, _ = data_sample
    # Ya existe 101 en hotel 1
    ok = agregar_habitacion_a_hotel(hoteles, 1, numero=101, capacidad=2, precio=100.0)
    assert ok is False


def test_actualizar_habitacion_ok(data_sample):
    hoteles, clientes, reservas = data_sample
    # En hotel 1 existe 101
    ok = actualizar_habitacion_de_hotel(
        hoteles, 1, 101, capacidad=4, precio=180.0, clientes=clientes, reservas=reservas
    )
    assert ok is True
    hotel = next(h for h in hoteles if h["id"] == 1)
    hab = next(h for h in hotel["habitaciones"] if h["numero"] == 101)
    assert hab["capacidad"] == 4
    assert hab["precio"] == 180.0


def test_actualizar_habitacion_valores_invalidos_falla(data_sample):
    hoteles, _, _ = data_sample
    # Capacidad negativa invalida
    ok = actualizar_habitacion_de_hotel(hoteles, 1, 101, capacidad=-1)
    assert ok is False
    # Precio cero invalido
    ok = actualizar_habitacion_de_hotel(hoteles, 1, 101, precio=0)
    assert ok is False


def test_eliminar_habitacion_ok_sin_reservas(data_sample):
    hoteles, clientes, reservas = data_sample
    # En hotel 2 hab 201 no tiene reservas
    ok = eliminar_habitacion_de_hotel(hoteles, 2, 201, clientes=clientes, reservas=reservas)
    assert ok is True
    hotel = next(h for h in hoteles if h["id"] == 2)
    assert all(hab["numero"] != 201 for hab in hotel["habitaciones"])


def test_eliminar_habitacion_con_reserva_falla(data_sample):
    hoteles, clientes, reservas = data_sample
    # En hotel 1 hab 101 tiene una reserva
    ok = eliminar_habitacion_de_hotel(hoteles, 1, 101, clientes=clientes, reservas=reservas)
    assert ok is False

from tests.conftest import RUTA_ELEGIBILIDAD


def test_consulta_usa_la_operacion_del_contrato(aplicacion, elegibilidad, contrato):
    cliente, _ = aplicacion
    cliente.post("/api/v1/postulaciones", json={"estudianteId": "EST-001", "asignatura": "ASIG-01"})
    solicitud = elegibilidad.solicitudes[0]
    assert contrato["servers"][0]["url"] == "http://localhost:8081/api/v1"
    assert RUTA_ELEGIBILIDAD in contrato["paths"]
    assert solicitud.method == "GET"
    assert str(solicitud.url) == "http://localhost:8081/api/v1/estudiantes/EST-001/elegibilidad?asignatura=ASIG-01"


def test_solo_se_hacen_lecturas_a_elegibilidad(aplicacion, elegibilidad):
    cliente, app = aplicacion
    elegibilidad.modo = "sga_no_disponible"
    for estudiante in ("EST-001", "EST-003", "EST-999"):
        cliente.post("/api/v1/postulaciones", json={"estudianteId": estudiante, "asignatura": "ASIG-01"})
    elegibilidad.modo = "normal"
    from app.validacion import revalidar_pendientes

    revalidar_pendientes(app.state.repositorio, app.state.cliente)
    assert {s.method for s in elegibilidad.solicitudes} == {"GET"}


def test_todos_los_ejemplos_del_contrato_se_registran(aplicacion, elegibilidad):
    cliente, _ = aplicacion
    for estudiante, esperado in elegibilidad.resultados.items():
        cuerpo = cliente.post(
            "/api/v1/postulaciones", json={"estudianteId": estudiante, "asignatura": esperado["asignatura"]}
        ).json()
        assert cuerpo["elegibilidad"] == esperado

from app.repositorio import ENVIADA, SIN_REGISTRO_ACADEMICO, VALIDACION_PENDIENTE, VALIDADA
from app.validacion import revalidar_pendientes


def postular(cliente, estudiante, asignatura="ASIG-01"):
    return cliente.post("/api/v1/postulaciones", json={"estudianteId": estudiante, "asignatura": asignatura})


def revalidar(app):
    return revalidar_pendientes(app.state.repositorio, app.state.cliente)


def test_salud(aplicacion):
    cliente, _ = aplicacion
    assert cliente.get("/api/v1/salud").json() == {"estado": "OK"}


def test_postulacion_elegible_muestra_la_respuesta_de_elegibilidad(aplicacion):
    cliente, _ = aplicacion
    respuesta = postular(cliente, "EST-001")
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == ENVIADA
    assert cuerpo["estadoValidacion"] == VALIDADA
    assert cuerpo["elegibilidad"]["estadoGeneral"] == "ELEGIBLE"
    assert cuerpo["elegibilidad"]["fechaConsulta"]


def test_postulacion_no_elegible_por_nota(aplicacion):
    cliente, _ = aplicacion
    cuerpo = postular(cliente, "EST-003").json()
    assert cuerpo["elegibilidad"]["estadoGeneral"] == "NO_ELEGIBLE"
    assert cuerpo["elegibilidad"]["requisitos"]["nota"]["resultado"] == "NO_CUMPLE"


def test_dato_faltante_queda_incompleto(aplicacion):
    cliente, _ = aplicacion
    cuerpo = postular(cliente, "EST-008").json()
    assert cuerpo["estadoValidacion"] == VALIDADA
    assert cuerpo["elegibilidad"]["estadoGeneral"] == "INCOMPLETO"


def test_estudiante_sin_registro_no_se_revalida(aplicacion, elegibilidad):
    cliente, app = aplicacion
    cuerpo = postular(cliente, "EST-999").json()
    assert cuerpo["estadoValidacion"] == SIN_REGISTRO_ACADEMICO
    consultas = len(elegibilidad.solicitudes)
    revalidar(app)
    assert len(elegibilidad.solicitudes) == consultas


def test_sga_no_disponible_conserva_y_revalida(aplicacion, elegibilidad):
    cliente, app = aplicacion
    elegibilidad.modo = "sga_no_disponible"
    cuerpo = postular(cliente, "EST-001").json()
    assert cuerpo["estado"] == ENVIADA
    assert cuerpo["estadoValidacion"] == VALIDACION_PENDIENTE
    assert revalidar(app) == 0
    elegibilidad.modo = "normal"
    assert revalidar(app) == 1
    actual = cliente.get(f"/api/v1/postulaciones/{cuerpo['id']}").json()
    assert actual["estadoValidacion"] == VALIDADA
    assert actual["elegibilidad"]["estadoGeneral"] == "ELEGIBLE"


def test_tiempo_agotado_y_conexion_rechazada_quedan_pendientes(aplicacion, elegibilidad):
    cliente, _ = aplicacion
    elegibilidad.modo = "tiempo_agotado"
    assert postular(cliente, "EST-001").json()["estadoValidacion"] == VALIDACION_PENDIENTE
    elegibilidad.modo = "conexion_rechazada"
    assert postular(cliente, "EST-002").json()["estadoValidacion"] == VALIDACION_PENDIENTE


def test_veinte_postulaciones_durante_la_falla_se_conservan_sin_duplicados(aplicacion, elegibilidad):
    cliente, app = aplicacion
    elegibilidad.modo = "sga_no_disponible"
    for numero in range(20):
        assert postular(cliente, "EST-001", f"ASIG-{numero:02d}").status_code == 201
    postulaciones = cliente.get("/api/v1/postulaciones").json()
    assert len(postulaciones) == 20
    assert all(p["estadoValidacion"] == VALIDACION_PENDIENTE for p in postulaciones)
    elegibilidad.modo = "normal"
    assert revalidar(app) == 20
    assert all(p["estadoValidacion"] == VALIDADA for p in cliente.get("/api/v1/postulaciones").json())


def test_postulacion_duplicada(aplicacion):
    cliente, _ = aplicacion
    assert postular(cliente, "EST-001").status_code == 201
    assert postular(cliente, "EST-001").status_code == 409


def test_consulta_de_estado(aplicacion):
    cliente, _ = aplicacion
    creada = postular(cliente, "EST-004").json()
    consultada = cliente.get(f"/api/v1/postulaciones/{creada['id']}").json()
    assert consultada == creada
    assert cliente.get("/api/v1/postulaciones/999").status_code == 404


def test_datos_invalidos_se_rechazan_sin_consultar(aplicacion, elegibilidad):
    cliente, _ = aplicacion
    assert postular(cliente, "EST 001").status_code == 422
    assert elegibilidad.solicitudes == []

from .elegibilidad import ClienteElegibilidad, TipoRespuesta
from .repositorio import SIN_REGISTRO_ACADEMICO, VALIDADA, RepositorioPostulaciones


def validar(repositorio: RepositorioPostulaciones, cliente: ClienteElegibilidad, postulacion: dict) -> dict:
    respuesta = cliente.consultar(postulacion["estudianteId"], postulacion["asignatura"])
    if respuesta.tipo is TipoRespuesta.RESULTADO:
        repositorio.registrar_validacion(postulacion["id"], VALIDADA, respuesta.cuerpo)
    elif respuesta.tipo is TipoRespuesta.SIN_REGISTRO:
        repositorio.registrar_validacion(postulacion["id"], SIN_REGISTRO_ACADEMICO, None)
    return repositorio.obtener(postulacion["id"])


def revalidar_pendientes(repositorio: RepositorioPostulaciones, cliente: ClienteElegibilidad) -> int:
    revalidadas = 0
    for postulacion in repositorio.pendientes():
        if validar(repositorio, cliente, postulacion)["estadoValidacion"] != postulacion["estadoValidacion"]:
            revalidadas += 1
    return revalidadas

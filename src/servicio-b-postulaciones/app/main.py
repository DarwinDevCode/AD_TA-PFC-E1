import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import Configuracion
from .elegibilidad import ClienteElegibilidad
from .repositorio import PostulacionDuplicada, RepositorioPostulaciones
from .validacion import revalidar_pendientes, validar

logger = logging.getLogger("postulaciones")


class SolicitudPostulacion(BaseModel):
    estudianteId: str = Field(min_length=1, max_length=20, pattern=r"^[A-Za-z0-9-]+$")
    asignatura: str = Field(min_length=1, max_length=20, pattern=r"^[A-Za-z0-9-]+$")


def crear_app(
    configuracion: Configuracion | None = None,
    cliente: ClienteElegibilidad | None = None,
    repositorio: RepositorioPostulaciones | None = None,
    revalidacion_automatica: bool = True,
) -> FastAPI:
    configuracion = configuracion or Configuracion()
    cliente = cliente or ClienteElegibilidad(configuracion.elegibilidad_url, configuracion.tiempo_espera)
    repositorio = repositorio or RepositorioPostulaciones(configuracion.ruta_bd)

    async def ciclo_revalidacion() -> None:
        while True:
            await asyncio.sleep(configuracion.intervalo_revalidacion)
            try:
                await asyncio.to_thread(revalidar_pendientes, repositorio, cliente)
            except Exception:
                logger.exception("Falló la revalidación de postulaciones pendientes")

    @asynccontextmanager
    async def ciclo_de_vida(_: FastAPI):
        tarea = asyncio.create_task(ciclo_revalidacion()) if revalidacion_automatica else None
        yield
        if tarea:
            tarea.cancel()

    app = FastAPI(title="Servicio de postulaciones del SGAC", version="1.0.0", lifespan=ciclo_de_vida)
    app.state.repositorio = repositorio
    app.state.cliente = cliente

    @app.get("/api/v1/salud")
    def salud() -> dict:
        return {"estado": "OK"}

    @app.post("/api/v1/postulaciones", status_code=201)
    def registrar_postulacion(solicitud: SolicitudPostulacion) -> dict:
        try:
            postulacion = repositorio.crear(solicitud.estudianteId, solicitud.asignatura)
        except PostulacionDuplicada:
            raise HTTPException(409, "El estudiante ya tiene una postulación para esta asignatura.")
        try:
            return validar(repositorio, cliente, postulacion)
        except ValueError as error:
            raise HTTPException(400, str(error))

    @app.get("/api/v1/postulaciones")
    def listar_postulaciones() -> list[dict]:
        return repositorio.listar()

    @app.get("/api/v1/postulaciones/{postulacion_id}")
    def consultar_postulacion(postulacion_id: int) -> dict:
        postulacion = repositorio.obtener(postulacion_id)
        if postulacion is None:
            raise HTTPException(404, "La postulación no existe.")
        return postulacion

    return app


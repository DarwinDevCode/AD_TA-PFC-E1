import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Configuracion:
    elegibilidad_url: str = os.getenv("ELEGIBILIDAD_URL", "http://localhost:8081/api/v1")
    tiempo_espera: float = float(os.getenv("ELEGIBILIDAD_TIEMPO_ESPERA", "3"))
    intervalo_revalidacion: float = float(os.getenv("REVALIDACION_SEGUNDOS", "60"))
    ruta_bd: str = os.getenv("POSTULACIONES_BD", "postulaciones.db")

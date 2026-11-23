# PFC Aplicaciones Distribuidas, TA-PFC-E1

**Nombre del proyecto:** PENDIENTE DE DEFINIR.

## Descripción del proyecto

PENDIENTE DE DEFINIR.

## Integrantes y roles

| Integrante | Rol propuesto |
| --- | --- |
| SANCHEZ VERA DARWIN JOEL | Arquitecto |
| MUÑOZ VERA MELANIE MICHELLE | Líder de Desarrollo y Responsable de Calidad |
| QUINTERO RICO LUIS DAVID | Responsable de Documentación |

Los roles son propuestas cuya confirmación estaba prevista para el **20 de noviembre de 2026**. La confirmación efectiva está **PENDIENTE DE DEFINIR**. MUÑOZ VERA MELANIE MICHELLE asume **dos roles**: Líder de Desarrollo y Responsable de Calidad.

## Aportes de Melanie Muñoz Vera a E1

- **Desarrollo:** implementó el [servicio A de elegibilidad](src/servicio-a-elegibilidad/README.md) y el SGA simulado de solo lectura. Preparó los [14 casos de elegibilidad](src/pruebas/casos-servicio-a.md) según el contrato OpenAPI y verificó la comunicación con el servicio B de postulaciones.
- **Calidad:** documentó [12 requisitos no funcionales](docs/secciones/06-requisitos-no-funcionales.tex) y su [matriz de pruebas](src/pruebas/matriz-pruebas-rnf.md), [siete riesgos técnicos](docs/secciones/12-analisis-riesgos.tex) y la [matriz de trazabilidad](docs/matriz-trazabilidad.md) entre RF, RNF, C4, ADR y CAP/PACELC. Las cifras sujetas a validación institucional siguen siendo provisionales.
- **Evidencia de integración:** documentó los resultados en la [sección 14](docs/secciones/14-esqueleto-funcional.tex). Al restablecer el SGA simulado, se revalidaron las 20 postulaciones sintéticas, con 0 pérdidas y 0 duplicados.

## Estructura del repositorio

- `/src/`: código fuente y servicios del esqueleto funcional.
- `/docs/`: documento único en LaTeX, secciones y bibliografía.
- `/docs/adr/`: registros de decisiones arquitectónicas.
- `/docs/diagramas/`: diagramas del sistema.
- `/evidencias/`: evidencias del trabajo y de las pruebas.
- `BITACORA.md`: sesiones de trabajo, participantes, decisiones y problemas resueltos.
- `README.md`: información del proyecto y guía de compilación.

## Ejecución del esqueleto

### Instalación

Usa Python 3.12 y ejecuta los comandos desde la raíz del repositorio.

En Windows (PowerShell):

```powershell
py -3.12 -m venv src/servicio-a-elegibilidad/.venv
$pythonSGAC = '.\src\servicio-a-elegibilidad\.venv\Scripts\python.exe'
& $pythonSGAC -m pip install -r src/servicio-a-elegibilidad/requirements.txt -r src/servicio-b-postulaciones/requirements.txt
& $pythonSGAC -X utf8 src/pruebas/prueba-comunicacion.py
```

En Linux o macOS:

```sh
python3.12 -m venv src/servicio-a-elegibilidad/.venv
python_sgac=src/servicio-a-elegibilidad/.venv/bin/python
"$python_sgac" -m pip install -r src/servicio-a-elegibilidad/requirements.txt -r src/servicio-b-postulaciones/requirements.txt
"$python_sgac" -X utf8 src/pruebas/prueba-comunicacion.py
```

### Prueba de comunicación

La prueba arranca el SGA simulado, elegibilidad (A) y postulaciones (B)
en puertos locales disponibles. Usa datos sintéticos y una base SQLite
temporal. Cuenta con el intervalo de revalidación de 60 segundos, por lo
que puede tardar algo más de un minuto.

El resultado esperado es `Prueba de comunicación superada.` Se comprueban
los resultados de elegibilidad, la respuesta de estudiante sin registro,
el `503` al detener el SGA y la revalidación de la misma postulación
cuando el SGA vuelve a estar disponible. Al terminar se comprueba que
el simulador recibió solo lecturas.

### Arranque manual

En tres terminales, desde la carpeta indicada, ejecuta cada comando con
el Python del entorno virtual anterior. Inicia primero el SGA y el
servicio A, y luego el servicio B.

| Carpeta | Comando de Python | Puerto local |
| --- | --- | --- |
| `src/servicio-a-elegibilidad` | `python -m uvicorn app.sga_simulado:app --port 8090` | 8090 |
| `src/servicio-a-elegibilidad` | `python -m uvicorn app.main:crear_app --factory --port 8081` | 8081 |
| `src/servicio-b-postulaciones` | `python -m uvicorn app.main:crear_app --factory --port 8080` | 8080 |

Las operaciones y variables de configuración están en los README de
[elegibilidad](src/servicio-a-elegibilidad/README.md) y
[postulaciones](src/servicio-b-postulaciones/README.md).

## Video de presentación

[Video de presentación de E1 (carpeta de Google Drive)](https://drive.google.com/drive/folders/1cz2WF7eTlp2MVnRtzyxq3t1MDS0v-Pkc?usp=drive_link)

## Compilación del documento

- **Compilador:** `pdflatex` con `biber`.
- **Archivo principal:** `docs/main.tex`.
- **Directorio de ejecución:** `docs/`.

Ejecutar los comandos en este orden, desde `docs/`:

```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

**Dependencias:** TeX Live o MiKTeX con `pdflatex`, `biber`, `inputenc` (UTF-8), `fontenc` (T1), `lmodern`, `babel` con español, `csquotes`, `geometry`, `graphicx`, `booktabs`, `tabularx`, `longtable`, `hyperref`, `biblatex` y `biblatex-ieee` (estilo IEEE).

En MiKTeX, las versiones de `biber` y `biblatex` deben ser compatibles.

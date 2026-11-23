# Sistema de Gestión de Ayudantías de Cátedra (SGAC)

**Actividad:** TA-PFC-E1 — Proyecto Fin de Curso de Aplicaciones Distribuidas.

## Descripción del proyecto

El SGAC es una propuesta para gestionar convocatorias, postulaciones, evaluación, seguimiento y certificación de ayudantes de cátedra en la UTEQ. La arquitectura definida en ADR-001 separa servicios por capacidad de negocio. La integración con el SGA se simula con consultas de solo lectura; no se utiliza acceso a registros institucionales reales.

## Integrantes y roles

| Integrante | Rol |
| --- | --- |
| SANCHEZ VERA DARWIN JOEL | Arquitecto |
| MUÑOZ VERA MELANIE MICHELLE | Líder de Desarrollo y Responsable de Calidad (dos roles) |
| QUINTERO RICO LUIS DAVID | Responsable de Documentación |

**Periodo académico:** PENDIENTE DE DEFINIR. Confirmación institucional de los roles: PENDIENTE DE DEFINIR.

**Link del video:** https://drive.google.com/drive/folders/1cz2WF7eTlp2MVnRtzyxq3t1MDS0v-Pkc?usp=drive_link

## Estructura del repositorio

- `src/`: contratos, servicios y pruebas del esqueleto funcional.
- `docs/`: documento LaTeX, secciones, bibliografía y PDF compilado.
- `docs/adr/`: decisiones arquitectónicas ADR-001 y ADR-002.
- `docs/diagramas/`: archivos editables de los niveles C4.
- `evidencias/`: levantamiento, sesiones de diseño y capturas.
- `BITACORA.md`: registro de sesiones y decisiones reales del equipo.
- `README.md`: orientación para la ejecución y la documentación.

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

## Compilación del documento

- **Compilador:** `pdflatex` y `biber`.
- **Archivo principal:** `docs/main.tex`.
- **Dependencias:** TeX Live o MiKTeX con `pdflatex`, `biber`, `inputenc` UTF-8, `fontenc` T1, `lmodern`, `babel` español, `csquotes`, `geometry`, `graphicx`, `booktabs`, `tabularx`, `longtable`, `hyperref`, `biblatex` y `biblatex-ieee`.

Desde `docs/` ejecutar, en este orden:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

El resultado es `docs/main.pdf`. En MiKTeX, las versiones de `biber` y `biblatex` deben ser compatibles. Para una entrega reproducible, el proceso debe funcionar en un clon limpio y sin referencias sin resolver (`??`).

## Estado de la documentación para E1

El informe se construye en un solo documento LaTeX, desde `docs/main.tex`. El estado del trabajo debe distinguir los archivos ya integrados en `main` de los borradores preparados en ramas de trabajo.

| Entregable | Archivo o ubicación | Situación |
| --- | --- | --- |
| Base documental | `docs/main.tex`, `docs/preambulo.tex`, `docs/main.pdf` | Estructura inicial integrada; el PDF final debe regenerarse tras fusionar cambios. |
| Levantamiento | [`docs/E1-levantamiento-entrevista`](https://github.com/DarwinDevCode/AD_TA-PFC-E1/tree/docs/E1-levantamiento-entrevista/evidencias/levantamiento) | Guion y acta preparados en una rama. Falta contrastar las respuestas, acreditar conformidad y autorización de publicación. |
| Contexto, objetivos y requisitos funcionales | `docs/secciones/02-contexto-problema.tex`, `03-objetivos.tex`, `05-requisitos-funcionales.tex` | Borradores documentales; los requisitos y cifras sin respaldo institucional requieren validación. |
| Presentación y planificación | `docs/secciones/00-portada.tex`, `01-resumen-ejecutivo.tex`, `13-plan-proyecto.tex` | Elaboración y revisión en curso; faltan algunos datos oficiales y el enlace de GitHub Projects. |
| Aportes y uso de IA | `docs/secciones/15-tabla-aportes.tex`, `16-declaracion-ia.tex` | Deben completarse con los enlaces y las declaraciones reales de todos los integrantes. |
| Requisitos no funcionales y riesgos | `docs/secciones/06-requisitos-no-funcionales.tex`, `12-analisis-riesgos.tex` | Responsabilidad de Desarrollo y Calidad; pendiente de integración definitiva. |

Las cifras técnicas de capacidad, respuesta, disponibilidad y recuperación son metas propuestas, no resultados medidos en la UTEQ ni declaraciones verificadas de la entrevista.

## Comprobaciones para el cierre

Antes de entregar E1, verificar la evidencia del levantamiento con el consentimiento requerido, completar las secciones y referencias, ejecutar el esqueleto desde un clon limpio, actualizar la bitácora con sesiones reales, comprobar el PDF compilado y agregar el enlace al video grupal. El PDF de identificación para el SGA debe tener una sola página.

## Organización y trazabilidad

- [Issues del repositorio](https://github.com/DarwinDevCode/AD_TA-PFC-E1/issues).
- [Decisiones de arquitectura](docs/adr/).
- [Documento LaTeX](docs/main.tex).
- [Trabajo de levantamiento](evidencias/levantamiento/): la conformidad de la entrevista debe acreditarse antes de declararlo validado.
- **Tablero GitHub Projects:** PENDIENTE DE DEFINIR.

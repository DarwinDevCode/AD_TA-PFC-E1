# Diagramas de arquitectura (modelo C4)

Esta carpeta guarda los archivos **editables** de los diagramas de arquitectura del PFC. Las figuras que se insertan en el documento LaTeX se exportan desde aquí a `docs/figuras/`.

Requisito de TA-PFC-E1 que cubre esta carpeta:

> Arquitectura base con el modelo C4: el diagrama de contexto (nivel 1), que muestra el sistema, sus usuarios y los sistemas externos, y el diagrama de contenedores (nivel 2), que muestra los servicios, las bases de datos y cómo se comunican. Ambos se elaboran en draw.io o Structurizr y se versionan en el repositorio.

| Dato | Valor |
| --- | --- |
| Herramienta | draw.io (diagrams.net), versión web en https://app.diagrams.net o aplicación de escritorio |
| Responsable | SANCHEZ VERA DARWIN JOEL (Arquitecto) |
| Revisa el nivel 1 | QUINTERO RICO LUIS DAVID (coherencia con los stakeholders del levantamiento) |
| Revisa el nivel 2 | MUÑOZ VERA MELANIE MICHELLE (coherencia con los servicios de `/src/`) |

## Archivos

| Archivo | Contenido | Figura exportada | Sección del documento | Estado |
| --- | --- | --- | --- | --- |
| `c4-nivel1-contexto.drawio` | Página `Leyenda` y página `Diagrama` con el contexto del sistema | `docs/figuras/c4-nivel1-contexto.pdf` | `docs/secciones/08-arquitectura-c4.tex` | Pendiente |
| `c4-nivel2-contenedores.drawio` | Página `Leyenda` y página `Diagrama` con los contenedores | `docs/figuras/c4-nivel2-contenedores.pdf` | `docs/secciones/08-arquitectura-c4.tex` y `09-modelo-comunicacion.tex` | Pendiente |

Cada archivo tiene dos páginas. `Leyenda` fija la notación y no se exporta. `Diagrama` es la única página que se exporta al documento.

Los diagramas se dibujan después del levantamiento de información (nivel 1) y después de ADR-001 y ADR-002 (nivel 2). Hasta entonces la página `Diagrama` solo tiene el título con el nombre del proyecto pendiente.

## Qué muestra cada nivel

**Nivel 1, contexto.** El sistema como una sola caja, las personas que lo usan y los sistemas externos con los que intercambia información.

- Cada persona corresponde a un stakeholder identificado en `02-contexto-problema.tex`. Si un stakeholder no aparece, la sección 08 explica por qué.
- No se muestran servicios internos, tecnologías ni bases de datos.

**Nivel 2, contenedores.** El interior del sistema: servicios, bases de datos y la comunicación entre ellos.

- Aparecen al menos los dos servicios del esqueleto funcional, con el mismo nombre que su carpeta en `/src/`.
- Cada contenedor indica su tecnología. Mientras no esté decidida se escribe `PENDIENTE DE DEFINIR`.
- El estilo de arquitectura debe coincidir con ADR-001 y el mecanismo principal de comunicación con ADR-002.

## Notación

Los diagramas son en blanco y negro. Los tipos de elemento se distinguen por la forma y el borde, no por el color.

| Elemento | Forma en draw.io | Texto obligatorio |
| --- | --- | --- |
| Persona | Figura de persona (C4) | **Nombre del rol** · `[Persona]` · qué hace con el sistema |
| Sistema en desarrollo (nivel 1) | Rectángulo redondeado, borde grueso | **Nombre del sistema** · `[Sistema de software]` · propósito |
| Sistema externo | Rectángulo redondeado, borde discontinuo | **Nombre** · `[Sistema externo]` · qué aporta |
| Límite del sistema (nivel 2) | Rectángulo sin relleno, borde discontinuo largo | **Nombre del sistema** · `[Límite del sistema]` |
| Contenedor: servicio o aplicación | Rectángulo redondeado, borde normal | **Nombre** · `[Contenedor: tecnología]` · responsabilidad |
| Contenedor: base de datos | Cilindro | **Nombre** · `[Contenedor: motor]` · qué datos guarda |
| Relación sincrónica | Flecha con línea continua | Ver reglas de etiquetado |
| Relación asincrónica | Flecha con línea discontinua | Ver reglas de etiquetado |

Las páginas `Leyenda` de los dos archivos `.drawio` contienen estas formas listas para copiar.

## Reglas de etiquetado de las relaciones

En el **nivel 1**, cada flecha lleva un verbo y lo que se intercambia. Ejemplo: `Consulta disponibilidad [navegador web]`.

En el **nivel 2**, cada flecha lleva tres datos, porque el modelo de comunicación exige, para cada interacción del diagrama de contenedores, el tipo, el mecanismo y su justificación:

```
I-NN: verbo y qué se intercambia
[Sincrónica | Asincrónica] mecanismo
```

Ejemplo de formato: `I-01: Solicita el estado del registro` / `[Sincrónica] REST`.

- `I-NN` es un identificador correlativo (I-01, I-02…). La sección `09-modelo-comunicacion.tex` tiene una fila por cada `I-NN`, con el mismo identificador. Así cada flecha se rastrea hasta su justificación.
- El mecanismo es uno de los que menciona la actividad: REST, gRPC o mensajería. Si es mensajería, se nombra el broker cuando esté decidido.
- La línea es continua si la interacción es sincrónica y discontinua si es asincrónica.
- Las flechas hacia una base de datos llevan el verbo y el protocolo, por ejemplo `Lee y escribe [protocolo]`. No necesitan `I-NN` salvo que el equipo las analice en el modelo de comunicación.

## Formato del archivo y control de versiones

- Se guarda como `.drawio` **sin comprimir**, para que GitHub muestre los cambios como XML legible. En draw.io: `Archivo > Propiedades`, desmarcar `Comprimido`.
- No se suben exportaciones (PDF o PNG) a esta carpeta. Van en `docs/figuras/`.
- Cada cambio en un `.drawio` se confirma en el mismo commit que su figura exportada, para que el documento nunca muestre una versión distinta del editable.

## Exportación al documento LaTeX

1. Abrir el `.drawio` y seleccionar la página `Diagrama`.
2. `Archivo > Exportar como > PDF`.
3. Marcar `Recortar` (sin márgenes) y exportar solo la página actual.
4. Guardar en `docs/figuras/` con el nombre de la tabla de archivos (`c4-nivel1-contexto.pdf` o `c4-nivel2-contenedores.pdf`).
5. Insertar en `08-arquitectura-c4.tex` con `\includegraphics`. El preámbulo ya busca imágenes en `figuras/`.

Se usa PDF porque es vectorial y no pierde calidad al ampliarse en el documento.

## Evolución desde el primer bosquejo

La actividad pide incluir el primer bosquejo de la arquitectura para mostrar cómo evolucionó hasta el diagrama C4. El bosquejo es una fotografía de la sesión de diseño y se guarda en `evidencias/sesiones-diseno/`, no aquí. Las versiones intermedias de los diagramas quedan registradas en el historial de Git de cada `.drawio`.

## Verificación antes de cerrar los issues de diagramas

- [ ] Los dos `.drawio` abren sin errores en https://app.diagrams.net.
- [ ] El nivel 1 muestra el sistema, todas las personas y todos los sistemas externos.
- [ ] Las personas del nivel 1 coinciden con los stakeholders del documento.
- [ ] El nivel 2 muestra los servicios del esqueleto con los mismos nombres que en `/src/`.
- [ ] Cada flecha del nivel 2 tiene `I-NN`, tipo y mecanismo, y hay una fila por flecha en la sección 09.
- [ ] El estilo coincide con ADR-001 y el mecanismo principal con ADR-002.
- [ ] Las figuras de `docs/figuras/` se exportaron desde la última versión de cada `.drawio`.

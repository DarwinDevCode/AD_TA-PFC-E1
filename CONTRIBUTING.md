# Guía de contribución

## Ramas y pull requests

- Crea una rama por issue con el formato `tipo/E1-NN-descripcion-corta`.
- Abre una pull request por rama, asigna un revisor e incluye `Closes #NN` en la descripción. Sustituye `NN` por el número del issue en GitHub.
- Integra los cambios con **Create a merge commit** para conservar el autor de cada commit. Evita **Squash and merge**.

## Commits

- Escribe los mensajes en minúsculas y sin tildes, con el formato `tipo(alcance): descripcion en presente`.
- Usa uno de estos tipos: `feat`, `fix`, `docs`, `build`, `chore`, `test` o `refactor`.
- Ejemplo: `docs(adr): agrega el indice de decisiones`.
- Un commit significativo agrega o cambia un entregable de forma verificable. Las correcciones de tildes, los merges y los cambios de una línea no cuentan.
- Cada integrante escribe sus mensajes y hace sus commits desde su propia cuenta, con su nombre y su correo de GitHub configurados. Nunca hagas commits en nombre de otra persona.

## Propiedad de los archivos

Cada archivo tiene un único dueño. Coordina con el dueño antes de editar su archivo.

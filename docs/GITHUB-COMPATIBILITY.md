# Compatibilidad con GitHub

Revisión previa a la publicación: 20 de noviembre de 2026.

## Comprobado

- El endpoint oficial `POST https://api.github.com/markdown`, en modo GFM, conserva las imágenes, las fuentes adaptativas de `picture`, el desplegable y los contactos.
- Las 32 referencias de imágenes y variantes del HTML devuelto resuelven a archivos locales existentes. Los archivos deberán publicarse junto al README.
- El icono del desplegable se incluye dentro de `picture`: el renderizador oficial ya no lo convierte en un enlace a la imagen, por lo que no interfiere con la apertura del desplegable.
- El correo y X son enlaces de texto reales. El subrayado al pasar el cursor se ha comprobado en la vista local con la hoja de estilos de GitHub.
- Las etiquetas usadas de actions/checkout@v7, actions/setup-python@v7 y actions/setup-node@v4 existen en los repositorios oficiales.
- Pasan 13 comprobaciones de datos y recursos y 9 del personaje animado.

La respuesta del renderizador y la comprobación de las acciones están guardadas en `.cache/github-compatibility/`, fuera de los archivos públicos.

## Pendiente de verificar tras publicar

La entrega de las imágenes a través de GitHub y su caché, la reproducción visual del banner en navegadores reales, la selección de tema del perfil y la primera ejecución completa de Actions. El endpoint de Markdown comprueba el HTML; no equivale a una publicación de prueba. Las preferencias de movimiento reducido pueden detener las animaciones de forma intencionada.

La actualización requiere que el flujo esté en la rama predeterminada y que Actions esté habilitado con los permisos necesarios. Su horario es aproximado: GitHub puede retrasar ejecuciones y suspender la programación tras 60 días sin actividad en un repositorio público. El correo abre el cliente configurado por cada visitante.

Fuentes: [formato y picture](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), [programación de workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [desactivación por inactividad](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows).

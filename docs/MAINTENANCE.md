# Mantenimiento del perfil

El perfil publicado es `README.md`. Se genera a partir de `data/profile.json`, `data/projects.json` y `data/github-stats.json`; no depende de una propuesta anterior ni de un HTML de demostración.

## Construir y revisar

```sh
npm ci
python3 -m pip install -r scripts/requirements.txt
python3 scripts/fetch_fonts.py
npm run build
npm test
npm run preview
```

La vista local utiliza el mismo Markdown y los mismos recursos que GitHub. `PROFILE_PREVIEW_PORT` permite elegir el puerto. Claro y Oscuro seleccionan las variantes correspondientes; `preview/motion.html` conserva el visor del personaje. La carpeta `preview/`, las fuentes descargadas y las copias locales no se publican.

## Contenido y recursos

- `scripts/build_profile.py`: construcción y composición del README.
- `scripts/profile_layout.py`: presentación, proyectos, cifras y contacto.
- `scripts/markdown_art.py`: títulos, tecnologías y gráfico de actividad.
- `scripts/svg_assets.py` y `scripts/art.py`: imágenes embebidas y tipografía vectorial.
- `scripts/signature.py`, `contour_field.py` y `compile_kitsune.mjs`: banner aprobado y actuación del kitsune.
- `assets/profile/sections/`: recursos del cuerpo; `identity/` conserva los originales y el motor del personaje.

El contacto usa texto enlazado real, para que GitHub aplique su subrayado al pasar el cursor. Su color y tipografía de enlace siguen la interfaz de GitHub; el contenido no simula este comportamiento únicamente en la vista local.

## Estadísticas

La acción de `.github/workflows/profile-stats.yml` consulta los repositorios públicos propios, lenguajes por bytes y contribuciones visibles; conserva el último resultado completo si la consulta falla. El calendario cubre 365 días. El flujo está preparado para ejecutarse cada hora, al minuto 23 UTC, una vez publicado y habilitado. No implica actualización instantánea ni garantiza que GitHub mantenga la programación indefinidamente.

Los datos reflejan lo que clasifica GitHub. Los 279 bytes detectados como Hack proceden de dos parciales HTML con extensión PHP en `php-course/ruleta-europea/includes/`: `header.php` (178) y `footer.php` (101).

## Copia anterior a la limpieza

`.cache/archive/pre-final-cleanup-2026-11-20.tar.gz` conserva las versiones anteriores, exploraciones de marca, generadores descartados y sus recursos. También permanece la instantánea aprobada en `.cache/snapshots/readme-aprobado-2026-11-20/`. Ninguna copia forma parte del README público. La limpieza no crea commits ni publica cambios.

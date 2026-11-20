# El kitsune: comportamiento, actuación y límites

El personaje conserva el retrato aprobado. No se ha sustituido por una mascota nueva ni por la variante de la gema. La firma, el nombre, el zarcillo y el fondo orgánico se mantienen.

## Qué hay ahora

Un director determinista con 24 comportamientos. Cada gesto tiene una entrada, una intención, una pose mantenida, una salida, efectos sobre el estado interno y un tiempo mínimo antes de repetirse. No se utiliza `Math.random`.

El repertorio incluye saludar, escuchar, parpadear despacio, mirar a ambos lados, explorar, acercarse, mirar arriba, pensar, concentrarse, asentir, negar suavemente, preguntar con la mirada, guiñar, sonreír con complicidad, reír, sorprenderse, celebrar, estirarse, suspirar, luchar contra el sueño, dormir, despertar y despedirse.

Energía, curiosidad, atención social y esfuerzo cambian con el tiempo y las acciones. El director puntúa las necesidades, respeta los descansos y recuerda las acciones anteriores. Dormir recupera energía; pensar y concentrarse incrementan el esfuerzo. Al terminar de dormir, despertar tiene prioridad. Si hay fatiga extrema, recuperarse pasa por delante de los estímulos pendientes.

Las señales se guardan en una cola limitada de seis elementos y caducan a los 18 segundos. Despertar y sorpresa tienen prioridad sobre el interés ordinario. Una señal bloqueada por el descanso de un gesto no impide atender otra válida. La acción actual termina antes de cambiar; las pausas permiten volver a una expresión neutral.

El parpadeo tiene cierre rápido, contacto y apertura más lenta, con una pauta reproducible de intervalos y dobles parpadeos. Se aplaza cuando el gesto ya mantiene los ojos cerrados. La respiración es muy pequeña. La mirada responde al puntero con aproximación y retirada suaves en la vista interactiva.

## Lo que utiliza el README

El banner lleva una actuación de **180 segundos**, con **20 acciones dirigidas**, pausas y transiciones. Las señales de esa actuación están escritas explícitamente: no se simula que GitHub detecte al usuario. Se ejecuta el mismo director al exportar y se convierten sus resultados en animaciones CSS dentro del SVG.

Los 24 comportamientos están disponibles en la biblioteca de pruebas; no todos necesitan aparecer en cada actuación. El ciclo termina con dos segundos de regreso a la pose inicial. Las pistas se simplifican con tolerancias pequeñas, conservando los puntos de los parpadeos y reduciendo el tamaño del recurso. El banner de escritorio claro pesa aproximadamente 580 kB, con todas las imágenes incorporadas y sin peticiones adicionales.

GitHub muestra el SVG como imagen: **no ejecuta el motor JavaScript ni permite interacción con el personaje**. La versión interactiva de la revisión sirve para probar y reutilizar la lógica más adelante. Sigue siendo un retrato animado por capas, no un modelo tridimensional articulado de cuerpo completo.

## Revisarlo

1. `npm run build` genera el README y sus recursos. Requiere Python con FontTools y Node 22 o posterior; la compilación del director no tiene dependencias npm.
2. `npm run preview` abre el servidor local. Visitar `/preview/motion.html`.
3. Probar la actuación, la cámara lenta y el modo autónomo. Las señales añaden motivos para reaccionar. La biblioteca permite revisar cada gesto y recorrerlo con la barra de tiempo.
4. `npm test` comprueba el contenido del perfil y el comportamiento del personaje.

El motor se encuentra en `assets/profile/identity/kitsune-3d/director.mjs`. No depende del navegador. `signal({type, x, y})` introduce un estímulo; `advance(segundos)` avanza la simulación; `snapshot()` devuelve pose, necesidades y motivo. `renderPose(svg, pose)` es el adaptador opcional para las capas SVG y conserva sus referencias para evitar búsquedas repetidas en cada fotograma. La vista de revisión pausa el avance al ocultarse la pestaña y respeta movimiento reducido. No se ha construido todavía un portfolio.

## Expresiones e identidad

La base aprobada y el parpadeo original se comprueban mediante SHA-256 en `approved-art.json`. Se utilizan cuatro etapas de párpados, cuatro direcciones de mirada y cuatro expresiones adicionales de boca. Los recortes de ojos comparten posición y proporciones; la boca utiliza una máscara suave. No se modifica la frente, las orejas, el contorno de la cabeza ni el pendiente.

El parpadeo responde a una presión acumulada: la fijación lo retrasa, cerrar los ojos alivia esa presión y terminar una tarea de concentración favorece el siguiente parpadeo. No se eligen intervalos aleatorios.

Las seis nuevas expresiones se generaron con la herramienta integrada de imágenes, editando el original como referencia única. Los PNG completos se guardan en `assets/profile/identity/kitsune-3d/source/expressions/`. Los WebP son recortes técnicos de esos recursos. Los prompts exactos están en [expression-prompts.md](../assets/profile/identity/kitsune-3d/expression-prompts.md); los anteriores de párpados están en [animation-prompts.md](../assets/profile/identity/kitsune-3d/animation-prompts.md).

## Investigación aplicada

- [Game AI Pro · An Introduction to Utility Theory](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter09_An_Introduction_to_Utility_Theory.pdf): puntuación de necesidades, inercia de la acción y descansos para evitar cambios continuos. Se adapta el principio a un personaje de firma; no se afirma equivalencia con la IA de un videojuego comercial.
- [MDN · Scripting SVG](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/Scripting): un SVG utilizado como imagen no ejecuta sus scripts. Por ello se entrega la actuación declarativa en el README y se separa el director interactivo.
- Fondo: adaptación existente del campo escalar real de `ContourBackground.jsx` de VCode; se conserva en `scripts/contour_field.py`.

## Verificaciones

Las pruebas cubren determinismo con distintas frecuencias, las 24 entradas y salidas, límites de expresiones y necesidades, continuidad de giro y escala, cola y descansos, sueño y despertar, transición de la mirada, sesiones autónomas de veinte minutos simulados y recursos exportados sin scripts ni imágenes remotas. La apariencia se revisa además en navegador: una prueba numérica no detecta por sí sola un recorte de párpados mal registrado.

# Kitsune con volumen · Víctor

Creado con el generador de imágenes integrado, usando el Memoji aportado por Víctor como referencia de estilo y personalidad. No se modifica el Memoji original. Es una ilustración con acabado 3D, no un modelo 3D interactivo.

## Archivos

- `source/open.png`: original transparente con los ojos abiertos.
- `source/blink.png`: original transparente para el parpadeo.
- `open.webp` y `blink.webp`: recursos optimizados a 256 px para el banner, conservando transparencia. Los originales quedan intactos.
- `../kitsune-live.svg`: detalle animado, con el cambio de ojos limitado a su zona para que el resto del pelaje no salte entre fotogramas.

La cabeza sustituye al punto de la i. Se conserva el zarcillo del lado izquierdo de la imagen. El gesto de cabeza está anclado a la base para mantener la relación con la letra. Con movimiento reducido se muestra el fotograma abierto estático.

## Prompt de creación

Use case: stylized-concept.
Asset type: one premium 3D avatar head for Víctor's personal signature, on a genuinely transparent background.
Input image 1 is ONLY a style and personality reference: Víctor's existing Memoji. Do not edit that Memoji or make a human/fox hybrid.
Create an original elegant male kitsune fox HEAD ONLY, straight-on, centered, both ears fully visible. Warm chocolate brown and ivory, no orange. Sculpted soft 3D volume, subtle satin material, restrained very short soft fur, refined render quality comparable to a high quality expressive phone avatar. The head must read as a fox, not a cat or dog. Long tapered ears, refined short muzzle, sweeping ivory cheek shapes. Brown eyes with lively catchlights, attentive gently raised eyebrows, warm mischievous smile. Small dark silver hoop earring on the ear at image-left, echoing the reference. Tiny subtle ivory forehead marking is acceptable.
Personality: curious, clever, friendly, composed, a quiet Japanese guardian character. It must feel designed for a creative adult, not a children's toy. Visually strong at 40 pixels: large clean shapes, expressive eyes, controlled detail. No body, no shoulders, no hair wig, no clothes, no crown, no tail fan, no energy orb, no glow or aura, no background, no cast shadow outside the head, no writing, no watermarks. Framing: head occupies about 85% of a square canvas with transparent padding. Both ears and the earring completely in frame. Production ready transparent PNG.

## Prompt del fotograma de parpadeo

Use case: precise-object-edit / identity-preserve.
Edit target image 1: the supplied 3D brown and ivory fox head.
Create exactly the SAME head, same framing, position, size, lighting, fur, colors, earring, forehead mark, cheek silhouette and open smiling mouth. Change ONLY the eyes to a natural fully closed blink: curved relaxed eyelids, no visible pupils or whites. Do not change the eyebrows or any other part of the face. This image is the closed-eye frame for an animation and must register pixel-aligned with the reference as closely as possible. Preserve the same genuinely transparent background and dimensions. No new objects or text.

## Ampliación de la animación conservando el retrato aprobado

`source/open.png`, `source/blink.png`, `open.webp` y `blink.webp` se mantienen intactos. Se han verificado sus huellas antes y después del trabajo.

Los nuevos `source/quarter.png`, `half.png`, `near.png`, `left.png` y `right.png` son fotogramas de ojos generados con el retrato original como única referencia. Solo se utilizan sus regiones de ojos, recortadas en `eyes-*.webp`. `eyes-closed.webp` procede del parpadeo original. La zona de la frente, el pelaje, las orejas, el zarcillo continúan procediendo siempre de la imagen aprobada. Esta fase inicial se amplía a continuación con expresiones de boca.

Los prompts exactos de estos fotogramas están en [animation-prompts.md](animation-prompts.md). El modo utilizado es el generador de imágenes integrado. No se utiliza la variante experimental `kitsune-divine`.

La secuencia combina parpadeos completos e intermedios, miradas laterales, un guiño ocasional, pausas e inclinaciones suaves. Se puede revisar en `preview/motion.html`, incluyendo cámara lenta y pausa. La versión de GitHub se mantiene como SVG sin controles ni JavaScript.

## Director de comportamiento

La versión actual utiliza `director.mjs`: 24 comportamientos, estado interno, señales priorizadas, memoria y pausas. `performance.json` contiene la actuación de tres minutos exportada al README. Se conserva el retrato original debajo de los recortes de ojos y boca.

Los nuevos originales están en `source/expressions/`. Sus seis prompts y el modo de generación integrado están en [expression-prompts.md](expression-prompts.md). Los recortes de ojos se han unificado a la región 300,650 de 654×230 px; los de boca a 400,900 de 460×280 px, sobre originales de 1254×1254. Se codifican como WebP de 256 px de ancho. `open.webp` y `blink.webp` permanecen intactos.

Ver [documentación del director](../../../../docs/KITSUNE-DIRECTOR.md) para uso, decisiones, investigación y verificaciones.

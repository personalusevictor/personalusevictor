# Expresiones dirigidas · fuente y prompts

Modo: herramienta integrada de generación de imágenes. Ediciones del retrato aprobado `source/open.png`, con transparencia. No se utilizó CLI/API externa. Los PNG completos se conservan en `source/expressions/`; los WebP son recortes técnicos para superponer únicamente ojos o boca. La cara base, zarcillo, marca de pelo y paleta permanecen intactos.

## mouth-neutral

Archivo: `source/expressions/mouth-neutral.png`

Use case: precise-object-edit / identity-preserve. Image 1 is the LOCKED approved kitsune portrait. This is an animation frame of exactly that character, not a redesign. Keep the exact brown/ivory fur, brown eyes, ivory FUR forehead mark (never a gem), ears, silver hoop at image-left, nose, camera, head position, lighting, transparent background and canvas dimensions. Change only the mouth region as specified. Keep the muzzle silhouette and original mouth corners in the same place. No new objects, no writing, no effects. Close the open smiling mouth into a relaxed, warm CLOSED-MOUTH smile. No teeth or tongue visible. A thin natural curved smile, attentive and composed; do not change cheeks, eyes or eyebrows.

## mouth-think

Archivo: `source/expressions/mouth-think.png`

Use case: precise-object-edit / identity-preserve. Image 1 is the LOCKED approved kitsune portrait. This is an animation frame of exactly that character, not a redesign. Keep the exact brown/ivory fur, brown eyes, ivory FUR forehead mark (never a gem), ears, silver hoop at image-left, nose, camera, head position, lighting, transparent background and canvas dimensions. Change only the mouth region as specified. Keep the muzzle silhouette and original mouth corners in the same place. No new objects, no writing, no effects. Replace the open smile with a small, slightly pursed closed mouth, a restrained thoughtful 'hmm' expression. Subtle rounded lips, no teeth or tongue, not a kiss and not a pout. Do not change cheeks, eyes or eyebrows.

## mouth-laugh

Archivo: `source/expressions/mouth-laugh.png`

Use case: precise-object-edit / identity-preserve. Image 1 is the exact approved fox portrait. Make one registered mouth-animation frame of the SAME character. Keep every detail except the mouth: exact brown and ivory fur and texture, original brown eyes, original ivory fur forehead marking (NOT a gem), earring at image-left, nose, ears, pose, framing and light. Preserve the transparent background and canvas dimensions. Keep the same muzzle silhouette and mouth-corner locations. No new objects, marks or effects. Change ONLY the mouth to a warm joyful laugh, slightly more open than the reference, with a relaxed lower lip and natural tongue/upper teeth. Friendly and expressive, not manic. Do not add fangs or new teeth. Keep eyes and eyebrows exactly as the original.

## mouth-surprise

Archivo: `source/expressions/mouth-surprise.png`

Use case: precise-object-edit / identity-preserve. Image 1 is the exact approved fox portrait. Make one registered mouth-animation frame of the SAME character. Keep every detail except the mouth: exact brown and ivory fur and texture, original brown eyes, original ivory fur forehead marking (NOT a gem), earring at image-left, nose, ears, pose, framing and light. Preserve the transparent background and canvas dimensions. Keep the same muzzle silhouette and mouth-corner locations. No new objects, marks or effects. Change ONLY the mouth into a small rounded open 'oh' expression of gentle curiosity/surprise. No visible teeth; a small oval mouth rather than a huge scream. Keep eyes and eyebrows exactly as the original.

## eyes-up

Archivo: `source/expressions/eyes-up.png`

Use case: precise-object-edit / identity-preserve. Image 1 is the approved fox portrait. Keep EXACTLY this character, its brown/ivory fur, original BROWN eye color, ivory forehead FUR marking (no gem), earrings, open smile, head position, ears, brows, camera, lighting, transparency and canvas dimensions. Change ONLY the pupils/irises direction within the normally open eyes. No redesign or added features. This frame is for a masked eye animation over the original. Both eyes look gently UPWARD, about 12 degrees, as if considering an idea just above the viewer. Natural binocular alignment. Do not tilt the head or raise the eyebrows.

## eyes-down

Archivo: `source/expressions/eyes-down.png`

Use case: precise-object-edit / identity-preserve. Image 1 is the approved fox portrait. Keep EXACTLY this character, its brown/ivory fur, original BROWN eye color, ivory forehead FUR marking (no gem), earrings, open smile, head position, ears, brows, camera, lighting, transparency and canvas dimensions. Change ONLY the pupils/irises direction within the normally open eyes. No redesign or added features. This frame is for a masked eye animation over the original. Both eyes look gently DOWNWARD, about 12 degrees, as if inspecting something below the viewer. Natural binocular alignment. Do not tilt the head or lower the eyebrows.

Las dos miradas verticales se identificaron por inspección visual: up mira hacia arriba, down hacia abajo. El nombre final describe el resultado, no el orden en que terminó cada generación.


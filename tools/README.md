# Signature artwork

`build_signature.py` builds the self-contained `surya.svg` from the original `rose.png` and the preserved cursive outlines and pen paths in `handwriting-source.svg`.

The shared background extends actual 24 by 8 pixel glyph tiles from the supplied rose image, preserving the source row and character phase. Tiles containing gray rose pixels are excluded. The rose region remains pixel-for-pixel identical to the source. There is no recoloring or uniform replacement of its red field. `assets/scene-texture.png` is the composed texture embedded in the final SVG.

The signature reveals a charcoal conversion of that same texture along eight pen paths over six seconds, holds the completed name for four seconds, and repeats. All paths share a ten-second clock so the writing order resets together. This keeps the handwriting active when a browser reuses the README image. It is larger and lower beside the rose, with a narrow outline for small-screen readability.

Build dependencies: Python, Pillow, NumPy. Run `python tools/build_signature.py`.

Browser validation uses Playwright with installed Windows Chrome: `python tools/verify_signature.py`. It captures the writing, completed hold, cycle reset, and second pass at desktop width, plus the completed composition at a 390 pixel mobile width. Assertions check that all pens reset together and repeat in the same order. Stroke offsets are recorded in `verification/animation-check.json`.

`python tools/verify_embed.py` checks the SVG as a standalone image embedded in HTML, matching the README embedding behavior. It captures the completed image after 6.5 seconds in `verification/readme-image-embed.png`.

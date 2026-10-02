# Snap every pixel to the six E Ink Spectra 6 colors (no dithering) so text stays crisp.
import sys
from PIL import Image
PALETTE = [(0,0,0),(255,255,255),(208,32,26),(242,197,0),(28,138,60),(27,79,191)]
src = sys.argv[1]
img = Image.open(src).convert("RGB")
pal = Image.new("P", (1, 1))
flat = [c for rgb in PALETTE for c in rgb]
pal.putpalette(flat + flat[:3] * (256 - len(PALETTE)))
img.quantize(palette=pal, dither=Image.Dither.NONE).convert("RGB").save(src, optimize=True)
print("quantized", src, img.size)

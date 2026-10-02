# Picks a photo from the shared Google Photos album and makes photo.png for the display:
# cropped to the photo panel (262x364) and dithered to the six E Ink Spectra 6 colors.
# A different photo is chosen every hour. If anything fails, no photo.png is written and
# the page shows a placeholder instead, so the plan itself always renders.
import io, os, re, sys, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageEnhance, ImageOps

ALBUM = os.environ.get("ALBUM_URL") or (
    "https://photos.google.com/share/AF1QipMp2zhF1zyFHB2Lj5cv5UZY24D3LplQbN8BrczfrZw7p13bRqsmQ66JyAZAa3y2XQ"
    "?key=UG9hY1lYcGI4aDFxTEc3Q3FWOURRaWlFaEwxcjRR")
SIZE = (262, 364)
CHANGE_EVERY_HOURS = 1
PALETTE = [(0,0,0),(255,255,255),(208,32,26),(242,197,0),(28,138,60),(27,79,191)]
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()

def album_photos():
    html = get(ALBUM).decode("utf-8", "ignore")
    # Photo entries look like ["https://lh3.googleusercontent.com/pw/AP1Gcz...",4032,3024,...
    urls = re.findall(r'\["(https://lh3\.googleusercontent\.com/pw/[^"]+)",(\d+),(\d+)', html)
    seen, out = set(), []
    for u, w, h in urls:
        if u not in seen and int(w) > 300:   # skip avatars and thumbnails
            seen.add(u); out.append(u)
    return out

def dither(img):
    pal = Image.new("P", (1, 1))
    flat = [c for rgb in PALETTE for c in rgb]
    pal.putpalette(flat + flat[:3] * (256 - len(PALETTE)))
    return img.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")

def main():
    photos = album_photos()
    print(f"found {len(photos)} photos in the album")
    if not photos:
        return
    now = datetime.now(ZoneInfo("America/New_York"))
    slot = int(now.timestamp()) // (3600 * CHANGE_EVERY_HOURS)
    idx = (slot * 7919) % len(photos)   # step through the album in a shuffled-looking but stable order
    img = Image.open(io.BytesIO(get(photos[idx] + "=w1200-h1200")))
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = ImageOps.fit(img, SIZE, Image.Resampling.LANCZOS, centering=(0.5, 0.38))  # favor the top, where faces usually are
    img = ImageEnhance.Color(img).enhance(1.4)       # e-ink colors are muted; push them a bit
    img = ImageEnhance.Contrast(img).enhance(1.15)
    dither(img).save("photo.png", optimize=True)
    print(f"photo.png <- photo {idx + 1}/{len(photos)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("photo skipped:", e, file=sys.stderr)

# Picks a photo from the shared Google Photos album and makes photo.png for the display:
# cropped around the faces in it (OpenCV YuNet face finder), sized for the photo panel (324x364, about 40% of the screen), and dithered to the six E Ink Spectra 6 colors.
# A different photo is chosen every 15 minutes. If anything fails, no photo.png is written and
# the page shows a placeholder instead, so the plan itself always renders.
# If no faces are found (or the face model is missing), it falls back to a crop that favors the top.
# On Friday from 4 pm and all of Saturday (or with SHABBAT=1) it also writes shabbat.png: a landscape
# photo filling the whole 800x480 screen, for the Shabbat screen.
# PREVIEW=1 also writes crops-preview.png: every album photo with its faces (red) and crop (green).
import io, os, re, sys, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageEnhance, ImageOps

FACE_MODEL = "face_detection_yunet_2023mar.onnx"   # downloaded by the GitHub job
ALBUM = os.environ.get("ALBUM_URL") or (
    "https://photos.google.com/share/AF1QipMp2zhF1zyFHB2Lj5cv5UZY24D3LplQbN8BrczfrZw7p13bRqsmQ66JyAZAa3y2XQ"
    "?key=UG9hY1lYcGI4aDFxTEc3Q3FWOURRaWlFaEwxcjRR")
SIZE = (324, 364)
FULL = (800, 480)      # the whole screen, for the Shabbat photo
SHABBAT_START_HOUR = 16
CHANGE_EVERY_MINUTES = 15
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
            seen.add(u); out.append((u, int(w), int(h)))
    return out

def dither(img):
    pal = Image.new("P", (1, 1))
    flat = [c for rgb in PALETTE for c in rgb]
    pal.putpalette(flat + flat[:3] * (256 - len(PALETTE)))
    return img.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")

def find_faces(img):
    """Face boxes (x, y, w, h) in img's pixels, biggest first. Background faces are dropped."""
    try:
        import cv2, numpy as np
    except ImportError:
        return []
    if not os.path.exists(FACE_MODEL):
        return []
    scale = min(1.0, 960 / max(img.size))   # YuNet is quick and accurate at about this size
    small = img.resize((round(img.width * scale), round(img.height * scale))) if scale < 1 else img
    bgr = cv2.cvtColor(np.array(small), cv2.COLOR_RGB2BGR)
    det = cv2.FaceDetectorYN.create(FACE_MODEL, "", small.size, 0.7, 0.3, 5000)
    _, found = det.detect(bgr)
    if found is None:
        return []
    faces = sorted(([float(v) / scale for v in f[:4]] for f in found), key=lambda f: -f[2] * f[3])
    big = faces[0][2]
    return [f for f in faces if f[2] >= big * 0.35]   # people far in the background don't steer the crop

def crop_box(w, h, faces, size=SIZE):
    """The crop (left, top, right, bottom) with the target's shape that keeps the faces in frame."""
    aspect = size[0] / size[1]
    cw = min(w, h * aspect); ch = cw / aspect               # the biggest crop that fits
    if not faces:
        left, top = (w - cw) / 2, (h - ch) * 0.2           # favor the top, where faces usually are
        return (left, top, left + cw, top + ch)
    # Framing priorities: 1) every face in the crop  2) faces at the top, with 10% of the
    # frame as space above the highest head  3) the group centered left to right.
    head = min(f[1] - f[3] * 0.3 for f in faces)          # top of the highest head (hair above the face box)
    chin = max(f[1] + f[3] * 1.1 for f in faces)          # bottom of the lowest face
    fx0 = min(f[0] - f[2] * 0.25 for f in faces); fx1 = max(f[0] + f[2] * 1.25 for f in faces)
    # 1) the smallest crop that still holds every face (with the 10% headroom)
    need = min(cw, max(fx1 - fx0, (chin - head) / 0.9 * aspect))
    full = cw
    cw = max(need, full * 0.4)                             # usually no closer than 40% of the frame (sharpness)
    # 2) faces low in the photo: zoom in further (down to 25%, never cutting a face) so heads still reach the top
    fits_top = (h - head) / 0.9 * aspect
    if fits_top < cw:
        cw = max(need, fits_top, full * 0.25)
    cw = min(cw, full); ch = cw / aspect
    if fx1 - fx0 <= cw:
        cx = (fx0 + fx1) / 2
    else:
        # the group is wider than the crop: slide across and keep the most (and biggest) faces whole
        def score(left):
            return sum(f[2] * f[3] for f in faces if f[0] >= left and f[0] + f[2] <= left + cw)
        lefts = [max(0.0, min(w - cw, f[0] - f[2] * 0.3)) for f in faces] + \
                [max(0.0, min(w - cw, f[0] + f[2] * 1.3 - cw)) for f in faces]
        best = max(lefts, key=lambda l: (score(l), -abs(l + cw / 2 - (fx0 + fx1) / 2)))
        cx = best + cw / 2
    left = max(0.0, min(w - cw, cx - cw / 2))
    top = max(0.0, min(h - ch, head - ch * 0.10))             # 10% of the frame above the highest head
    return (left, top, left + cw, top + ch)

def prepare(img, size=SIZE):
    img = ImageOps.exif_transpose(img).convert("RGB")
    faces = find_faces(img)
    box = crop_box(img.width, img.height, faces, size)
    out = img.crop(tuple(round(v) for v in box)).resize(size, Image.Resampling.LANCZOS)
    out = ImageEnhance.Color(out).enhance(1.4)       # e-ink colors are muted; push them a bit
    out = ImageEnhance.Contrast(out).enhance(1.15)
    return dither(out), faces, box, img

def preview(photos):
    from PIL import ImageDraw
    cells = []
    for u, _, _ in photos:
        try:
            done, faces, box, img = prepare(Image.open(io.BytesIO(get(u + "=w1200-h1200"))))
        except Exception as e:
            print("preview skipped a photo:", e, file=sys.stderr); continue
        t = 300 / img.height
        thumb = img.resize((round(img.width * t), 300)); d = ImageDraw.Draw(thumb)
        for x, y, fw, fh in faces:
            d.rectangle([x * t, y * t, (x + fw) * t, (y + fh) * t], outline=(255, 0, 0), width=3)
        d.rectangle([v * t for v in box], outline=(0, 255, 0), width=4)
        cell = Image.new("RGB", (thumb.width + 10 + round(SIZE[0] * 300 / SIZE[1]), 300), "white")
        cell.paste(thumb, (0, 0)); cell.paste(done.resize((round(SIZE[0] * 300 / SIZE[1]), 300)), (thumb.width + 10, 0))
        cells.append(cell)
    if not cells:
        return
    cols, cw = 3, max(c.width for c in cells)
    sheet = Image.new("RGB", (cols * (cw + 20), -(-len(cells) // cols) * 320), "white")
    for i, c in enumerate(cells):
        sheet.paste(c, ((i % cols) * (cw + 20), (i // cols) * 320))
    sheet.save("crops-preview.png", optimize=True)
    print(f"crops-preview.png <- {len(cells)} photos")

def main():
    photos = album_photos()
    print(f"found {len(photos)} photos in the album")
    if not photos:
        return
    if os.environ.get("PREVIEW") == "1":
        preview(photos)
    now = datetime.now(ZoneInfo("America/New_York"))
    slot = int(now.timestamp()) // (60 * CHANGE_EVERY_MINUTES)
    idx = (slot * 7919) % len(photos)   # step through the album in a shuffled-looking but stable order
    done, faces, box, _ = prepare(Image.open(io.BytesIO(get(photos[idx][0] + "=w2000-h2000"))))
    done.save("photo.png", optimize=True)
    print(f"photo.png <- photo {idx + 1}/{len(photos)}, {len(faces)} face(s), crop {[round(v) for v in box]}")
    shabbat = (now.weekday() == 4 and now.hour >= SHABBAT_START_HOUR) or now.weekday() == 5
    if shabbat or os.environ.get("SHABBAT") == "1":
        wide = [p for p in photos if p[1] >= p[2]] or photos   # landscape photos fill the screen best
        p = wide[(slot * 7919) % len(wide)]
        done, faces, box, _ = prepare(Image.open(io.BytesIO(get(p[0] + "=w1600-h1600"))), FULL)
        done.save("shabbat.png", optimize=True)
        print(f"shabbat.png <- {len(wide)} landscape photos, {len(faces)} face(s), crop {[round(v) for v in box]}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("photo skipped:", e, file=sys.stderr)

"""Pad and restore cropped arch crowns on doorway images 2–4 to match 1.jpg."""
from PIL import Image, ImageFilter
import os
import math
import random

base = r"C:\Web Projects\Rajasthan\assets"
bak = os.path.join(base, "_arch_backup")
os.makedirs(bak, exist_ok=True)


def sample_arch_color(im):
    w, h = im.size
    samples = []
    for y in range(0, min(120, h), 2):
        for x in list(range(0, max(1, w // 7), 2)) + list(range(6 * w // 7, w, 2)):
            samples.append(im.getpixel((x, y)))
    samples = sorted(samples, key=lambda p: sum(p))[: max(1, len(samples) // 2)]
    r = sum(p[0] for p in samples) // len(samples)
    g = sum(p[1] for p in samples) // len(samples)
    b = sum(p[2] for p in samples) // len(samples)
    return (r, g, b)


def find_opening_top(im):
    w, h = im.size
    cx = w // 2
    for y in range(0, h // 3):
        r, g, b = im.getpixel((cx, y))
        if (r + g + b) / 3 > 55:
            return y
    return 0


def find_pillar_edges(im, y_probe=None):
    w, h = im.size
    if y_probe is None:
        y_probe = max(h // 5, find_opening_top(im) + 40)
    left = 0
    for x in range(0, w // 2):
        if sum(im.getpixel((x, y_probe))) / 3 > 48:
            left = x
            break
    right = w - 1
    for x in range(w - 1, w // 2, -1):
        if sum(im.getpixel((x, y_probe))) / 3 > 48:
            right = x
            break
    return left, right


def restore_arch(path, target_crown=42):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    opening_y = find_opening_top(im)
    left, right = find_pillar_edges(im)
    arch = sample_arch_color(im)

    missing = max(0, target_crown - opening_y)
    headroom = 12
    pad = missing + headroom

    if pad < 8 and opening_y >= target_crown - 5:
        print(f"{os.path.basename(path)}: already ok (opening_y={opening_y}), skip")
        return False

    bpath = os.path.join(bak, os.path.basename(path))
    if not os.path.exists(bpath):
        im.save(bpath, quality=95)

    new_h = h + pad
    out = Image.new("RGB", (w, new_h), arch)

    random.seed(hash(os.path.basename(path)) & 0xFFFF)
    noise = Image.new("RGB", (w, pad + target_crown + 24), arch)
    px = noise.load()
    for yy in range(noise.size[1]):
        for xx in range(w):
            d = random.randint(-6, 6)
            r = max(0, min(255, arch[0] + d))
            g = max(0, min(255, arch[1] + d // 2))
            b = max(0, min(255, arch[2] + d // 3))
            edge = min(xx, w - 1 - xx)
            lim = max(1, int(left * 0.85))
            if edge < lim:
                f = edge / lim
                r = int(r * (0.55 + 0.45 * f))
                g = int(g * (0.55 + 0.45 * f))
                b = int(b * (0.55 + 0.45 * f))
            px[xx, yy] = (r, g, b)
    noise = noise.filter(ImageFilter.GaussianBlur(0.8))
    out.paste(noise.crop((0, 0, w, pad + 4)), (0, 0))

    # Interior fill for padded zone (extend from original opening top)
    top_strip = im.crop(
        (0, max(0, opening_y), w, max(opening_y + 1, min(h, opening_y + 60)))
    )
    fill_h = pad + target_crown + 30
    interior_fill = top_strip.resize((w, max(1, fill_h)), Image.Resampling.LANCZOS)
    interior_fill = interior_fill.filter(ImageFilter.GaussianBlur(1.2))

    draw_layer = out.copy()
    draw_layer.paste(interior_fill, (0, 0))
    draw_layer.paste(im, (0, pad))

    # Inner arch opening peak (matches image 1 breathing room)
    inner_top = target_crown
    cx = (left + right) / 2.0
    rx = (right - left) / 2.0
    ry = rx * 0.92

    mask = Image.new("L", (w, new_h), 0)
    mpx = mask.load()
    zone = int(inner_top + ry) + 3
    for y in range(0, min(new_h, zone)):
        for x in range(w):
            nx = (x - cx) / max(1e-6, rx)
            if abs(nx) > 1:
                mpx[x, y] = 0 if y < pad + opening_y + 8 else 255
                continue
            y_curve = inner_top + ry * (1 - math.sqrt(max(0.0, 1 - nx * nx)))
            mpx[x, y] = 255 if y >= y_curve else 0

    for y in range(zone, new_h):
        for x in range(w):
            mpx[x, y] = 255

    mask = mask.filter(ImageFilter.GaussianBlur(0.65))
    result = Image.composite(draw_layer, out, mask)
    result.save(path, quality=94, optimize=True)
    print(
        f"{os.path.basename(path)}: pad={pad}px opening was {opening_y} "
        f"-> new {w}x{new_h}"
    )
    return True


if __name__ == "__main__":
    for i in (2, 3, 4):
        restore_arch(os.path.join(base, f"{i}.jpg"), target_crown=42)

    print("\nVerification:")
    for i in range(1, 5):
        im = Image.open(os.path.join(base, f"{i}.jpg")).convert("RGB")
        print(f"{i}.jpg {im.size} opening_top={find_opening_top(im)}")

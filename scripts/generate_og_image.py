#!/usr/bin/env python3
"""Generate 1200x630 Open Graph image with avatar for social sharing."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
AVATAR = ROOT / "assets/img/avatar.png"
OUT = ROOT / "assets/img/og-image.jpg"

W, H = 1200, 630
BG = (7, 7, 13)
CYAN = (34, 211, 238)
AMBER = (245, 158, 11)
TEXT = (244, 244, 248)
MUTED = (148, 148, 168)


def load_font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def radial_glow(base: Image.Image, cx: int, cy: int, radius: int, color: tuple[int, int, int], alpha: int) -> None:
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    for i in range(radius, 0, -4):
        a = int(alpha * (i / radius) ** 2)
        draw.ellipse((cx - i, cy - i, cx + i, cy + i), fill=(*color, a))
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    base.paste(Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB"))


def circular_avatar(source: Image.Image, size: int) -> Image.Image:
    source = source.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(source, (0, 0), mask)
    return output


def gradient_ring(size: int, thickness: int = 8) -> Image.Image:
    ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ring)
    outer = size // 2
    inner = outer - thickness
    for angle in range(0, 360, 2):
        t = angle / 360
        if t < 0.33:
            c = CYAN
        elif t < 0.66:
            c = (129, 140, 248)
        else:
            c = AMBER
        draw.arc((outer - inner, outer - inner, outer + inner, outer + inner), angle, angle + 3, fill=(*c, 220), width=thickness)
    return ring


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    radial_glow(img, 980, 300, 260, CYAN, 55)
    radial_glow(img, 760, 420, 180, AMBER, 35)

    draw = ImageDraw.Draw(img)
    draw.line((72, 520, W - 72, 520), fill=(255, 255, 255, 18), width=1)

    title_font = load_font(54, bold=True)
    subtitle_font = load_font(28)
    label_font = load_font(18, bold=True)

    draw.rounded_rectangle((72, 118, 330, 158), radius=20, fill=(34, 211, 238, 20), outline=(34, 211, 238, 80), width=1)
    draw.text((92, 128), "FULL STACK ENGINEER", fill=CYAN, font=label_font)
    draw.text((72, 188), "Jaime Jazareno III", fill=TEXT, font=title_font)
    draw.text((72, 268), "Mobile · Web · iOS · Leadership", fill=MUTED, font=subtitle_font)
    draw.text((72, 318), "jaimejazarenoiii.me", fill=CYAN, font=subtitle_font)

    avatar_size = 320
    avatar = circular_avatar(Image.open(AVATAR), avatar_size)
    ring = gradient_ring(avatar_size + 24, 6)

    ax, ay = W - 72 - avatar_size - 12, (H - avatar_size) // 2
    img_rgba = img.convert("RGBA")
    img_rgba.paste(ring, (ax - 12, ay - 12), ring)
    img_rgba.paste(avatar, (ax, ay), avatar)
    img = img_rgba.convert("RGB")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

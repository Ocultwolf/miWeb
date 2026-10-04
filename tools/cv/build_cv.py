"""Genera el CV en PDF (A4, una página) en inglés y en español con el mismo diseño.

    python tools/cv/build_cv.py            # escribe static/portfolio/cv/Pablo_Dominguez_CV.pdf y _ES.pdf

Necesita reportlab y pillow. El texto está en content.py; aquí solo el diseño, calibrado sobre el
CV original (barra lateral oscura con foto, columna principal clara, acentos ámbar).
"""

from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content import CONTACT, CV  # noqa: E402

OUT_DIR = HERE.parent.parent / "static" / "portfolio" / "cv"
OUTPUTS = {"en": "Pablo_Dominguez_CV.pdf", "es": "Pablo_Dominguez_CV_ES.pdf"}

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("DV", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-B", str(FONT_DIR / "DejaVuSans-Bold.ttf")))

W, H = A4
PAPER = (0.964706, 0.956863, 0.941176)
SIDEBAR = (0.086275, 0.12549, 0.168627)
AMBER = (0.827451, 0.580392, 0.290196)
INK = (0.109804, 0.133333, 0.152941)
GREY = (0.356863, 0.4, 0.447059)
SIDE_MUTED = (0.658824, 0.705882, 0.74902)
RULE_LIGHT = (0.894118, 0.878431, 0.847059)
WHITE = (1, 1, 1)

SIDE_X, SIDE_W = 20.0, 155.0          # contenido de la barra lateral: x 20 → 175
MAIN_X, MAIN_R = 223.0, 563.3         # columna principal
ASC = 0.76                            # ascendente aproximado de DejaVu para pasar de "top" a línea base


class Page:
    def __init__(self, c: canvas.Canvas):
        self.c = c

    def text(self, x, top, s, font, size, color, anchor="left"):
        self.c.setFont(font, size)
        self.c.setFillColorRGB(*color)
        y = H - top - size * ASC
        if anchor == "center":
            self.c.drawCentredString(x, y, s)
        elif anchor == "right":
            self.c.drawRightString(x, y, s)
        else:
            self.c.drawString(x, y, s)

    def rule(self, x0, x1, top, color, width):
        self.c.setStrokeColorRGB(*color)
        self.c.setLineWidth(width)
        self.c.line(x0, H - top, x1, H - top)

    def wrap(self, s, font, size, width):
        words, lines, cur = s.split(), [], ""
        for w in words:
            cand = f"{cur} {w}".strip()
            if pdfmetrics.stringWidth(cand, font, size) <= width:
                cur = cand
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, top, s, font, size, color, width, leading):
        for i, line in enumerate(self.wrap(s, font, size, width)):
            self.text(x, top + i * leading, line, font, size, color)
        return top + (len(self.wrap(s, font, size, width)) - 1) * leading

    def dot(self, x, top, color, r=1.6):
        self.c.setFillColorRGB(*color)
        self.c.circle(x + r, H - top - r, r, stroke=0, fill=1)


def sidebar(p: Page, d: dict) -> None:
    c = p.c
    # Foto en círculo con borde ámbar
    x, top, size = 38.5, 40.0, 118.0
    cx, cy = x + size / 2, H - top - size / 2
    c.saveState()
    path = c.beginPath()
    path.circle(cx, cy, size / 2)
    c.clipPath(path, stroke=0, fill=0)
    c.drawImage(ImageReader(str(HERE / "photo.png")), x, H - top - size, size, size, mask="auto")
    c.restoreState()
    c.setStrokeColorRGB(*AMBER)
    c.setLineWidth(2)
    c.circle(cx, cy, size / 2, stroke=1, fill=0)

    center = SIDE_X + SIDE_W / 2 + 2.5
    p.text(center, 179.1, "Pablo", "DV-B", 17, WHITE, "center")
    p.text(center, 199.1, "Dominguez", "DV-B", 17, WHITE, "center")
    for i, line in enumerate(d["subtitle"]):
        p.text(center, 221.0 + i * 12.0, line, "DV", 9.2, AMBER, "center")

    def section(title, top):
        p.text(SIDE_X, top, title, "DV-B", 9.5, AMBER)
        p.rule(SIDE_X, SIDE_X + SIDE_W, top + 12.2, AMBER, 1.0)
        return top + 15.9

    top = section(d["contact_title"], 262.8)
    for i, item in enumerate(CONTACT + [d["location"]]):
        p.text(SIDE_X, top + i * 13.0, item, "DV", 8.3, WHITE)

    top = section(d["skills_title"], 338.5)
    top += 5.3
    for i, skill in enumerate(d["skills"]):
        p.dot(SIDE_X + 0.4, top + i * 13.0 + 2.2, AMBER)
        p.text(SIDE_X + 9.0, top + i * 13.0, skill, "DV", 8.3, WHITE)

    top = section(d["languages_title"], 483.8)
    for i, (lang, level) in enumerate(d["languages"]):
        t = top + 0.5 + i * 14.2
        p.text(SIDE_X, t, lang, "DV", 8.3, WHITE)
        p.text(SIDE_X + SIDE_W, t + 0.6, level, "DV", 7.3, SIDE_MUTED, "right")

    top = section(d["education_title"], 548.8) + 3.4
    for title, school in d["education"]:
        p.text(SIDE_X, top, title, "DV", 7.8, WHITE)
        if school:
            p.text(SIDE_X, top + 11.0, school, "DV", 7.8, WHITE)
            top += 27.0
        else:
            top += 13.3


def main_column(p: Page, d: dict) -> None:
    width = MAIN_R - MAIN_X
    p.text(MAIN_X, 35.3, d["title"], "DV-B", 22, INK)
    p.text(MAIN_X, 62.0, d["tagline"], "DV", 10.5, GREY)
    p.text(MAIN_X, 79.9, d["availability"], "DV", 8.0, AMBER)

    def section(title, top):
        p.text(MAIN_X, top, title, "DV-B", 11.5, INK)
        p.rule(MAIN_X, MAIN_R, top + 13.7, AMBER, 1.4)
        return top + 21.6

    top = section(d["about_title"], 109.3)
    last = p.para(MAIN_X, top, d["about"], "DV", 9.3, INK, width, 13.5)

    top = section(d["strengths_title"], last + 36.1)
    top += 1.0
    for name, desc in d["strengths"]:
        p.text(MAIN_X, top, name, "DV-B", 9.6, INK)
        last = p.para(MAIN_X, top + 13.8, desc, "DV", 8.6, GREY, width, 11.3)
        top = last + 20.7

    top = section(d["projects_title"], last + 31.1)
    top += 0.0
    for name, tech, desc in d["projects"]:
        p.text(MAIN_X, top, name, "DV-B", 9.8, INK)
        p.text(MAIN_X, top + 13.6, tech, "DV", 7.6, AMBER)
        last = p.para(MAIN_X, top + 25.4, desc, "DV", 8.6, GREY, width, 11.3)
        top = last + 24.0

    top = section(d["experience_title"], last + 31.1)
    last = p.para(MAIN_X, top - 1.6, d["experience_intro"], "DV", 8.2, GREY, width, 11.0)
    top = last + 22.7
    for role, place in d["experience"]:
        p.dot(MAIN_X + 0.4, top + 2.4, AMBER)
        p.text(MAIN_X + 9.0, top, role, "DV-B", 8.6, INK)
        offset = pdfmetrics.stringWidth(role, "DV-B", 8.6) + 6
        p.text(MAIN_X + 9.0 + offset, top + 0.1, f"— {place}", "DV", 8.4, GREY)
        top += 16.0

    rule_top = max(749.1, top + 8.0)  # la posición del original, salvo que el texto empuje más abajo
    p.rule(MAIN_X, MAIN_R, rule_top, RULE_LIGHT, 1.0)
    last = p.para(MAIN_X, rule_top + 13.2, d["closing"], "DV", 9.0, GREY, width, 13.0)
    if last > 790:
        raise ValueError(f"El CV ({d['title']}) no cabe en una página: el cierre acaba en {last:.0f}")
    footer = " · ".join([CONTACT[2], CONTACT[1], d["location"]])
    p.text((MAIN_X + MAIN_R) / 2, 814.3, footer, "DV", 7.3, GREY, "center")


def build(lang: str) -> Path:
    out = OUT_DIR / OUTPUTS[lang]
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle(f"Pablo Dominguez — CV ({lang.upper()})")
    c.setAuthor("Pablo Dominguez Viera")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColorRGB(*SIDEBAR)
    c.rect(0, 0, 195.0, H, stroke=0, fill=1)
    p = Page(c)
    sidebar(p, CV[lang])
    main_column(p, CV[lang])
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    langs = sys.argv[1:] or list(OUTPUTS)
    for lang in langs:
        print(build(lang))

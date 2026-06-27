"""Build the CSCI 250 Fall 2026 promotional flyer (PDF + PNG).

Uses reportlab for crisp, auto-wrapping typography (text can never overlap) and
PyMuPDF to render a PNG preview. Run: python build_flyer.py
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
QR = os.path.join(HERE, "..", "..", "assets", "qr-intro2ai.png")
PDF = os.path.join(HERE, "CSCI250-Flyer-Fall2026.pdf")
PNG = os.path.join(HERE, "CSCI250-Flyer-Fall2026.png")

NAVY = HexColor("#0B1F3A"); TEAL = HexColor("#128C8C"); LIGHT = HexColor("#EEF2F6")
INK = HexColor("#222428"); GREY = HexColor("#5B6470"); GREEN = HexColor("#2E8B57")
CREAM = HexColor("#CFE3E3"); MIST = HexColor("#9FC6C6")

W, Hh = letter            # 612 x 792
M = 50                    # side margin
CW = W - 2 * M            # content width
c = canvas.Canvas(PDF, pagesize=letter)


def para(text, size, color, leading=None, bold=False, align=0, bullet=None,
         left_indent=0, font="Helvetica"):
    st = ParagraphStyle(
        "s", fontName=("Helvetica-Bold" if bold else font), fontSize=size,
        leading=leading or size * 1.32, textColor=color, alignment=align,
        leftIndent=left_indent, bulletIndent=0, bulletFontName="Helvetica-Bold",
        bulletFontSize=size, bulletColor=TEAL)
    return Paragraph(text, st, bulletText=bullet)


def draw(p, x, top, width):
    """Draw a flowable so its TOP sits at y=top. Returns the new y (bottom)."""
    _, h = p.wrapOn(c, width, Hh)
    p.drawOn(c, x, top - h)
    return top - h


# ───────────────────────── Header (navy) ─────────────────────────
HEAD = 168
c.setFillColor(NAVY); c.rect(0, Hh - HEAD, W, HEAD, fill=1, stroke=0)
c.setFillColor(TEAL); c.rect(0, Hh - HEAD - 6, W, 6, fill=1, stroke=0)  # teal rule

c.setFillColor(MIST); c.setFont("Helvetica-Bold", 11)
c.drawString(M, Hh - 40, "P A L O M A R   C O L L E G E   ·   C O M P U T E R   S C I E N C E   ( C S I T )")
c.setFillColor(white); c.setFont("Helvetica-Bold", 30)
c.drawString(M, Hh - 78, "Introduction to")
c.drawString(M, Hh - 112, "Artificial Intelligence")
c.setFillColor(CREAM); c.setFont("Helvetica-Bold", 15)
c.drawString(M, Hh - 144, "CSCI 250    ·    Fall 2026    ·    4 Units    ·    Online")

# ───────────────────────── Tagline (light) ───────────────────────
TAG_TOP = Hh - HEAD - 6
TAG_H = 50
c.setFillColor(LIGHT); c.rect(0, TAG_TOP - TAG_H, W, TAG_H, fill=1, stroke=0)
c.setFillColor(TEAL); c.rect(0, TAG_TOP - TAG_H, 8, TAG_H, fill=1, stroke=0)
draw(para("Now with deep, hands-on coverage of <b>Large Language Models</b>, "
          "<b>Generative AI</b> &amp; <b>AI-assisted coding</b>.", 13.5, NAVY, leading=18),
     M, TAG_TOP - 16, CW)

# ───────────────────────── Intro ─────────────────────────────────
y = TAG_TOP - TAG_H - 26
y = draw(para(
    "Artificial Intelligence is the defining technology of the decade — and generative AI has "
    "put it in everyone's hands. In this <b>project-based, beginner-friendly</b> course you'll go "
    "from the fundamentals of machine learning to <b>building and deploying your own AI "
    "applications</b> using the same tools professionals use today.",
    11.5, INK, leading=16.5), M, y, CW)

# ───────────────────────── What you'll build & learn ─────────────
y -= 24
c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 15)
c.drawString(M, y, "What you'll build & learn")
c.setFillColor(TEAL); c.rect(M, y - 7, 64, 3, fill=1, stroke=0)  # accent underline
y_cols = y - 22

left = [
    "<b>ML &amp; neural-network foundations</b> in Python",
    "<b>How LLMs really work</b> — build a tokenizer and attention from scratch",
    "<b>Prompt engineering &amp; reasoning</b> with Claude &amp; Gemini",
    "<b>Retrieval-Augmented Generation (RAG)</b> over your own data",
]
right = [
    "<b>AI agents &amp; tool use</b> (Model Context Protocol)",
    "<b>AI-assisted coding</b> with Claude Code",
    "<b>Multimodal AI, fine-tuning &amp; evaluation</b>",
    "<b>Capstone:</b> build &amp; deploy your own AI assistant",
]
GAP = 34
colw = (CW - GAP) / 2


def column(items, x, top):
    yy = top
    for it in items:
        yy = draw(para(it, 11.5, INK, leading=15.5, bullet="•", left_indent=15), x, yy, colw)
        yy -= 11   # space between bullets
    return yy


yl = column(left, M, y_cols)
yr = column(right, M + colw + GAP, y_cols)
y = min(yl, yr)

# ───────────────────────── Highlight pills ───────────────────────
y -= 16
pills = [("100% Online", TEAL), ("Asynchronous", NAVY),
         ("Hands-on Projects", NAVY), ("Portfolio Capstone", TEAL)]
PS = 10.5; padx = 13; gap = 10; ph = 22
widths = [c.stringWidth(l, "Helvetica-Bold", PS) + 2 * padx for l, _ in pills]
total = sum(widths) + gap * (len(pills) - 1)
if total > CW:
    s = CW / total; widths = [w * s for w in widths]; gap *= s; total = CW
x = (W - total) / 2
for (label, color), pw in zip(pills, widths):
    c.setFillColor(color); c.roundRect(x, y - ph, pw, ph, ph / 2, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", PS)
    c.drawCentredString(x + pw / 2, y - ph + 7, label)
    x += pw + gap
y -= ph

# ───────────────────────── Tools line ────────────────────────────
y -= 22
c.setFillColor(GREY); c.setFont("Helvetica", 11)
c.drawCentredString(W / 2, y, "Tools you'll use:   Anthropic Claude   ·   Claude Code   ·   "
                              "Google Gemini   ·   Hugging Face   ·   Ollama")

# ───────────────────────── Footer (navy) ─────────────────────────
FH = 140
c.setFillColor(NAVY); c.rect(0, 0, W, FH, fill=1, stroke=0)
c.setFillColor(TEAL); c.rect(0, FH, W, 4, fill=1, stroke=0)

# QR (right) — draw first so we know the safe text width
qs = 92; qx = W - M - qs; qy = (FH - qs) / 2 + 4
c.setFillColor(white); c.roundRect(qx - 7, qy - 7, qs + 14, qs + 14, 7, fill=1, stroke=0)
if os.path.exists(QR):
    c.drawImage(QR, qx, qy, qs, qs, mask="auto")
c.setFillColor(MIST); c.setFont("Helvetica", 8)
c.drawCentredString(qx + qs / 2, qy - 17, "Scan for course info & enrollment")

# Footer info (left) — width stops well before the QR
finfo_w = qx - M - 24
ftop = FH - 24
def line(lbl, val, yy):
    c.setFillColor(MIST); c.setFont("Helvetica-Bold", 10.5); c.drawString(M, yy, lbl)
    c.setFillColor(white); c.setFont("Helvetica", 10.5)
    c.drawString(M + c.stringWidth(lbl, "Helvetica-Bold", 10.5) + 6, yy, val)
line("Instructor:", "Gheni Abla   ·   gabla@palomar.edu", ftop)
line("Prerequisite:", "CSCI 114 (grade of “C” or better)", ftop - 20)
line("Format:", "Online, fully asynchronous", ftop - 40)
c.setFillColor(HexColor("#7FE3E3")); c.setFont("Helvetica-Bold", 14)
c.drawString(M, ftop - 70, "Enroll →  palomar.edu/how-to-register")
c.setFillColor(CREAM); c.setFont("Helvetica", 9.5)
c.drawString(M, ftop - 88, "Questions or trouble enrolling?  Email gabla@palomar.edu")

c.showPage(); c.save()

# ───────────────────────── PNG preview ───────────────────────────
doc = fitz.open(PDF)
pix = doc[0].get_pixmap(dpi=150)
pix.save(PNG)
print("wrote", PDF)
print("wrote", PNG)

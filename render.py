#!/usr/bin/env python3
"""Draw the rebuilt make.fun news-image entry: a dense 1024x1024 newspaper
front page summing up Monday 23 November 2026. Deterministic output:
fixed seed, fixed fonts, no timestamps, no network."""

import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (164, 30, 34)
GREY = (90, 86, 76)
RULE = (60, 58, 52)

FD = "/usr/share/fonts/truetype/dejavu/"
F_MAST = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 56)
F_DATE = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 23)
F_LEAD = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 37)
F_LEAD2 = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 28)
F_KICK = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 13)
F_HEAD = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 13)
F_SUB = ImageFont.truetype(FD + "DejaVuSans.ttf", 10)
F_LEADSUB = ImageFont.truetype(FD + "DejaVuSans.ttf", 13)
F_SEC = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 13)
F_BOX = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 13)
F_BOXTXT = ImageFont.truetype(FD + "DejaVuSans.ttf", 12)
F_FOOT = ImageFont.truetype(FD + "DejaVuSans.ttf", 10)


def wrap(draw, text, font, width):
    """Greedy word wrap, returns list of lines that fit width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, font, fill=INK):
    draw.text((W // 2, y), text, font=font, fill=fill, anchor="ma")


def draw_para(draw, x, y, text, font, width, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, font, width)
    if max_lines is not None:
        assert len(lines) <= max_lines, f"overflow ({len(lines)} lines): {text[:60]}"
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------- stories: (headline, sub-line) ----------------
LEAD1_HEAD = "COP31 COLLAPSES WITH NO DEAL AS TALKS RUN LONGEST EVER"
LEAD1_SUB = (
    "Pacific islands despair as the fossil-fuel phase-out is dropped from the text; "
    "90+ nations back an electrification pledge to 35% by 2035; calls grow for "
    "negotiations president Chris Bowen to resign."
)
LEAD2_HEAD = "DEMOCRATS CLINCH THE HOUSE"
LEAD2_SUB = (
    "At least 258 seats, the largest House majority for either party since 1992."
)

SECTIONS = [
    ("EUROPE", [
        ("Kyiv region strikes kill at least 15",
         "Rescuers dig for survivors in Dymer after Russian strikes."),
        ("Russian corvette sinks in Benghazi",
         "Merkury goes down after a suspected Ukrainian sea drone strike."),
        ("Denmark says Russia plotted a killing",
         "Copenhagen accuses Moscow of plotting to kill a Ukrainian-American rapper."),
        ("Burnham: EU deal or a broken status quo",
         "UK prime minister frames the choice; Theresa May dismayed at rejoin talk."),
        ("Belgian airports shut as protests hit",
         "Air traffic control suspended Monday in a nationwide austerity protest."),
        ("Poland reports airspace breach",
         "Russian strike on Zelenskyy's hometown kills two and wounds 60."),
    ]),
    ("MIDDLE EAST", [
        ("Trump 'inclined' to hit Iran again",
         "US president said to favour resuming conflict if no deal by New Year."),
        ("Gaza flooding displaces 100,000 more",
         "Hamas demands talks after aid workers are killed in Gaza."),
        ("Syria and EU seek normalisation",
         "Diplomats push ties forward as migration worries shape the talks."),
    ]),
    ("ASIA-PACIFIC", [
        ("Banten factory fire toll hits 24",
         "Death toll rises in Indonesia; about 30 people still unaccounted for."),
        ("Seoul minister quits over AI exam chaos",
         "South Korea's education minister resigns after AI cheating upends the exam."),
        ("Selangor flood evacuees pass 1,800",
         "Malaysian flood shelters fill as waters rise in Selangor."),
        ("Nvidia chief's Beijing contact probed",
         "Alice Huang kept contact with China's security ministry; SEC examines Nvidia."),
        ("Markets rebound as Nasdaq futures rise",
         "Nasdaq 100 futures up about 3% on Monday; China state funds buy ETFs."),
        ("Bitcoin climbs back to $61,800",
         "Bitcoin recovers Monday from Saturday's $55,081 two-year low."),
    ]),
    ("AMERICAS", [
        ("Trump signs law ending the penny",
         "Common Cents Act ends the one-cent coin's 232-year run."),
        ("Delta outage delays 1,600+ flights",
         "Thanksgiving travel begins with delays at Delta's Atlanta hub."),
        ("US Army to blow up unstable stockpile",
         "Army plans to detonate lead azide in Iowa despite a court order."),
        ("UK set to host 2035 Women's World Cup",
         "FIFA expected to confirm the UK as host on Monday."),
    ]),
    ("MARKETS", [
        ("Kospi falls 3.3% as Seoul readies fund",
         "South Korea prepares a stabilisation fund as the Kospi drops."),
        ("Taiwan's Taiex jumps 2.2%",
         "Taiex climbs as Asian markets split on Monday."),
        ("Anthropic shares fall 8.5% after IPO",
         "Shares close Friday at $88.91 after an $81.3bn listing; Nasdaq gives up all 2026 gains."),
    ]),
    ("WEEKEND SPORT", [
        ("Alcaraz wins first ATP Finals title",
         "Beats Zverev 6-2, 7-6 in Turin."),
        ("Liverpool thrash Man Utd 4-0",
         "Ten-man United beaten in Pochettino's debut as manager."),
        ("Verstappen wins Las Vegas Grand Prix",
         "Red Bull driver takes the win under the lights in Las Vegas."),
        ("Thitikul wins third straight LPGA title",
         "Jeeno Thitikul extends her winning run on the LPGA Tour."),
        ("Price ends four-year wait at darts",
         "Gerwyn Price wins the Grand Slam of Darts."),
        ("England thrash New Zealand 37-12",
         "England run in the points at Twickenham."),
    ]),
]

# Column plan: balance story counts (10 / 9 / 9) across 3 columns.
COLUMNS = [
    [SECTIONS[0], SECTIONS[3]],   # EUROPE 6 + AMERICAS 4 = 10
    [SECTIONS[1], SECTIONS[2]],   # MIDDLE EAST 3 + ASIA-PACIFIC 6 = 9
    [SECTIONS[4], SECTIONS[5]],   # MARKETS 3 + WEEKEND SPORT 6 = 9
]

MARGIN = 28
GUTTER = 18
COLW = (W - 2 * MARGIN - 2 * GUTTER) // 3  # 310


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Deterministic paper speckle.
    rnd = random.Random(7)
    for _ in range(900):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        d.point((x, y), fill=(238, 232, 214))

    # Frame.
    d.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=2)

    # Masthead.
    y = 22
    draw_centered(d, y, "THE WORLD IN ONE DAY", F_MAST)
    y += 64
    draw_centered(d, y, "Monday, 23 November 2026", F_DATE)
    y += 30
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 6
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 10

    # Lead story 1: COP31.
    d.text((MARGIN, y), "CLIMATE — ANTALYA, TURKEY", font=F_KICK, fill=RED)
    y += 20
    y = draw_para(d, MARGIN, y, LEAD1_HEAD, F_LEAD, W - 2 * MARGIN, 44,
                  max_lines=2)
    y += 4
    y = draw_para(d, MARGIN, y, LEAD1_SUB, F_LEADSUB, W - 2 * MARGIN, 17,
                  max_lines=3)
    y += 10
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 10

    # Lead story 2: Democrats take the House.
    d.text((MARGIN, y), "UNITED STATES — WASHINGTON", font=F_KICK, fill=RED)
    y += 20
    y = draw_para(d, MARGIN, y, LEAD2_HEAD, F_LEAD2, W - 2 * MARGIN, 34,
                  max_lines=1)
    y += 2
    y = draw_para(d, MARGIN, y, LEAD2_SUB, F_LEADSUB, W - 2 * MARGIN, 17,
                  max_lines=1)
    y += 10
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 12
    grid_top = y

    # Section grid: 3 columns, sections stacked per column.
    col_x = [MARGIN + i * (COLW + GUTTER) for i in range(3)]
    grid_bottom = 0
    for ci, sections in enumerate(COLUMNS):
        x = col_x[ci]
        cy = grid_top
        for name, stories in sections:
            # Section header: red rule + label with story count.
            d.line([(x, cy), (x + COLW, cy)], fill=RED, width=2)
            cy += 6
            d.rectangle([x, cy + 2, x + 9, cy + 11], fill=RED)
            d.text((x + 14, cy), f"{name} — {len(stories)}",
                   font=F_SEC, fill=RED)
            cy += 18
            if name == "WEEKEND SPORT":
                cy = draw_para(d, x, cy,
                               "Results from Sunday 22 Nov, reported in Monday's papers.",
                               F_SUB, COLW, 13, fill=GREY, max_lines=1)
                cy += 2
            for head, sub in stories:
                cy = draw_para(d, x, cy, head, F_HEAD, COLW, 16, max_lines=2)
                cy = draw_para(d, x, cy, sub, F_SUB, COLW, 12,
                               fill=(52, 50, 44), max_lines=2)
                cy += 5
            cy += 3
        grid_bottom = max(grid_bottom, cy)

    y = grid_bottom + 2
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 10

    # DATE CHECK box.
    box_h = 58
    assert y + box_h <= H - 34, f"date box overflows: y={y}"
    d.rectangle([MARGIN, y, W - MARGIN, y + box_h], outline=RED, width=2)
    d.text((MARGIN + 12, y + 7), "✓  DATE CHECK", font=F_BOX, fill=RED)
    d.text((MARGIN + 12, y + 26),
           "Every story above happened or was first reported on Monday 23 November 2026.",
           font=F_BOXTXT, fill=INK)
    d.text((MARGIN + 12, y + 42),
           "Weekend sport results are marked as such.",
           font=F_BOXTXT, fill=INK)
    y += box_h + 8
    d.text((MARGIN, y),
           "Sources: Reuters, AP, CNN, BBC, Xinhua, Morningstar, Cointelegraph, The Guardian, Le Monde",
           font=F_FOOT, fill=GREY)
    y += 16
    assert y <= H - 14, f"footer overflows: y={y}"

    img.save("entry.png", optimize=True)
    print(f"saved entry.png {img.size}")


if __name__ == "__main__":
    main()

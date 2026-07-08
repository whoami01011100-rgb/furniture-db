# drawing_3d.py — 2D front-elevation furniture drawings using Matplotlib
# No extra install needed — matplotlib comes with Python

import matplotlib
matplotlib.use('Agg')            # Non-GUI backend, safe for Flask
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
import io, base64

# ── Color palettes per material ─────────────────────────────────
MATERIAL_COLORS = {
    "Plywood":        {"main": "#DEB887", "dark": "#A0784A", "light": "#F5DEB3", "edge": "#7A5830"},
    "MDF":            {"main": "#D2B48C", "dark": "#B0926E", "light": "#EDD5B0", "edge": "#8B6F50"},
    "Solid Wood":     {"main": "#8B5A2B", "dark": "#5C3317", "light": "#A0744A", "edge": "#3D1C02"},
    "PVC / WPC":      {"main": "#A8C4D0", "dark": "#7A9CAA", "light": "#C8DCE8", "edge": "#5A7A88"},
    "Particle Board": {"main": "#C8B89A", "dark": "#A09070", "light": "#DED0BA", "edge": "#806850"},
    "_default":       {"main": "#DEB887", "dark": "#A0784A", "light": "#F5DEB3", "edge": "#7A5830"},
}

def _colors(material):
    return MATERIAL_COLORS.get(material, MATERIAL_COLORS["_default"])


# ── Canvas setup ────────────────────────────────────────────────
def _setup():
    fig, ax = plt.subplots(figsize=(9, 6), facecolor="#0d0d1a")
    ax.set_facecolor("#0d0d1a")
    ax.tick_params(colors="#888", labelsize=7)
    ax.spines['bottom'].set_color('#2a2a3a')
    ax.spines['top'].set_color('#2a2a3a')
    ax.spines['left'].set_color('#2a2a3a')
    ax.spines['right'].set_color('#2a2a3a')
    ax.grid(True, alpha=0.12, color="#444", linestyle="--")
    return fig, ax

def _finalise(fig, ax, L, H, title):
    margin = max(L, H) * 0.14
    ax.set_xlim(-margin, L + margin)
    ax.set_ylim(-margin * 0.5, H + margin)
    ax.set_xlabel("Width (ft)", color="#aaa", fontsize=8)
    ax.set_ylabel("Height (ft)", color="#aaa", fontsize=8)

    # Dimension arrows/labels
    ax.annotate("", xy=(L, -margin*0.3), xytext=(0, -margin*0.3),
                arrowprops=dict(arrowstyle="<->", color="#FFD700", lw=1.5))
    ax.text(L/2, -margin*0.45, f"{L} ft", color="#FFD700", fontsize=9,
            ha="center", fontweight="bold")

    ax.annotate("", xy=(-margin*0.35, H), xytext=(-margin*0.35, 0),
                arrowprops=dict(arrowstyle="<->", color="#FFD700", lw=1.5))
    ax.text(-margin*0.5, H/2, f"{H} ft", color="#FFD700", fontsize=9,
            va="center", ha="right", fontweight="bold", rotation=90)

    plt.title(title, color="#FFD700", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()

def _to_b64(fig):
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=130, bbox_inches="tight", facecolor="#0d0d1a")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return b64

# ── Drawing helper ───────────────────────────────────────────────
def _rect(ax, x, y, w, h, fc, ec="#333", alpha=0.85, lw=1.0, zorder=2):
    """Draw a filled rectangle."""
    if w <= 0 or h <= 0:
        return
    r = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                  linewidth=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(r)

def _line(ax, x1, y1, x2, y2, color="#888", lw=1.0, zorder=3):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=zorder)

def _dot(ax, x, y, color="#C0C0C0", size=30, zorder=5):
    ax.scatter([x], [y], color=color, s=size, zorder=zorder)


# ══════════════════════════════════════════════════════════════
# SHAPE DRAWING FUNCTIONS  (2D front-elevation view)
# ══════════════════════════════════════════════════════════════

def _draw_bed(ax, L, H, c):
    base_h = max(0.30, H * 0.28)
    mat_h  = max(0.18, H * 0.18)
    hb_h   = H
    hb_w   = max(0.12, L * 0.08)
    fb_w   = max(0.08, L * 0.05)
    fb_h   = H * 0.48

    # Base frame
    _rect(ax, hb_w, 0, L - hb_w - fb_w, base_h, c["dark"], ec=c["edge"])
    # Headboard
    _rect(ax, 0, 0, hb_w, hb_h, c["dark"], ec=c["edge"])
    # Footboard
    _rect(ax, L - fb_w, 0, fb_w, fb_h, c["dark"], ec=c["edge"])
    # Mattress
    _rect(ax, hb_w + 0.03, base_h, L - hb_w - fb_w - 0.06, mat_h, "#ECDDC0", ec="#C8A882")
    # Pillow
    pw = (L - hb_w - fb_w) * 0.28
    _rect(ax, hb_w + 0.08, base_h + mat_h + 0.02, pw, mat_h * 0.5, "#FFFFFF", ec="#DDD", alpha=0.9)
    _rect(ax, hb_w + pw + 0.14, base_h + mat_h + 0.02, pw, mat_h * 0.5, "#FFFFFF", ec="#DDD", alpha=0.9)

def _draw_storage_bed(ax, L, H, c):
    _draw_bed(ax, L, H, c)
    base_h = max(0.30, H * 0.28)
    n = max(2, int(L / 1.5))
    dw = L / n
    for i in range(n):
        x = i * dw + 0.05
        _rect(ax, x, 0.04, dw - 0.10, base_h - 0.08, c["main"], ec=c["edge"], alpha=0.6, lw=0.6)
        _dot(ax, x + dw / 2 - 0.05, base_h / 2, "#D4AF37", 18)

def _draw_bunk_bed(ax, L, H, c):
    mid = H / 2
    post_w = max(0.08, L * 0.04)
    mat_h  = mid * 0.18

    # Posts (left & right)
    _rect(ax, 0, 0, post_w, H, c["dark"], ec=c["edge"])
    _rect(ax, L - post_w, 0, post_w, H, c["dark"], ec=c["edge"])
    # Lower mattress
    _rect(ax, post_w, mid * 0.22, L - 2 * post_w, mat_h, "#ECDDC0", ec="#C8A882")
    # Middle platform
    _rect(ax, 0, mid - 0.04, L, 0.08, c["main"], ec=c["edge"])
    # Upper mattress
    _rect(ax, post_w, mid + 0.12, L - 2 * post_w, mat_h, "#ECDDC0", ec="#C8A882")
    # Guard rail
    _rect(ax, 0, H - 0.20, L * 0.55, 0.08, c["dark"], ec=c["edge"])
    # Ladder (right)
    for rz in np.arange(0.28, H - 0.15, 0.35):
        _rect(ax, L - post_w - 0.22, rz, 0.18, 0.06, c["dark"], ec=c["edge"])

def _draw_wardrobe(ax, L, H, c, n_doors=2, sliding=False):
    # Body
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"], alpha=0.80)
    # Cornice
    _rect(ax, -0.02, H, L + 0.04, H * 0.025, c["dark"], ec=c["edge"])
    # Plinth
    _rect(ax, 0, 0, L, H * 0.025, c["dark"], ec=c["edge"])
    dw = L / n_doors
    if sliding:
        _line(ax, 0, H * 0.97, L, H * 0.97, "#AAA", lw=2)
        _line(ax, 0, H * 0.035, L, H * 0.035, "#AAA", lw=2)
    for i in range(n_doors):
        x0 = i * dw
        _rect(ax, x0 + 0.03, H * 0.027, dw - 0.06, H * 0.93, c["light"], ec=c["dark"], alpha=0.85)
        if i > 0:
            _line(ax, x0, 0, x0, H, c["edge"], lw=1.5)
        hx = x0 + (dw * 0.12 if not sliding else dw * 0.85)
        _dot(ax, hx, H * 0.5, "#C0C0C0", 28)

def _draw_walkin(ax, L, H, c, shape="L"):
    # Show as shelving unit (front view)
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"], alpha=0.78)
    ns = max(3, int(H / 0.4))
    sh = H / ns
    for i in range(1, ns):
        _rect(ax, 0.04, i * sh - 0.025, L - 0.08, 0.05, c["light"], ec=c["edge"])
    # divider in center for L/U shape
    _rect(ax, L / 2 - 0.025, 0, 0.05, H, c["dark"], ec=c["edge"], alpha=0.7)
    ax.text(L * 0.25, H * 0.5, shape, color="#FFD700", fontsize=12,
            ha="center", va="center", fontweight="bold", alpha=0.4)

def _draw_dining_table(ax, L, H, c):
    top = max(0.08, H * 0.07)
    leg_h = H - top
    leg_w = max(0.06, L * 0.04)
    # Tabletop
    _rect(ax, -0.04, leg_h, L + 0.08, top, c["main"], ec=c["edge"])
    # Legs
    _rect(ax, 0.10, 0, leg_w, leg_h, c["dark"], ec=c["edge"])
    _rect(ax, L - leg_w - 0.10, 0, leg_w, leg_h, c["dark"], ec=c["edge"])

def _draw_tv_unit(ax, L, H, c):
    # Body
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"], alpha=0.85)
    # Top highlight strip
    _rect(ax, 0, H - 0.025, L, 0.025, c["light"], ec=c["edge"])
    # Compartment dividers
    n = max(2, int(L / 1.5))
    for i in range(1, n):
        x = i * (L / n)
        _rect(ax, x - 0.02, 0.04, 0.04, H - 0.08, c["dark"], ec=c["edge"], alpha=0.9)
    # Feet
    fh = H * 0.07
    _rect(ax, L * 0.08, -fh, L * 0.18, fh, c["dark"], ec=c["edge"])
    _rect(ax, L * 0.74, -fh, L * 0.18, fh, c["dark"], ec=c["edge"])

def _draw_sofa(ax, L, H, c):
    sh  = H * 0.42
    aw  = L * 0.10
    ah  = H * 0.68
    bd  = H * 0.40
    # Seat
    _rect(ax, aw, 0, L - 2 * aw, sh, c["main"], ec=c["edge"])
    # Backrest
    _rect(ax, aw, sh, L - 2 * aw, bd, c["main"], ec=c["edge"])
    # Armrests
    _rect(ax, 0, 0, aw, ah, c["dark"], ec=c["edge"])
    _rect(ax, L - aw, 0, aw, ah, c["dark"], ec=c["edge"])
    # Seat cushions
    nc = max(2, int((L - 2 * aw) / 0.75))
    cw = (L - 2 * aw) / nc
    for i in range(nc):
        _rect(ax, aw + i * cw + 0.03, sh + 0.02, cw - 0.06, sh * 0.25, c["light"], ec=c["dark"], alpha=0.80)

def _draw_kitchen_base(ax, L, H, c):
    # Carcass
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"])
    # Countertop
    _rect(ax, -0.04, H, L + 0.08, 0.045, "#808080", ec="#555", alpha=0.92)
    # Doors
    n = max(1, int(L / 0.65))
    dw = L / n
    for i in range(n):
        _rect(ax, i * dw + 0.03, 0.03, dw - 0.06, H - 0.06, c["light"], ec=c["dark"], alpha=0.82)
        _dot(ax, i * dw + dw / 2, H * 0.5, "#C0C0C0", 16)

def _draw_kitchen_tall(ax, L, H, c):
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"])
    mid = H * 0.5
    _line(ax, 0, mid, L, mid, c["dark"], lw=1.5)
    _rect(ax, 0.03, mid + 0.03, L - 0.06, H * 0.44, c["light"], ec=c["dark"], alpha=0.82)
    _rect(ax, 0.03, 0.03, L - 0.06, mid - 0.07, c["light"], ec=c["dark"], alpha=0.82)
    _dot(ax, L / 2, H * 0.76, "#C0C0C0", 20)
    _dot(ax, L / 2, H * 0.26, "#C0C0C0", 20)

def _draw_kitchen_wall(ax, L, H, c):
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"])
    n = max(1, int(L / 0.75))
    dw = L / n
    for i in range(n):
        _rect(ax, i * dw + 0.03, 0.03, dw - 0.06, H - 0.06, c["light"], ec=c["dark"], alpha=0.82)
        _dot(ax, i * dw + dw / 2, H / 2, "#C0C0C0", 16)

def _draw_bookshelf(ax, L, H, c):
    t = 0.05
    # Sides
    _rect(ax, 0, 0, t, H, c["main"], ec=c["edge"])
    _rect(ax, L - t, 0, t, H, c["main"], ec=c["edge"])
    # Top & bottom
    _rect(ax, 0, H - t, L, t, c["main"], ec=c["edge"])
    _rect(ax, 0, 0, L, t, c["main"], ec=c["edge"])
    # Shelves
    ns = max(2, int(H / 0.4))
    sh = H / ns
    for i in range(1, ns):
        _rect(ax, t, i * sh - t / 2, L - 2 * t, t, c["main"], ec=c["edge"], alpha=0.88)
    # Books on bottom shelf
    bk_colors = ["#E74C3C", "#3498DB", "#27AE60", "#F39C12", "#9B59B6", "#E67E22", "#1ABC9C"]
    bx = t + 0.04
    for bc in bk_colors:
        bw = np.random.uniform(0.06, 0.11)
        if bx + bw > L - t - 0.04:
            break
        _rect(ax, bx, t, bw, sh * 0.82, bc, ec="#333", alpha=0.92, lw=0.4)
        bx += bw + 0.015

def _draw_study_desk(ax, L, H, c):
    top = max(0.06, H * 0.05)
    leg_h = H - top
    leg_w = 0.07
    # Tabletop
    _rect(ax, 0, leg_h, L, top, c["main"], ec=c["edge"])
    # Legs
    _rect(ax, 0.06, 0, leg_w, leg_h, c["dark"], ec=c["edge"])
    _rect(ax, L - leg_w - 0.06, 0, leg_w, leg_h, c["dark"], ec=c["edge"])
    # Drawer pedestal (right)
    pd = min(L * 0.3, 0.65)
    _rect(ax, L - pd - 0.08, 0, pd, leg_h * 0.72, c["dark"], ec=c["edge"], alpha=0.82)
    nd = 3
    ddh = leg_h * 0.72 / nd
    for i in range(nd):
        _rect(ax, L - pd - 0.06, i * ddh + 0.02, pd - 0.04, ddh - 0.04, c["light"], ec=c["dark"], alpha=0.80)
        _dot(ax, L - pd - 0.06 + pd / 2 - 0.02, i * ddh + ddh / 2, "#C0C0C0", 14)

def _draw_door(ax, L, H, c):
    # Door slab
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"])
    # Panel insets
    pw = L * 0.12
    ph = H * 0.12
    _rect(ax, pw, ph, L - 2 * pw, H * 0.35, c["light"], ec=c["dark"], alpha=0.72, lw=0.5)
    _rect(ax, pw, H * 0.54, L - 2 * pw, H * 0.34, c["light"], ec=c["dark"], alpha=0.72, lw=0.5)
    # Handle
    _dot(ax, L * 0.14, H * 0.5, "#C0C0C0", 40)
    # Hinges
    _dot(ax, L * 0.86, H * 0.18, "#888", 14)
    _dot(ax, L * 0.86, H * 0.82, "#888", 14)

def _draw_chest_drawers(ax, L, H, c):
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"])
    n = max(3, int(H / 0.28))
    dh = H / n
    for i in range(n):
        dz = i * dh
        _rect(ax, 0.03, dz + 0.02, L - 0.06, dh - 0.04, c["light"], ec=c["dark"], alpha=0.88)
        _dot(ax, L / 2, dz + dh / 2, "#C0C0C0", 22)

def _draw_center_table(ax, L, H, c):
    top = max(0.04, H * 0.09)
    leg_h = H - top
    # Tabletop
    _rect(ax, -0.06, leg_h, L + 0.12, top, c["main"], ec=c["edge"])
    if L < 2.0:  # pedestal
        _rect(ax, L / 2 - 0.12, 0, 0.24, leg_h, c["dark"], ec=c["edge"])
    else:
        ls = 0.06
        _rect(ax, 0.12, 0, ls, leg_h, c["dark"], ec=c["edge"])
        _rect(ax, L - ls - 0.12, 0, ls, leg_h, c["dark"], ec=c["edge"])

def _draw_mandir(ax, L, H, c):
    pw = L * 0.07
    # Base platform
    _rect(ax, 0, 0, L, H * 0.08, c["dark"], ec=c["edge"])
    # Main body
    _rect(ax, 0, H * 0.08, L, H * 0.72, c["main"], ec=c["edge"], alpha=0.85)
    # Pillars
    _rect(ax, L * 0.04, H * 0.08, pw, H * 0.72, c["dark"], ec=c["edge"])
    _rect(ax, L * 0.89, H * 0.08, pw, H * 0.72, c["dark"], ec=c["edge"])
    # Inner sanctum
    inn_x = L * 0.04 + pw + 0.02
    inn_w = L - 2 * (L * 0.04 + pw + 0.02)
    _rect(ax, inn_x, H * 0.10, inn_w, H * 0.62, "#1A0A00", ec=c["edge"], alpha=0.95)
    # Arch top
    arch_x = L * 0.25
    _rect(ax, arch_x, H * 0.80, L - 2 * arch_x, H * 0.12, c["dark"], ec=c["edge"])
    # Shikhara
    _rect(ax, L * 0.35, H * 0.92, L * 0.30, H * 0.08, c["dark"], ec=c["edge"])

def _draw_ceiling(ax, L, H, c):
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"], alpha=0.70)
    n = max(2, int(L / 3.0))
    bw = 0.25
    for i in range(n + 1):
        x = i * (L / n)
        _rect(ax, x, 0, bw, H, c["dark"], ec=c["edge"], alpha=0.82)

def _draw_wall_panel(ax, L, H, c):
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"])
    n = max(4, int(L / 0.3))
    fw = L / n
    for i in range(n):
        if i % 2 == 0:
            _rect(ax, i * fw + 0.01, 0, fw - 0.02, H, c["light"], ec=c["dark"], alpha=0.70, lw=0.4)

def _draw_default(ax, L, H, c, label=""):
    _rect(ax, 0, 0, L, H, c["main"], ec=c["edge"])
    if label:
        ax.text(L / 2, H / 2, label[:18], ha="center", va="center",
                color="#FFD700", fontsize=9, fontweight="bold")


# ══════════════════════════════════════════════════════════════
# DISPATCH TABLE  (item name → drawing function key)
# ══════════════════════════════════════════════════════════════
_TYPE_MAP = {
    # Beds
    "double bed":"bed","king bed":"bed","queen bed":"bed","single bed":"bed",
    "loft bed":"bed","canopy bed":"bed","panel bed":"bed","platform bed":"bed",
    "sleigh bed":"bed","upholstered bed":"bed","four poster bed":"bed",
    "adjustable bed":"bed","futon bed":"bed","day bed":"bed","daybed":"bed",
    "antique bed":"bed","victorian bed":"bed","iron bed":"bed","wooden bed":"bed",
    "leather bed":"bed","metal bed":"bed","rustic bed":"bed","hospital bed":"bed",
    "massage bed":"bed","kids bed":"bed","murphy bed":"bed",
    # Storage beds
    "storage bed":"storage_bed","box storage bed":"storage_bed",
    "drawer storage bed":"storage_bed","hydraulic bed":"storage_bed",
    "trundle bed":"storage_bed",
    # Sofa bed
    "sofa bed":"sofa",
    # Bunk
    "bunk bed":"bunk_bed","l-shaped bunk bed":"bunk_bed",
    # Wardrobe hinged
    "2 door wardrobe":"wardrobe_2","3 door wardrobe":"wardrobe_3",
    "4 door wardrobe":"wardrobe_4","5 door wardrobe":"wardrobe_5",
    "hotel wardrobe":"wardrobe_3",
    # Sliding
    "2 panel sliding":"sliding_2","3 panel sliding":"sliding_3","mirror sliding":"sliding_2",
    # Walk-in
    "l shape walk-in":"walkin_l","u shape walk-in":"walkin_u",
    # Dining
    "2 seater dining table":"dining_table","4 seater dining table":"dining_table",
    "6 seater dining table":"dining_table","8 seater dining table":"dining_table",
    "conference table":"dining_table","buffet unit":"tv_unit","sideboard unit":"tv_unit",
    # TV & living
    "floating tv unit":"tv_unit","floor mounted tv unit":"tv_unit",
    "wall mounted tv unit":"tv_unit","hotel tv unit":"tv_unit",
    "crockery unit":"tv_unit","showcase unit":"bookshelf",
    "entertainment unit":"tv_unit","bar cabinet":"wardrobe_2",
    # Tables
    "center table":"center_table","coffee table":"center_table",
    "side table":"center_table","console table":"center_table",
    "bedside table":"center_table","outdoor table":"dining_table",
    "garden bench":"center_table","café table":"dining_table",
    # Sofas
    "sofa frame":"sofa","recliner frame":"sofa",
    # Kitchen
    "bottle pull-out":"kitchen_base","corner unit":"kitchen_base",
    "drawer unit":"kitchen_base","sink unit":"kitchen_base","tandem unit":"kitchen_base",
    "oven unit":"kitchen_tall","pantry unit":"kitchen_tall","refrigerator unit":"kitchen_tall",
    "double door cabinet":"kitchen_wall","glass door cabinet":"kitchen_wall","single door cabinet":"kitchen_wall",
    # Bedroom
    "dressing table":"study_desk","vanity unit":"study_desk",
    "chest of drawers":"chest_drawers",
    # Study/office
    "study table":"study_desk","computer table":"study_desk","executive desk":"study_desk",
    "kids study table":"study_desk","reception desk":"study_desk","workstation":"study_desk",
    "book shelf":"bookshelf","file cabinet":"chest_drawers","toy storage":"chest_drawers",
    # Doors
    "main door":"door","flush door":"door","panel door":"door","veneer door":"door",
    "folding door":"door","sliding door":"door",
    "casement window":"door","french window":"door","sliding window":"door",
    # Mandir
    "floor mandir":"mandir","wall mounted mandir":"mandir",
    "wooden temple designs":"mandir",
    # Ceiling
    "beam ceiling":"ceiling","false ceiling":"ceiling",
    # Wall panels
    "fluted panel":"wall_panel","laminate panel":"wall_panel","veneer panel":"wall_panel",
    "wall cladding":"wall_panel","wooden louvers":"wall_panel","wooden screens":"wall_panel",
    # Shoe / storage
    "open shoe rack":"bookshelf","closed shoe rack":"bookshelf","entry console":"study_desk",
    "linen cabinet":"wardrobe_2","utility cabinet":"wardrobe_2",
    "custom cabinet":"wardrobe_2","custom storage unit":"bookshelf",
    "display rack":"bookshelf","cash counter":"study_desk",
    # Custom / default
    "custom table":"dining_table","home office unit":"wardrobe_2",
    "pergola":"default","gazebo":"default","decking":"default",
}

def _get_type(item_name):
    return _TYPE_MAP.get(item_name.lower().strip(), "default")


# ══════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════
def draw_furniture_3d(item_name: str, L: float, W: float, H: float,
                      material: str = "Plywood") -> str:
    """Return base64 PNG of 2D front-elevation furniture drawing scaled to user dimensions."""
    c     = _colors(material)
    dtype = _get_type(item_name)
    fig, ax = _setup()

    dispatch = {
        "bed":           lambda: _draw_bed(ax, L, H, c),
        "storage_bed":   lambda: _draw_storage_bed(ax, L, H, c),
        "bunk_bed":      lambda: _draw_bunk_bed(ax, L, H, c),
        "wardrobe_2":    lambda: _draw_wardrobe(ax, L, H, c, 2),
        "wardrobe_3":    lambda: _draw_wardrobe(ax, L, H, c, 3),
        "wardrobe_4":    lambda: _draw_wardrobe(ax, L, H, c, 4),
        "wardrobe_5":    lambda: _draw_wardrobe(ax, L, H, c, 5),
        "sliding_2":     lambda: _draw_wardrobe(ax, L, H, c, 2, sliding=True),
        "sliding_3":     lambda: _draw_wardrobe(ax, L, H, c, 3, sliding=True),
        "walkin_l":      lambda: _draw_walkin(ax, L, H, c, "L"),
        "walkin_u":      lambda: _draw_walkin(ax, L, H, c, "U"),
        "dining_table":  lambda: _draw_dining_table(ax, L, H, c),
        "tv_unit":       lambda: _draw_tv_unit(ax, L, H, c),
        "sofa":          lambda: _draw_sofa(ax, L, H, c),
        "kitchen_base":  lambda: _draw_kitchen_base(ax, L, H, c),
        "kitchen_tall":  lambda: _draw_kitchen_tall(ax, L, H, c),
        "kitchen_wall":  lambda: _draw_kitchen_wall(ax, L, H, c),
        "door":          lambda: _draw_door(ax, L, H, c),
        "bookshelf":     lambda: _draw_bookshelf(ax, L, H, c),
        "study_desk":    lambda: _draw_study_desk(ax, L, H, c),
        "center_table":  lambda: _draw_center_table(ax, L, H, c),
        "chest_drawers": lambda: _draw_chest_drawers(ax, L, H, c),
        "mandir":        lambda: _draw_mandir(ax, L, H, c),
        "ceiling":       lambda: _draw_ceiling(ax, L, H, c),
        "wall_panel":    lambda: _draw_wall_panel(ax, L, H, c),
        "default":       lambda: _draw_default(ax, L, H, c, item_name),
    }
    dispatch.get(dtype, dispatch["default"])()

    _finalise(fig, ax, L, H, item_name)
    return _to_b64(fig)

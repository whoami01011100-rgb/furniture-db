# viewer_3d.py — Furniture geometry as box primitives for Three.js (360° coloured viewer)
# No extra Python library needed — just JSON output

# Box format: (x0,y0,z0) = min corner, (x1,y1,z1) = max corner
# Coord system: x=length, y=depth/width, z=height

def _b(x0, y0, z0, x1, y1, z1, color, label=""):
    """Create a box primitive dict."""
    return {
        "x0": round(x0, 4), "y0": round(y0, 4), "z0": round(z0, 4),
        "x1": round(x1, 4), "y1": round(y1, 4), "z1": round(z1, 4),
        "color": color, "label": label
    }

# ── Material colour palettes ─────────────────────────────────────
_PALETTES = {
    "Plywood":        {"main":"#C8A664","dark":"#7A5018","light":"#EAD09A","metal":"#D4AF37","fabric":"#F0E4C8","white":"#FFF8F0","stone":"#888888","gold":"#D4AF37"},
    "MDF":            {"main":"#C4A882","dark":"#7A5C3A","light":"#DECAA8","metal":"#B8B8B8","fabric":"#ECD5B0","white":"#FFF8EE","stone":"#909090","gold":"#C8A030"},
    "Solid Wood":     {"main":"#8B5A2B","dark":"#4A2810","light":"#AA7848","metal":"#D4AF37","fabric":"#D8C0A0","white":"#FFF8F4","stone":"#808080","gold":"#D4AF37"},
    "PVC / WPC":      {"main":"#A8C8D8","dark":"#507888","light":"#C8E4F4","metal":"#C0C0C0","fabric":"#E0F0FF","white":"#FFFFFF","stone":"#909090","gold":"#B8A820"},
    "Particle Board": {"main":"#C0B090","dark":"#806040","light":"#D8C8A8","metal":"#B0B0B0","fabric":"#E8D8B8","white":"#FFF8F0","stone":"#888888","gold":"#C0A820"},
}

def _p(material):
    return _PALETTES.get(material, _PALETTES["Plywood"])


# ══════════════════════════════════════════════════════════════════
# FURNITURE GEOMETRY FUNCTIONS  (return list of box dicts)
# ══════════════════════════════════════════════════════════════════

def _bed(L, W, H, p):
    hb = max(0.15, H*0.11)     # headboard thickness
    fb = max(0.10, H*0.07)     # footboard thickness
    bh = max(0.35, H*0.24)     # base height
    mh = max(0.25, H*0.20)     # mattress height
    pw = (L-hb)*0.28; ph = W*0.38   # pillow size

    bs = [
        _b(0,0,0, L,W,bh,            p["dark"],   "Base Frame"),
        _b(0,0,0, hb,W,H,            p["dark"],   "Headboard"),
        _b(L-fb,0,0, L,W,H*0.44,     p["dark"],   "Footboard"),
        _b(hb,0,0, L-fb,0.07,bh,     p["dark"],   "Rail L"),
        _b(hb,W-0.07,0, L-fb,W,bh,   p["dark"],   "Rail R"),
        _b(hb,W*0.04,bh, L-fb,W*0.96,bh+mh,  p["fabric"], "Mattress"),
        _b(hb+0.1,W*0.06,bh+mh, hb+0.1+pw,W*0.06+ph,bh+mh+mh*0.4, p["white"], "Pillow"),
    ]
    if W > 4:
        bs.append(_b(hb+0.1,W*0.56,bh+mh, hb+0.1+pw,W*0.56+ph,bh+mh+mh*0.4, p["white"], "Pillow"))
    return bs

def _storage_bed(L, W, H, p):
    bs = _bed(L, W, H, p)
    bh = max(0.35, H*0.24)
    n = max(2, int(L/1.5))
    dw = L/n
    for i in range(n):
        x0 = i*dw+0.05; x1 = (i+1)*dw-0.05
        bs.append(_b(x0,0,0.05, x1,0.06,bh-0.06, p["light"], f"Drawer{i+1}"))
        hx = (x0+x1)/2-0.05
        bs.append(_b(hx,0,bh*0.45, hx+0.1,0.022,bh*0.55, p["metal"], "Handle"))
    return bs

def _bunk_bed(L, W, H, p):
    mid = H/2
    post = max(0.09, L*0.025)
    bs = []
    for ox,oy in [(0.04,0.04),(L-post-0.04,0.04),(0.04,W-post-0.04),(L-post-0.04,W-post-0.04)]:
        bs.append(_b(ox,oy,0, ox+post,oy+post,H, p["dark"], "Post"))
    bs += [
        _b(post+0.04,W*0.04,mid*0.22, L-post-0.04,W*0.96,mid*0.22+mid*0.18, p["fabric"],"Lower Mattress"),
        _b(0,0,0, post*1.8,W,mid*0.85,              p["dark"],   "Headboard"),
        _b(0,0,mid-0.04, L,W,mid+0.04,              p["dark"],   "Platform"),
        _b(post+0.04,W*0.04,mid+0.1, L-post-0.04,W*0.96,mid+0.1+mid*0.18, p["fabric"],"Upper Mattress"),
        _b(0,0,H-0.26, L,0.05,H,                    p["dark"],   "Guard Rail"),
    ]
    for rz in [mid+0.3, mid+0.6, H-0.3]:
        bs.append(_b(L-post-0.3,W+0.01,rz-0.03, L-post-0.04,W+0.09,rz+0.03, p["dark"],"Rung"))
    bs.append(_b(L-post-0.3,W+0.01,mid, L-post-0.26,W+0.09,H, p["dark"],"Ladder"))
    bs.append(_b(L-post-0.08,W+0.01,mid, L-post-0.04,W+0.09,H, p["dark"],"Ladder"))
    return bs

def _wardrobe(L, W, H, p, n=2, sliding=False):
    t = 0.04
    dw = L/n
    bs = [
        _b(0,0,0, L,W,H,           p["main"],"Body"),
        _b(t,W-t,0, L-t,W,H,       p["dark"],"Back"),
        _b(0,0,0, t,W,H,           p["dark"],"Side L"),
        _b(L-t,0,0, L,W,H,         p["dark"],"Side R"),
        _b(0,0,0, L,W,t,           p["dark"],"Bottom"),
        _b(0,0,H-t, L,W,H,         p["dark"],"Top"),
        _b(0,0,0, L,W,H*0.026,     p["dark"],"Plinth"),
        _b(-0.015,-0.015,H, L+0.03,W+0.03,H+H*0.024, p["dark"],"Cornice"),
    ]
    for i in range(n):
        x0 = i*dw; x1 = x0+dw
        door_c = p["light"] if not sliding else p["main"]
        bs.append(_b(x0+0.02,0,H*0.028, x1-0.02,W*0.022,H*0.945, door_c,f"Door{i+1}"))
        if i > 0:
            bs.append(_b(x0-0.01,0,0, x0+0.01,W*0.022,H, p["dark"],"Divider"))
        hx = x0+(dw*0.12 if not sliding else dw/2-0.05)
        bs.append(_b(hx,0,H*0.48, hx+0.08,0.022,H*0.52, p["metal"],"Handle"))
    if sliding:
        bs.append(_b(0,0,H*0.97, L,W*0.022,H,   "#A0A0A0","Rail"))
        bs.append(_b(0,0,H*0.028,L,W*0.022,H*0.044,"#A0A0A0","Rail"))
    return bs

def _walkin(L, W, H, p, shape="L"):
    d = min(2.0, W*0.32)
    bs = []
    if shape == "L":
        bs.append(_b(0,0,0, L,d,H, p["main"],"Back Wall"))
        bs.append(_b(0,0,0, d,W,H, p["main"],"Side Wall"))
        for sh in [H*0.2, H*0.42, H*0.62, H*0.82]:
            bs.append(_b(0,0,sh, L,d*0.92,sh+0.04, p["light"],"Shelf"))
            bs.append(_b(0,0,sh, d*0.92,W,sh+0.04, p["light"],"Shelf"))
    else:
        bs.append(_b(0,0,0, L,d,H, p["main"],"Front"))
        bs.append(_b(0,W-d,0, L,W,H, p["main"],"Back"))
        bs.append(_b(0,0,0, d,W,H, p["main"],"Side"))
        for sh in [H*0.2, H*0.42, H*0.62, H*0.82]:
            bs.append(_b(0,0,sh, L,d*0.9,sh+0.04, p["light"],"Shelf"))
    return bs

def _dining_table(L, W, H, p):
    top = max(0.12, H*0.07); lh = H-top; ls = max(0.07,L*0.035)
    bs = [
        _b(-0.05,-0.05,lh, L+0.05,W+0.05,lh+top, p["main"],"Tabletop"),
        _b(ls+0.1,0,lh-0.12, L-ls-0.1,0.05,lh, p["dark"],"Apron"),
        _b(ls+0.1,W-0.05,lh-0.12, L-ls-0.1,W,lh, p["dark"],"Apron"),
    ]
    for ox,oy in [(0.12,0.12),(L-ls-0.12,0.12),(0.12,W-ls-0.12),(L-ls-0.12,W-ls-0.12)]:
        bs.append(_b(ox,oy,0, ox+ls,oy+ls,lh, p["dark"],"Leg"))
    return bs

def _tv_unit(L, W, H, p):
    n = max(2, int(L/1.5))
    bs = [
        _b(0,0,0, L,W,H,           p["main"],"Body"),
        _b(0,0,H, L,W,H+0.025,     p["light"],"Top"),
    ]
    for i in range(1,n):
        x = i*(L/n)
        bs.append(_b(x-0.025,0,0.03, x+0.025,W,H-0.03, p["dark"],"Divider"))
    fh = H*0.07
    bs.append(_b(L*0.08,0,-fh, L*0.26,W,0, p["dark"],"Foot"))
    bs.append(_b(L*0.74,0,-fh, L*0.92,W,0, p["dark"],"Foot"))
    return bs

def _sofa(L, W, H, p):
    sh=H*0.43; bd=W*0.26; aw=L*0.10; ah=H*0.70; lh=0.10; ls=0.07; nc=max(2,int((L-2*aw)/0.75)); cw=(L-2*aw)/nc
    bs = [
        _b(aw,0,lh, L-aw,W-bd,sh,   p["main"],"Seat"),
        _b(aw,W-bd,0, L-aw,W,H,     p["main"],"Backrest"),
        _b(0,0,0, aw,W,ah,           p["dark"],"Armrest L"),
        _b(L-aw,0,0, L,W,ah,         p["dark"],"Armrest R"),
    ]
    for i in range(nc):
        cx = aw+i*cw+0.025
        bs.append(_b(cx,0.025,sh, cx+cw-0.05,W-bd-0.025,sh+sh*0.28, p["light"],f"Cushion{i+1}"))
        bs.append(_b(cx,W-bd+0.025,sh*0.5, cx+cw-0.05,W-0.025,H*0.38, p["light"],f"BackC{i+1}"))
    for ox,oy in [(aw+0.05,0.05),(L-aw-ls-0.05,0.05),(aw+0.05,W-bd-ls-0.05),(L-aw-ls-0.05,W-bd-ls-0.05)]:
        bs.append(_b(ox,oy,0, ox+ls,oy+ls,lh, p["dark"],"Leg"))
    return bs

def _kitchen_base(L, W, H, p):
    n = max(1, int(L/0.65)); dw = L/n
    bs = [
        _b(0,0,0, L,W,H,             p["main"],"Body"),
        _b(-0.04,-0.06,H, L+0.04,W+0.08,H+0.045, p["stone"],"Countertop"),
        _b(0,0,0, L,0.12,0.12,       p["dark"],"Toe Kick"),
    ]
    for i in range(n):
        x0=i*dw+0.025; x1=(i+1)*dw-0.025
        bs.append(_b(x0,0,0.13, x1,0.06,H-0.05, p["light"],f"Door{i+1}"))
        hx=(x0+x1)/2-0.04
        bs.append(_b(hx,0,H*0.5, hx+0.08,0.02,H*0.5+0.12, p["metal"],"Handle"))
    return bs

def _kitchen_tall(L, W, H, p):
    mid = H*0.5
    bs = [
        _b(0,0,0, L,W,H, p["main"],"Body"),
        _b(0.025,0,0.025, L-0.025,0.06,mid-0.04, p["light"],"Lower Door"),
        _b(0.025,0,mid+0.025, L-0.025,0.06,H-0.04, p["light"],"Upper Door"),
        _b(0,0,mid-0.03, L,W,mid+0.03, p["dark"],"Mid Shelf"),
    ]
    for hz in [H*0.25, H*0.75]:
        bs.append(_b(L/2-0.04,0,hz, L/2+0.04,0.02,hz+0.12, p["metal"],"Handle"))
    return bs

def _kitchen_wall(L, W, H, p):
    n = max(1, int(L/0.75)); dw = L/n
    bs = [_b(0,0,0, L,W,H, p["main"],"Wall Cabinet")]
    for i in range(n):
        x0=i*dw+0.025; x1=(i+1)*dw-0.025
        bs.append(_b(x0,0,0.025, x1,0.06,H-0.025, p["light"],f"Door{i+1}"))
        hx=(x0+x1)/2-0.04
        bs.append(_b(hx,0,H/2, hx+0.08,0.02,H/2+0.10, p["metal"],"Handle"))
    return bs

def _bookshelf(L, W, H, p):
    t=0.05; ns=max(2,int(H/0.4)); sh=H/ns
    bs = [
        _b(0,0,0, t,W,H,       p["main"],"Side L"),
        _b(L-t,0,0, L,W,H,     p["main"],"Side R"),
        _b(0,0,0, L,W,t,       p["main"],"Bottom"),
        _b(0,0,H-t, L,W,H,     p["main"],"Top"),
        _b(0,W-t,0, L,W,H,     p["dark"],"Back"),
    ]
    for i in range(1,ns):
        bs.append(_b(t,0,i*sh-t/2, L-t,W-t,i*sh+t/2, p["main"],"Shelf"))
    # colourful books on first shelf
    bcols = ["#E74C3C","#3498DB","#27AE60","#F39C12","#9B59B6","#E67E22","#1ABC9C","#E91E63","#00BCD4","#FF5722"]
    bx = t+0.04
    for j,bc in enumerate(bcols):
        bw = 0.07+(j%3)*0.025
        if bx+bw > L-t-0.04: break
        bs.append(_b(bx,0,t, bx+bw,W*0.7,t+sh*0.82, bc,f"Book{j+1}"))
        bx += bw+0.012
    return bs

def _study_desk(L, W, H, p):
    top=max(0.07,H*0.05); lh=H-top; ls=0.07; pd=min(L*0.3,0.65)
    nd=3; ddh=lh*0.72/nd
    bs = [
        _b(0,0,lh, L,W,lh+top, p["main"],"Tabletop"),
        _b(L-pd-0.08,0.05,0, L-0.08,W*0.65,lh*0.72, p["dark"],"Pedestal"),
    ]
    for ox,oy in [(0.06,0.06),(L-ls-0.06,0.06),(0.06,W-ls-0.06),(L-ls-0.06,W-ls-0.06)]:
        bs.append(_b(ox,oy,0, ox+ls,oy+ls,lh, p["dark"],"Leg"))
    for i in range(nd):
        bs.append(_b(L-pd-0.06,0.05,i*ddh+0.02, L-0.1,W*0.65*0.09,i*ddh+ddh-0.04, p["light"],f"Drawer{i+1}"))
        hx=L-pd/2-0.09
        bs.append(_b(hx,0.05,i*ddh+ddh*0.45, hx+0.08,0.02,i*ddh+ddh*0.55, p["metal"],"Handle"))
    return bs

def _door(L, W, H, p):
    t=max(W,0.09); pw=L*0.12; ph=H*0.12
    return [
        _b(0,0,0, L,t,H, p["main"],"Door"),
        _b(pw,0,H*0.54, L-pw,t*0.05,H-ph, p["light"],"Upper Panel"),
        _b(pw,0,ph, L-pw,t*0.05,H*0.48, p["light"],"Lower Panel"),
        _b(L*0.1,0,H*0.47, L*0.1+0.08,t*0.05,H*0.53, p["metal"],"Handle"),
        _b(L*0.84,0,H*0.14, L*0.92,t*0.05,H*0.22, "#888888","Hinge"),
        _b(L*0.84,0,H*0.78, L*0.92,t*0.05,H*0.86, "#888888","Hinge"),
    ]

def _chest_drawers(L, W, H, p):
    n=max(3,int(H/0.28)); dh=H/n
    bs = [_b(0,0,0, L,W,H, p["main"],"Body")]
    for i in range(n):
        dz=i*dh; hx=L/2-0.04
        bs.append(_b(0.03,0,dz+0.02, L-0.03,0.06,dz+dh-0.02, p["light"],f"Drawer{i+1}"))
        bs.append(_b(hx,0,dz+dh*0.44, hx+0.08,0.022,dz+dh*0.56, p["metal"],"Handle"))
    return bs

def _center_table(L, W, H, p):
    top=max(0.05,H*0.09); lh=H-top; ls=0.06
    bs = [_b(-0.06,-0.06,lh, L+0.06,W+0.06,lh+top, p["main"],"Tabletop")]
    if L < 2.0:
        bs.append(_b(L/2-0.15,W/2-0.15,0, L/2+0.15,W/2+0.15,lh, p["dark"],"Pedestal"))
    else:
        for ox,oy in [(0.12,0.12),(L-ls-0.12,0.12),(0.12,W-ls-0.12),(L-ls-0.12,W-ls-0.12)]:
            bs.append(_b(ox,oy,0, ox+ls,oy+ls,lh, p["dark"],"Leg"))
    return bs

def _mandir(L, W, H, p):
    pw=L*0.07; gold="#D4AF37"; dk="#3D1C02"
    return [
        _b(0,0,0, L,W,H*0.08,   dk,    "Base"),
        _b(0,0,H*0.08, L,W,H*0.8, p["main"],"Body"),
        _b(L*0.04,0,H*0.08, L*0.04+pw,W*0.12,H*0.8, dk,"Left Pillar"),
        _b(L*0.89,0,H*0.08, L*0.89+pw,W*0.12,H*0.8, dk,"Right Pillar"),
        _b(L*0.04+pw+0.02,0,H*0.1, L*0.89-0.02,W*0.06,H*0.7, dk,"Sanctum"),
        _b(L*0.14,0,H*0.12, L*0.86,W*0.05,"#FFA500","Inner Glow"),  # small worship area
        _b(0,0,H*0.78, L,W,H*0.80, gold,"Gold Strip"),
        _b(L*0.25,0,H*0.80, L*0.75,W,H*0.92, dk,"Arch"),
        _b(L*0.35,0,H*0.92, L*0.65,W*0.8,H, gold,"Shikhara"),
    ]

def _ceiling(L, W, H, p):
    n=max(2,int(L/3)); bw=0.25
    bs = [_b(0,0,0, L,W,H, p["light"],"Panel")]
    for i in range(n+1):
        x=i*(L/n)
        bs.append(_b(x,0,0, x+bw,W,H*1.3, p["dark"],"Beam"))
    return bs

def _wall_panel(L, W, H, p):
    t=max(W,0.1); n=max(4,int(L/0.3)); fw=L/n
    bs = [_b(0,0,0, L,t,H, p["main"],"Panel")]
    for i in range(n):
        if i%2==0:
            bs.append(_b(i*fw+0.01,0,0, i*fw+fw-0.01,t*0.07,H, p["light"],"Flute"))
    return bs

def _default(L, W, H, p):
    return [_b(0,0,0, L,W,H, p["main"],"Furniture")]


# ── Dispatch map ──────────────────────────────────────────────────
_MAP = {
    "double bed":"bed","king bed":"bed","queen bed":"bed","single bed":"bed",
    "loft bed":"bed","canopy bed":"bed","panel bed":"bed","platform bed":"bed",
    "sleigh bed":"bed","upholstered bed":"bed","four poster bed":"bed",
    "adjustable bed":"bed","daybed":"bed","day bed":"bed","antique bed":"bed",
    "iron bed":"bed","wooden bed":"bed","leather bed":"bed","metal bed":"bed",
    "rustic bed":"bed","hospital bed":"bed","massage bed":"bed",
    "kids bed":"bed","murphy bed":"bed",
    "storage bed":"sbед","box storage bed":"sbed","drawer storage bed":"sbed","hydraulic bed":"sbed","trundle bed":"sbed",
    "sofa bed":"sofa","sofa frame":"sofa","recliner frame":"sofa",
    "bunk bed":"bunk","l-shaped bunk bed":"bunk",
    "2 door wardrobe":"w2","3 door wardrobe":"w3","4 door wardrobe":"w4","5 door wardrobe":"w5","hotel wardrobe":"w3",
    "2 panel sliding":"s2","3 panel sliding":"s3","mirror sliding":"s2",
    "l shape walk-in":"wl","u shape walk-in":"wu",
    "2 seater dining table":"dt","4 seater dining table":"dt","6 seater dining table":"dt","8 seater dining table":"dt",
    "conference table":"dt","buffet unit":"tv","sideboard unit":"tv",
    "floating tv unit":"tv","floor mounted tv unit":"tv","wall mounted tv unit":"tv","hotel tv unit":"tv",
    "crockery unit":"tv","entertainment unit":"tv","bar cabinet":"w2",
    "showcase unit":"shelf",
    "center table":"ct","coffee table":"ct","side table":"ct","console table":"ct",
    "bedside table":"ct","outdoor table":"dt","garden bench":"ct","café table":"dt",
    "bottle pull-out":"kb","corner unit":"kb","drawer unit":"kb","sink unit":"kb","tandem unit":"kb",
    "oven unit":"kt","pantry unit":"kt","refrigerator unit":"kt",
    "double door cabinet":"kw","glass door cabinet":"kw","single door cabinet":"kw",
    "dressing table":"desk","vanity unit":"desk",
    "study table":"desk","computer table":"desk","executive desk":"desk",
    "kids study table":"desk","reception desk":"desk","workstation":"desk",
    "chest of drawers":"chest",
    "book shelf":"shelf","file cabinet":"chest","toy storage":"chest",
    "open shoe rack":"shelf","closed shoe rack":"shelf","entry console":"desk",
    "linen cabinet":"w2","utility cabinet":"w2","custom cabinet":"w2",
    "custom storage unit":"shelf","display rack":"shelf","cash counter":"desk",
    "custom table":"dt","home office unit":"w2",
    "main door":"door","flush door":"door","panel door":"door","veneer door":"door",
    "folding door":"door","sliding door":"door",
    "casement window":"door","french window":"door","sliding window":"door",
    "floor mandir":"mandir","wall mounted mandir":"mandir","wooden temple designs":"mandir",
    "beam ceiling":"ceil","false ceiling":"ceil",
    "fluted panel":"wp","laminate panel":"wp","veneer panel":"wp",
    "wall cladding":"wp","wooden louvers":"wp","wooden screens":"wp",
}

def _type(name):
    return _MAP.get(name.lower().strip(), "default")


# ── Public API ────────────────────────────────────────────────────
def get_furniture_boxes(item_name: str, L: float, W: float, H: float, material: str = "Plywood"):
    """Return list of box primitives for Three.js rendering."""
    p = _p(material)
    t = _type(item_name)
    fn = {
        "bed":  lambda: _bed(L,W,H,p),
        "sbed": lambda: _storage_bed(L,W,H,p),
        "sbед": lambda: _storage_bed(L,W,H,p),
        "bunk": lambda: _bunk_bed(L,W,H,p),
        "w2":   lambda: _wardrobe(L,W,H,p,2),
        "w3":   lambda: _wardrobe(L,W,H,p,3),
        "w4":   lambda: _wardrobe(L,W,H,p,4),
        "w5":   lambda: _wardrobe(L,W,H,p,5),
        "s2":   lambda: _wardrobe(L,W,H,p,2,True),
        "s3":   lambda: _wardrobe(L,W,H,p,3,True),
        "wl":   lambda: _walkin(L,W,H,p,"L"),
        "wu":   lambda: _walkin(L,W,H,p,"U"),
        "dt":   lambda: _dining_table(L,W,H,p),
        "tv":   lambda: _tv_unit(L,W,H,p),
        "sofa": lambda: _sofa(L,W,H,p),
        "kb":   lambda: _kitchen_base(L,W,H,p),
        "kt":   lambda: _kitchen_tall(L,W,H,p),
        "kw":   lambda: _kitchen_wall(L,W,H,p),
        "door": lambda: _door(L,W,H,p),
        "shelf":lambda: _bookshelf(L,W,H,p),
        "desk": lambda: _study_desk(L,W,H,p),
        "ct":   lambda: _center_table(L,W,H,p),
        "chest":lambda: _chest_drawers(L,W,H,p),
        "mandir":lambda: _mandir(L,W,H,p),
        "ceil": lambda: _ceiling(L,W,H,p),
        "wp":   lambda: _wall_panel(L,W,H,p),
        "default": lambda: _default(L,W,H,p),
    }
    return fn.get(t, fn["default"])()

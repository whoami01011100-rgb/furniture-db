# quotation.py — Price calculation with dummy rates (demo)

# ── Base rates (₹ per sqft of board, approximate) ──────────────
BASE_RATES = {
    # Beds
    "Double Bed": 850, "King Bed": 980, "Queen Bed": 900,
    "Single Bed": 700, "Loft Bed": 780, "Sofa Bed": 1100,
    "Canopy Bed": 1200, "Daybed": 750, "Panel Bed": 820,
    "Platform Bed": 800, "Sleigh Bed": 950, "Upholstered Bed": 900,
    "Four Poster Bed": 1150, "Trundle Bed": 950, "Adjustable Bed": 1050,
    "Antique Bed": 1100, "Iron Bed": 900, "Wooden Bed": 850,
    "Kids Bed": 700, "Hospital Bed": 800, "Massage Bed": 950,
    # Storage Beds
    "Box Storage Bed": 1000, "Drawer Storage Bed": 1050, "Hydraulic Bed": 1200,
    # Bunk
    "Bunk Bed": 950, "L-Shaped Bunk Bed": 1050,
    # Wardrobe
    "2 Door Wardrobe": 900, "3 Door Wardrobe": 950,
    "4 Door Wardrobe": 1000, "5 Door Wardrobe": 1050,
    "2 Panel Sliding": 1050, "3 Panel Sliding": 1100, "Mirror Sliding": 1200,
    "L Shape Walk-In": 1150, "U Shape Walk-In": 1250,
    # Kitchen
    "Bottle Pull-Out": 1400, "Corner Unit": 1200, "Drawer Unit": 1100,
    "Sink Unit": 1000, "Tandem Unit": 1300, "Oven Unit": 1200,
    "Pantry Unit": 1100, "Refrigerator Unit": 1050,
    "Double Door Cabinet": 950, "Glass Door Cabinet": 1100, "Single Door Cabinet": 850,
    # Dining
    "2 Seater Dining Table": 800, "4 Seater Dining Table": 880,
    "6 Seater Dining Table": 950, "8 Seater Dining Table": 1000,
    "Conference Table": 1000, "Buffet Unit": 900, "Sideboard Unit": 900,
    # TV / Living
    "Floating TV Unit": 950, "Floor Mounted TV Unit": 850, "Wall Mounted TV Unit": 1000,
    "Hotel TV Unit": 1050, "Crockery Unit": 900, "Showcase Unit": 950,
    "Center Table": 700, "Coffee Table": 650, "Side Table": 600,
    "Sofa Frame": 1100, "Recliner Frame": 1200,
    # Bedroom
    "Dressing Table": 800, "Vanity Unit": 850,
    "Bedside Table": 550, "Chest of Drawers": 870,
    # Study
    "Study Table": 750, "Computer Table": 800, "Executive Desk": 980,
    "Kids Study Table": 680, "Book Shelf": 780, "File Cabinet": 820,
    "Reception Desk": 1050, "Workstation": 900,
    # Doors & Windows
    "Main Door": 1300, "Flush Door": 900, "Panel Door": 1000,
    "Veneer Door": 1150, "Folding Door": 1000, "Sliding Door": 1050,
    "Casement Window": 1100, "French Window": 1200, "Sliding Window": 1000,
    # Others
    "Floor Mandir": 1200, "Wall Mounted Mandir": 1100,
    "Open Shoe Rack": 600, "Closed Shoe Rack": 650, "Entry Console": 750,
    "Toy Storage": 720, "Garden Bench": 700, "Outdoor Table": 750,
    "Pergola": 900, "Gazebo": 1000,
    "Hotel Wardrobe": 1000, "Cash Counter": 950, "Display Rack": 800,
    "Café Table": 750, "Restaurant Furniture": 900,
    "Custom Cabinet": 950, "Custom Storage Unit": 950, "Custom Table": 850,
    "Murphy Bed": 1150, "Bar Cabinet": 1000, "Entertainment Unit": 950,
    "Home Office Unit": 900, "Beam Ceiling": 700, "False Ceiling": 650,
    "Fluted Panel": 750, "Laminate Panel": 600, "Veneer Panel": 850,
}

# ── Multipliers ─────────────────────────────────────────────────
MATERIAL_MULTIPLIER = {
    "Plywood":       1.00,
    "MDF":           0.88,
    "Solid Wood":    1.45,
    "PVC / WPC":     0.80,
    "Particle Board":0.72,
}

FINISH_MULTIPLIER = {
    "Laminate":    1.00,
    "Veneer":      1.28,
    "PU Paint":    1.18,
    "Duco Paint":  1.22,
    "Acrylic":     1.32,
    "High Gloss":  1.20,
}


def estimate_board_sqft(L, W, H, item_name):
    """Estimate total board area in sqft based on furniture geometry."""
    n = item_name.lower()

    if any(k in n for k in ["wardrobe", "cabinet", "unit", "storage", "kitchen",
                             "shelf", "closet", "rack", "sideboard", "buffet",
                             "showcase", "crockery", "mandir", "console"]):
        # Full box + 2 internal shelves
        return 2*(L*H) + 2*(W*H) + 2*(L*W) + 2*(L*W)

    elif any(k in n for k in ["bed", "sofa", "daybed", "futon"]):
        # Headboard + footboard + rails + base panels
        return 2*(W*H*0.55) + 2*(L*H*0.22) + L*W*0.35

    elif any(k in n for k in ["table", "desk", "workstation", "counter"]):
        # Top + 4 legs + optional modesty panel
        return L*W + 4*(0.08 * H) + (L * H * 0.2)

    elif any(k in n for k in ["door", "window", "panel", "cladding"]):
        # Single face area
        return L * H

    elif any(k in n for k in ["ceiling"]):
        return L * W

    else:
        # Generic: surface area * 0.75 efficiency
        return (2*(L*W) + 2*(L*H) + 2*(W*H)) * 0.75


def calculate_quotation(item_name, L, W, H, material, finish):
    rate = BASE_RATES.get(item_name, 850)
    area = estimate_board_sqft(L, W, H, item_name)

    mat_mult  = MATERIAL_MULTIPLIER.get(material, 1.0)
    fin_mult  = FINISH_MULTIPLIER.get(finish, 1.0)

    # Cost splits
    material_cost = round(area * rate * mat_mult * 0.55)
    labor_cost    = round(area * rate * 0.32)
    finish_cost   = round(area * rate * 0.13 * fin_mult)
    hardware_cost = round(max(800, area * 55))

    subtotal = material_cost + labor_cost + finish_cost + hardware_cost
    gst      = round(subtotal * 0.18)
    total    = subtotal + gst

    return {
        "item_name":     item_name,
        "L": L, "W": W, "H": H,
        "material":      material,
        "finish":        finish,
        "board_area":    round(area, 1),
        "material_cost": material_cost,
        "labor_cost":    labor_cost,
        "finish_cost":   finish_cost,
        "hardware_cost": hardware_cost,
        "subtotal":      subtotal,
        "gst":           gst,
        "total":         total,
    }

# furniture_data.py — Complete furniture catalog

FURNITURE_DATA = {
    "Bed": {
        "Standard Bed": [
            {"id": "double-bed",       "name": "Double Bed",       "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 3.5},
            {"id": "king-bed",         "name": "King Bed",         "emoji": "🛏️", "std_L": 6.5, "std_W": 6.0, "std_H": 3.5},
            {"id": "queen-bed",        "name": "Queen Bed",        "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 3.5},
            {"id": "single-bed",       "name": "Single Bed",       "emoji": "🛏️", "std_L": 6.0, "std_W": 3.0, "std_H": 3.0},
            {"id": "loft-bed",         "name": "Loft Bed",         "emoji": "🛏️", "std_L": 6.0, "std_W": 3.5, "std_H": 5.0},
            {"id": "sofa-bed",         "name": "Sofa Bed",         "emoji": "🛋️", "std_L": 6.0, "std_W": 3.0, "std_H": 2.5},
            {"id": "canopy-bed",       "name": "Canopy Bed",       "emoji": "🛏️", "std_L": 6.5, "std_W": 5.5, "std_H": 7.0},
            {"id": "daybed",           "name": "Daybed",           "emoji": "🛏️", "std_L": 6.0, "std_W": 3.0, "std_H": 2.5},
            {"id": "panel-bed",        "name": "Panel Bed",        "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 4.0},
            {"id": "platform-bed",     "name": "Platform Bed",     "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 2.0},
            {"id": "sleigh-bed",       "name": "Sleigh Bed",       "emoji": "🛏️", "std_L": 6.5, "std_W": 5.0, "std_H": 4.5},
            {"id": "upholstered-bed",  "name": "Upholstered Bed",  "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 4.0},
            {"id": "four-poster-bed",  "name": "Four Poster Bed",  "emoji": "🛏️", "std_L": 6.5, "std_W": 5.5, "std_H": 7.0},
            {"id": "trundle-bed",      "name": "Trundle Bed",      "emoji": "🛏️", "std_L": 6.0, "std_W": 3.0, "std_H": 3.0},
            {"id": "adjustable-bed",   "name": "Adjustable Bed",   "emoji": "🛏️", "std_L": 6.5, "std_W": 5.0, "std_H": 2.5},
            {"id": "antique-bed",      "name": "Antique Bed",      "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 5.0},
            {"id": "iron-bed",         "name": "Iron Bed",         "emoji": "🛏️", "std_L": 6.0, "std_W": 4.0, "std_H": 4.0},
            {"id": "wooden-bed",       "name": "Wooden Bed",       "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 4.0},
            {"id": "hospital-bed",     "name": "Hospital Bed",     "emoji": "🏥", "std_L": 6.5, "std_W": 3.0, "std_H": 2.5},
            {"id": "kids-bed",         "name": "Kids Bed",         "emoji": "🧸", "std_L": 5.5, "std_W": 3.0, "std_H": 3.0},
        ],
        "Storage Bed": [
            {"id": "box-storage-bed",    "name": "Box Storage Bed",    "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 3.5},
            {"id": "drawer-storage-bed", "name": "Drawer Storage Bed", "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 3.5},
            {"id": "hydraulic-bed",      "name": "Hydraulic Bed",      "emoji": "🛏️", "std_L": 6.0, "std_W": 5.0, "std_H": 3.5},
        ],
        "Bunk Bed": [
            {"id": "bunk-bed",         "name": "Bunk Bed",         "emoji": "🛏️", "std_L": 6.0, "std_W": 3.0, "std_H": 6.0},
            {"id": "l-shaped-bunk",    "name": "L-Shaped Bunk Bed","emoji": "🛏️", "std_L": 6.0, "std_W": 3.5, "std_H": 6.5},
        ],
    },

    "Wardrobe": {
        "Hinged Wardrobe": [
            {"id": "wardrobe-2door", "name": "2 Door Wardrobe", "emoji": "🚪", "std_L": 4.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "wardrobe-3door", "name": "3 Door Wardrobe", "emoji": "🚪", "std_L": 6.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "wardrobe-4door", "name": "4 Door Wardrobe", "emoji": "🚪", "std_L": 8.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "wardrobe-5door", "name": "5 Door Wardrobe", "emoji": "🚪", "std_L": 10.0,"std_W": 2.0, "std_H": 7.0},
        ],
        "Sliding Wardrobe": [
            {"id": "sliding-2panel", "name": "2 Panel Sliding", "emoji": "🚪", "std_L": 5.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "sliding-3panel", "name": "3 Panel Sliding", "emoji": "🚪", "std_L": 7.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "mirror-sliding", "name": "Mirror Sliding",  "emoji": "🪞", "std_L": 5.0, "std_W": 2.0, "std_H": 7.0},
        ],
        "Walk-In Wardrobe": [
            {"id": "walkin-l",       "name": "L Shape Walk-In", "emoji": "👔", "std_L": 8.0, "std_W": 6.0, "std_H": 7.5},
            {"id": "walkin-u",       "name": "U Shape Walk-In", "emoji": "👔", "std_L": 8.0, "std_W": 8.0, "std_H": 7.5},
        ],
    },

    "Modular Kitchen": {
        "Base Unit": [
            {"id": "kitchen-bottle",  "name": "Bottle Pull-Out",  "emoji": "🍳", "std_L": 1.5, "std_W": 2.0, "std_H": 2.8},
            {"id": "kitchen-corner",  "name": "Corner Unit",      "emoji": "🍳", "std_L": 3.0, "std_W": 2.0, "std_H": 2.8},
            {"id": "kitchen-drawer",  "name": "Drawer Unit",      "emoji": "🍳", "std_L": 2.0, "std_W": 2.0, "std_H": 2.8},
            {"id": "kitchen-sink",    "name": "Sink Unit",        "emoji": "🚿", "std_L": 2.0, "std_W": 2.0, "std_H": 2.8},
            {"id": "kitchen-tandem",  "name": "Tandem Unit",      "emoji": "🍳", "std_L": 2.5, "std_W": 2.0, "std_H": 2.8},
        ],
        "Tall Unit": [
            {"id": "kitchen-oven",   "name": "Oven Unit",          "emoji": "🔥", "std_L": 2.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "kitchen-pantry", "name": "Pantry Unit",        "emoji": "🍳", "std_L": 2.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "kitchen-fridge", "name": "Refrigerator Unit",  "emoji": "❄️", "std_L": 3.0, "std_W": 2.5, "std_H": 7.0},
        ],
        "Wall Unit": [
            {"id": "kitchen-wall-double", "name": "Double Door Cabinet", "emoji": "🗄️", "std_L": 2.0, "std_W": 1.0, "std_H": 2.0},
            {"id": "kitchen-wall-glass",  "name": "Glass Door Cabinet",  "emoji": "🪟", "std_L": 1.5, "std_W": 1.0, "std_H": 2.0},
            {"id": "kitchen-wall-single", "name": "Single Door Cabinet", "emoji": "🗄️", "std_L": 1.0, "std_W": 1.0, "std_H": 2.0},
        ],
    },

    "Dining Room": {
        "Dining Table": [
            {"id": "dining-2seater", "name": "2 Seater Dining Table", "emoji": "🍽️", "std_L": 3.0, "std_W": 2.5, "std_H": 2.5},
            {"id": "dining-4seater", "name": "4 Seater Dining Table", "emoji": "🍽️", "std_L": 4.0, "std_W": 2.5, "std_H": 2.5},
            {"id": "dining-6seater", "name": "6 Seater Dining Table", "emoji": "🍽️", "std_L": 6.0, "std_W": 3.0, "std_H": 2.5},
            {"id": "dining-8seater", "name": "8 Seater Dining Table", "emoji": "🍽️", "std_L": 8.0, "std_W": 3.5, "std_H": 2.5},
        ],
        "Storage": [
            {"id": "buffet-unit",   "name": "Buffet Unit",   "emoji": "🗄️", "std_L": 5.0, "std_W": 1.5, "std_H": 3.0},
            {"id": "sideboard",     "name": "Sideboard Unit","emoji": "🗄️", "std_L": 5.0, "std_W": 1.5, "std_H": 3.0},
        ],
    },

    "Living Room": {
        "TV Unit": [
            {"id": "tv-floating",   "name": "Floating TV Unit",      "emoji": "📺", "std_L": 6.0, "std_W": 1.5, "std_H": 2.0},
            {"id": "tv-floor",      "name": "Floor Mounted TV Unit", "emoji": "📺", "std_L": 7.0, "std_W": 1.5, "std_H": 2.5},
            {"id": "tv-wall",       "name": "Wall Mounted TV Unit",  "emoji": "📺", "std_L": 6.0, "std_W": 1.0, "std_H": 1.8},
        ],
        "Storage": [
            {"id": "crockery-unit", "name": "Crockery Unit", "emoji": "🍽️", "std_L": 4.0, "std_W": 1.5, "std_H": 6.0},
            {"id": "showcase-unit", "name": "Showcase Unit", "emoji": "✨", "std_L": 4.0, "std_W": 1.5, "std_H": 7.0},
        ],
        "Table": [
            {"id": "center-table",  "name": "Center Table",  "emoji": "☕", "std_L": 4.0, "std_W": 2.0, "std_H": 1.5},
            {"id": "coffee-table",  "name": "Coffee Table",  "emoji": "☕", "std_L": 3.5, "std_W": 2.0, "std_H": 1.5},
            {"id": "side-table",    "name": "Side Table",    "emoji": "🪑", "std_L": 1.5, "std_W": 1.5, "std_H": 2.0},
        ],
        "Seating": [
            {"id": "sofa-frame",    "name": "Sofa Frame",    "emoji": "🛋️", "std_L": 7.0, "std_W": 3.0, "std_H": 3.0},
        ],
    },

    "Bedroom": {
        "Dressing": [
            {"id": "dressing-table","name": "Dressing Table","emoji": "🪞", "std_L": 3.5, "std_W": 1.5, "std_H": 5.0},
            {"id": "vanity-unit",   "name": "Vanity Unit",  "emoji": "🪞", "std_L": 4.0, "std_W": 1.5, "std_H": 6.0},
        ],
        "Storage": [
            {"id": "bedside-table", "name": "Bedside Table",    "emoji": "💡", "std_L": 1.5, "std_W": 1.5, "std_H": 2.0},
            {"id": "chest-drawers", "name": "Chest of Drawers", "emoji": "🗄️", "std_L": 3.0, "std_W": 1.5, "std_H": 4.0},
        ],
    },

    "Study & Office": {
        "Desk": [
            {"id": "study-table",   "name": "Study Table",   "emoji": "📚", "std_L": 4.0, "std_W": 2.0, "std_H": 2.5},
            {"id": "computer-desk", "name": "Computer Table", "emoji": "💻", "std_L": 4.0, "std_W": 2.0, "std_H": 2.5},
            {"id": "exec-desk",     "name": "Executive Desk", "emoji": "💼", "std_L": 5.0, "std_W": 2.5, "std_H": 2.5},
        ],
        "Storage": [
            {"id": "bookshelf",     "name": "Book Shelf",    "emoji": "📚", "std_L": 3.0, "std_W": 1.0, "std_H": 6.0},
            {"id": "file-cabinet",  "name": "File Cabinet",  "emoji": "🗂️", "std_L": 3.0, "std_W": 1.5, "std_H": 4.0},
        ],
        "Conference": [
            {"id": "conf-table",    "name": "Conference Table","emoji": "🤝", "std_L": 10.0,"std_W": 4.0, "std_H": 2.5},
        ],
    },

    "Doors": {
        "Exterior Door": [
            {"id": "main-door",     "name": "Main Door",    "emoji": "🚪", "std_L": 3.5, "std_W": 0.3, "std_H": 7.0},
        ],
        "Interior Door": [
            {"id": "flush-door",    "name": "Flush Door",   "emoji": "🚪", "std_L": 2.5, "std_W": 0.2, "std_H": 7.0},
            {"id": "panel-door",    "name": "Panel Door",   "emoji": "🚪", "std_L": 2.5, "std_W": 0.2, "std_H": 7.0},
            {"id": "veneer-door",   "name": "Veneer Door",  "emoji": "🚪", "std_L": 2.5, "std_W": 0.2, "std_H": 7.0},
        ],
        "Specialty Door": [
            {"id": "folding-door",  "name": "Folding Door", "emoji": "🔄", "std_L": 3.0, "std_W": 0.2, "std_H": 7.0},
            {"id": "sliding-door",  "name": "Sliding Door", "emoji": "🔄", "std_L": 4.0, "std_W": 0.2, "std_H": 7.0},
        ],
    },

    "Windows": {
        "Wooden Window": [
            {"id": "casement-win",  "name": "Casement Window","emoji": "🪟", "std_L": 3.0, "std_W": 0.2, "std_H": 4.0},
            {"id": "french-win",    "name": "French Window",  "emoji": "🪟", "std_L": 4.0, "std_W": 0.2, "std_H": 5.0},
            {"id": "sliding-win",   "name": "Sliding Window", "emoji": "🪟", "std_L": 4.0, "std_W": 0.2, "std_H": 3.5},
        ],
    },

    "Pooja Unit": {
        "Mandir": [
            {"id": "floor-mandir",  "name": "Floor Mandir",        "emoji": "🕉️", "std_L": 3.0, "std_W": 1.5, "std_H": 5.0},
            {"id": "wall-mandir",   "name": "Wall Mounted Mandir", "emoji": "🕉️", "std_L": 2.5, "std_W": 1.0, "std_H": 4.0},
        ],
    },

    "Shoe Storage": {
        "Shoe Rack": [
            {"id": "open-shoe-rack","name": "Open Shoe Rack",  "emoji": "👟", "std_L": 3.0, "std_W": 1.0, "std_H": 3.0},
            {"id": "closed-shoe",   "name": "Closed Shoe Rack","emoji": "👟", "std_L": 3.0, "std_W": 1.0, "std_H": 3.0},
        ],
        "Entry Unit": [
            {"id": "entry-console", "name": "Entry Console",   "emoji": "🚪", "std_L": 4.0, "std_W": 1.2, "std_H": 3.0},
        ],
    },

    "Kids Furniture": {
        "Bed": [
            {"id": "kids-bed-2",    "name": "Kids Bed",        "emoji": "🧸", "std_L": 5.5, "std_W": 3.0, "std_H": 3.0},
        ],
        "Storage": [
            {"id": "toy-storage",   "name": "Toy Storage",     "emoji": "🧩", "std_L": 3.0, "std_W": 1.5, "std_H": 3.5},
        ],
        "Study": [
            {"id": "kids-study",    "name": "Kids Study Table","emoji": "✏️", "std_L": 3.0, "std_W": 1.5, "std_H": 2.5},
        ],
    },

    "Wall Panel": {
        "Decorative Panel": [
            {"id": "fluted-panel",  "name": "Fluted Panel",   "emoji": "🎨", "std_L": 6.0, "std_W": 0.1, "std_H": 9.0},
            {"id": "laminate-panel","name": "Laminate Panel", "emoji": "🎨", "std_L": 6.0, "std_W": 0.1, "std_H": 9.0},
            {"id": "veneer-panel",  "name": "Veneer Panel",   "emoji": "🎨", "std_L": 6.0, "std_W": 0.1, "std_H": 9.0},
        ],
    },

    "Outdoor": {
        "Garden Furniture": [
            {"id": "garden-bench",  "name": "Garden Bench",   "emoji": "🌿", "std_L": 4.0, "std_W": 1.5, "std_H": 3.0},
            {"id": "outdoor-table", "name": "Outdoor Table",  "emoji": "🌳", "std_L": 4.0, "std_W": 3.0, "std_H": 2.5},
        ],
        "Structure": [
            {"id": "pergola",       "name": "Pergola",         "emoji": "🏡", "std_L": 10.0,"std_W": 8.0, "std_H": 8.0},
            {"id": "gazebo",        "name": "Gazebo",          "emoji": "⛺", "std_L": 8.0, "std_W": 8.0, "std_H": 8.0},
        ],
    },

    "Hospitality": {
        "Hotel Furniture": [
            {"id": "hotel-tv-unit", "name": "Hotel TV Unit",  "emoji": "🏨", "std_L": 5.0, "std_W": 1.5, "std_H": 2.5},
            {"id": "hotel-wardrobe","name": "Hotel Wardrobe", "emoji": "🏨", "std_L": 4.0, "std_W": 2.0, "std_H": 7.0},
        ],
    },

    "Commercial": {
        "Office": [
            {"id": "reception-desk","name": "Reception Desk", "emoji": "🏢", "std_L": 6.0, "std_W": 2.5, "std_H": 3.5},
            {"id": "workstation",   "name": "Workstation",    "emoji": "💻", "std_L": 4.0, "std_W": 2.0, "std_H": 2.5},
        ],
        "Retail": [
            {"id": "cash-counter",  "name": "Cash Counter",   "emoji": "💰", "std_L": 5.0, "std_W": 2.0, "std_H": 3.5},
            {"id": "display-rack",  "name": "Display Rack",   "emoji": "🏪", "std_L": 4.0, "std_W": 1.5, "std_H": 6.0},
        ],
        "Restaurant": [
            {"id": "cafe-table",    "name": "Café Table",     "emoji": "☕", "std_L": 3.0, "std_W": 3.0, "std_H": 2.5},
            {"id": "rest-furniture","name": "Restaurant Furniture","emoji":"🍽️","std_L": 6.0, "std_W": 3.0, "std_H": 3.0},
        ],
    },

    "Custom Furniture": {
        "Custom": [
            {"id": "custom-cabinet","name": "Custom Cabinet",      "emoji": "🔨", "std_L": 4.0, "std_W": 2.0, "std_H": 6.0},
            {"id": "custom-storage","name": "Custom Storage Unit", "emoji": "📦", "std_L": 4.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "custom-table",  "name": "Custom Table",       "emoji": "🪵", "std_L": 5.0, "std_W": 3.0, "std_H": 2.5},
            {"id": "murphy-bed",    "name": "Murphy Bed",          "emoji": "🛏️", "std_L": 5.0, "std_W": 1.0, "std_H": 7.0},
            {"id": "bar-cabinet",   "name": "Bar Cabinet",         "emoji": "🍸", "std_L": 4.0, "std_W": 1.5, "std_H": 5.0},
            {"id": "entertainment", "name": "Entertainment Unit",  "emoji": "📺", "std_L": 8.0, "std_W": 2.0, "std_H": 7.0},
            {"id": "home-office",   "name": "Home Office Unit",    "emoji": "🏠", "std_L": 6.0, "std_W": 2.0, "std_H": 7.0},
        ],
    },

    "Ceiling": {
        "Wooden Ceiling": [
            {"id": "beam-ceiling",  "name": "Beam Ceiling",  "emoji": "🏠", "std_L": 10.0,"std_W": 12.0,"std_H": 0.5},
            {"id": "false-ceiling", "name": "False Ceiling", "emoji": "🏠", "std_L": 10.0,"std_W": 12.0,"std_H": 0.3},
        ],
    },
}

# ────────────────────────────────────────────────────────────────
# Flat lookup: item_id → item dict (with category & subcategory)
# ────────────────────────────────────────────────────────────────
ALL_ITEMS = {}
for _cat, _subcats in FURNITURE_DATA.items():
    for _subcat, _items in _subcats.items():
        for _item in _items:
            ALL_ITEMS[_item["id"]] = {**_item, "category": _cat, "subcategory": _subcat}

CATEGORY_EMOJIS = {
    "Bed": "🛏️",
    "Wardrobe": "👔",
    "Modular Kitchen": "🍳",
    "Dining Room": "🍽️",
    "Living Room": "🛋️",
    "Bedroom": "🪞",
    "Study & Office": "📚",
    "Doors": "🚪",
    "Windows": "🪟",
    "Pooja Unit": "🕉️",
    "Shoe Storage": "👟",
    "Kids Furniture": "🧸",
    "Wall Panel": "🎨",
    "Outdoor": "🌿",
    "Hospitality": "🏨",
    "Commercial": "🏢",
    "Custom Furniture": "🔨",
    "Ceiling": "🏠",
}

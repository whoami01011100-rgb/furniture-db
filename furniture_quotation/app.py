# app.py — Flask backend
from flask import Flask, render_template, request, redirect, url_for
from furniture_data import FURNITURE_DATA, ALL_ITEMS, CATEGORY_EMOJIS
from database import init_db, save_quotation, get_all_quotations
from drawing_3d import draw_furniture_3d
from viewer_3d import get_furniture_boxes
from quotation import calculate_quotation, MATERIAL_MULTIPLIER, FINISH_MULTIPLIER
import json

app = Flask(__name__)
app.secret_key = "furniture_demo_secret_2024"

# ── Jinja2 helper: dimension field labels per item type ─────────
def dim_labels(item_name):
    n = item_name.lower()
    if any(k in n for k in ["door", "window", "panel", "cladding"]):
        return ["Width of opening", "Thickness / frame", "Height of opening"]
    if any(k in n for k in ["bed", "sofa bed", "daybed"]):
        return ["Bed length", "Bed width", "Total height incl. headboard"]
    if "sofa" in n:
        return ["Overall length", "Seat depth", "Overall height"]
    if any(k in n for k in ["table", "desk"]):
        return ["Table length", "Table depth", "Height from floor"]
    if "wardrobe" in n or "sliding" in n or "walk-in" in n:
        return ["Total width", "Depth (front to back)", "Floor to ceiling height"]
    if "kitchen" in n:
        return ["Cabinet width", "Cabinet depth", "Cabinet height"]
    if any(k in n for k in ["shelf", "bookshelf", "rack", "display"]):
        return ["Total width", "Shelf depth", "Total height"]
    if "ceiling" in n:
        return ["Room length", "Room width", "Ceiling height / thickness"]
    return ["Length", "Width / Depth", "Height"]

app.jinja_env.globals["dim_labels"] = dim_labels

# Initialise DB on startup
with app.app_context():
    init_db()


# ── Home ────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html",
                           furniture_data=FURNITURE_DATA,
                           emojis=CATEGORY_EMOJIS)


# ── Category → list items ───────────────────────────────────────
@app.route("/category/<path:cat_name>")
def category(cat_name):
    cat_data = FURNITURE_DATA.get(cat_name)
    if not cat_data:
        return redirect(url_for("index"))
    emoji = CATEGORY_EMOJIS.get(cat_name, "🪑")
    return render_template("category.html",
                           category=cat_name,
                           emoji=emoji,
                           subcategories=cat_data)


# ── Configure (size form) ───────────────────────────────────────
@app.route("/configure/<item_id>")
def configure(item_id):
    item = ALL_ITEMS.get(item_id)
    if not item:
        return redirect(url_for("index"))
    return render_template("configure.html",
                           item=item,
                           materials=list(MATERIAL_MULTIPLIER.keys()),
                           finishes=list(FINISH_MULTIPLIER.keys()))


# ── Generate quotation + 3D ─────────────────────────────────────
@app.route("/generate", methods=["POST"])
def generate():
    f = request.form
    item_id   = f.get("item_id", "")
    item_name = f.get("item_name", "Furniture")
    category  = f.get("category", "")
    customer  = f.get("customer_name", "Customer").strip() or "Customer"
    phone     = f.get("phone", "").strip()
    material  = f.get("material", "Plywood")
    finish    = f.get("finish", "Laminate")

    try:
        L = float(f.get("length", 6))
        W = float(f.get("width",  2))
        H = float(f.get("height", 7))
    except ValueError:
        L, W, H = 6.0, 2.0, 7.0

    # Guard against zero/negative
    L = max(0.5, L); W = max(0.3, W); H = max(0.3, H)

    # Calculate price
    quote = calculate_quotation(item_name, L, W, H, material, finish)

    # Generate 2D front-elevation drawing (matplotlib PNG → base64)
    drawing_b64 = draw_furniture_3d(item_name, L, W, H, material)

    # Generate 3D box geometry for Three.js viewer
    boxes = get_furniture_boxes(item_name, L, W, H, material)
    boxes_json = json.dumps(boxes)

    # Persist to SQLite
    qid = save_quotation(customer, phone, item_name, category,
                         L, W, H, material, finish, quote["total"])

    return render_template("result.html",
                           customer=customer,
                           phone=phone,
                           quote=quote,
                           drawing_b64=drawing_b64,
                           boxes_json=boxes_json,
                           quote_id=qid)


# ── History (bonus) ─────────────────────────────────────────────
@app.route("/history")
def history():
    rows = get_all_quotations()
    return render_template("history.html", rows=rows)


if __name__ == "__main__":
    init_db()
    print("\n[OK] Furniture Quotation App running -> http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)

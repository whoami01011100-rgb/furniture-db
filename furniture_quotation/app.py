# ============================================================
# app.py — Flask Backend (Main Server File)
# ============================================================
# Ye file poore web application ka "brain" hai.
# Yahan sab URL routes define hote hain.
#
# Flow:
#   /           → Home page (categories grid)
#   /category/X → Ek category ke items
#   /configure/X→ Ek item ka size/material form
#   /generate   → Form submit → quotation calculate → preview dikhao
#   /confirm    → User confirm kare → MySQL mein save karo
#   /pdf/<id>   → Saved quotation ka PDF download karo
#   /history    → Sabhi saved quotations ki list
#
# Python files ka connection:
#   app.py ─── import ──→ database.py   (MySQL save/fetch)
#   app.py ─── import ──→ quotation.py  (price calculate)
#   app.py ─── import ──→ drawing_3d.py (2D drawing PNG)
#   app.py ─── import ──→ viewer_3d.py  (3D boxes data)
#   app.py ─── import ──→ furniture_data.py (saara furniture data)
#   app.py ─── import ──→ config.py     (MySQL credentials)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, session, flash
from furniture_data import FURNITURE_DATA, ALL_ITEMS, CATEGORY_EMOJIS
from database import init_db, save_quotation, get_all_quotations, get_quotation_by_id, create_user, get_user, get_user_by_id, update_user_profile
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from drawing_3d import draw_furniture_3d
from viewer_3d import get_furniture_boxes
from quotation import calculate_quotation, MATERIAL_MULTIPLIER, FINISH_MULTIPLIER
import json
import io
from datetime import datetime

# ReportLab — PDF banane ke liye
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Flask app initialize ──────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "woodcraft_mysql_secret_2024"

# ── Authentication Decorator ──────────────────────────────────────
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ── Auth Routes ───────────────────────────────────────────────────
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        if not username or not password:
            return render_template("signup.html", error="Please fill all fields")
            
        hashed_password = generate_password_hash(password)
        if create_user(username, hashed_password):
            return redirect(url_for("login"))
        else:
            return render_template("signup.html", error="Username already exists")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        
        user = get_user(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        update_user_profile(session['user_id'], full_name, phone, address)
        # Using simple message since flash might require template changes
        user = get_user_by_id(session['user_id'])
        return render_template("profile.html", user=user, success="Profile updated successfully!")
    
    user = get_user_by_id(session['user_id'])
    return render_template("profile.html", user=user)


# ── Jinja2 helper: dimension field labels per item type ───────────
# Ye function HTML templates mein directly call hoti hai
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


# ── Database initialize on startup ────────────────────────────────
# Ye MySQL mein database + table auto-create karta hai
with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"[WARNING] DB init failed: {e} — Check config.py password!")


# ════════════════════════════════════════════════════════════════
# ROUTE 1: Home Page
# URL: /
# Template: templates/index.html
# ════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    return render_template("index.html",
                           furniture_data=FURNITURE_DATA,
                           emojis=CATEGORY_EMOJIS)


# ════════════════════════════════════════════════════════════════
# ROUTE 2: Category Page
# URL: /category/<category_name>
# Template: templates/category.html
# ════════════════════════════════════════════════════════════════
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


# ════════════════════════════════════════════════════════════════
# ROUTE 3: Configure Page (Size + Material Form)
# URL: /configure/<item_id>
# Template: templates/configure.html
# ════════════════════════════════════════════════════════════════
@app.route("/configure/<item_id>")
def configure(item_id):
    item = ALL_ITEMS.get(item_id)
    if not item:
        return redirect(url_for("index"))
    return render_template("configure.html",
                           item=item,
                           materials=list(MATERIAL_MULTIPLIER.keys()),
                           finishes=list(FINISH_MULTIPLIER.keys()))


# ════════════════════════════════════════════════════════════════
# ROUTE 4: Generate Quotation (PREVIEW ONLY — DB mein save nahi)
# URL: /generate  (POST only)
# Template: templates/result.html
#
# Kya karta hai:
#   - Form data uthata hai
#   - Price calculate karta hai (quotation.py)
#   - 2D drawing banata hai (drawing_3d.py)
#   - 3D boxes data banata hai (viewer_3d.py)
#   - Sab kuch session mein store karta hai (confirm ke liye)
#   - Result page dikhata hai (CONFIRM button ke saath)
# ════════════════════════════════════════════════════════════════
@app.route("/generate", methods=["POST"])
@login_required
def generate():
    f = request.form

    # Form se data uthao
    item_id   = f.get("item_id", "")
    item_name = f.get("item_name", "Furniture")
    category  = f.get("category", "")
    customer  = f.get("customer_name", "Customer").strip() or "Customer"
    phone     = f.get("phone", "").strip()
    material  = f.get("material", "Plywood")
    finish    = f.get("finish", "Laminate")

    # Dimensions parse karo
    try:
        L = float(f.get("length", 6))
        W = float(f.get("width",  2))
        H = float(f.get("height", 7))
    except ValueError:
        L, W, H = 6.0, 2.0, 7.0

    # Negative/zero se protect karo
    L = max(0.5, L); W = max(0.3, W); H = max(0.3, H)

    # Price calculate karo (quotation.py se)
    quote = calculate_quotation(item_name, L, W, H, material, finish)

    # 2D drawing banao (matplotlib → PNG → base64 string)
    drawing_b64 = draw_furniture_3d(item_name, L, W, H, material)

    # 3D boxes data banao (Three.js ke liye)
    boxes = get_furniture_boxes(item_name, L, W, H, material)
    boxes_json = json.dumps(boxes)

    # ─── Session mein store karo (confirm route ke liye) ───
    # Session ek temporary storage hai (browser band hone tak)
    session["pending_quote"] = {
        "customer": customer,
        "phone":    phone,
        "item_name": item_name,
        "category": category,
        "L": L, "W": W, "H": H,
        "material": material,
        "finish":   finish,
        "quote":    quote,
    }

    return render_template("result.html",
                           customer=customer,
                           phone=phone,
                           quote=quote,
                           drawing_b64=drawing_b64,
                           boxes_json=boxes_json,
                           quote_id=None,        # Abhi save nahi hua
                           confirmed=False)      # Confirm button dikhao


# ════════════════════════════════════════════════════════════════
# ROUTE 5: Confirm & Save to MySQL
# URL: /confirm  (POST only)
# Kya karta hai:
#   - Session se pending quote uthata hai
#   - MySQL mein save karta hai (database.py)
#   - Quote ID return karta hai (JSON)
# ════════════════════════════════════════════════════════════════
@app.route("/confirm", methods=["POST"])
@login_required
def confirm():
    pending = session.get("pending_quote")
    if not pending:
        return jsonify({"error": "No pending quotation. Please generate first."}), 400

    try:
        # MySQL mein save karo
        qid = save_quotation(
            user_id   = session['user_id'],
            customer  = pending["customer"],
            phone     = pending["phone"],
            item_name = pending["item_name"],
            category  = pending["category"],
            L         = pending["L"],
            W         = pending["W"],
            H         = pending["H"],
            material  = pending["material"],
            finish    = pending["finish"],
            quote_dict= pending["quote"],
        )
        # Session se clear karo (ek baar hi save ho)
        session.pop("pending_quote", None)

        return jsonify({"success": True, "quote_id": qid})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ════════════════════════════════════════════════════════════════
# ROUTE 6: PDF Download
# URL: /pdf/<quote_id>  (GET)
# Kya karta hai:
#   - MySQL se quotation fetch karta hai
#   - ReportLab se professional PDF banata hai
#   - PDF file download karata hai
# ════════════════════════════════════════════════════════════════
@app.route("/pdf/<int:quote_id>")
@login_required
def download_pdf(quote_id):
    # MySQL se quotation data lao
    row = get_quotation_by_id(quote_id)
    if not row:
        return "Quotation not found", 404

    # Memory mein PDF banao (file disk pe save nahi hogi)
    buffer = io.BytesIO()

    # A4 page setup
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    # ── Styles ────────────────────────────────────────────────
    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=26, textColor=colors.HexColor("#B8860B"),
        spaceAfter=2, fontName="Helvetica-Bold"
    )
    style_sub = ParagraphStyle(
        "Sub", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#555555"),
        spaceAfter=4, fontName="Helvetica"
    )
    style_section = ParagraphStyle(
        "Section", parent=styles["Normal"],
        fontSize=11, textColor=colors.HexColor("#8B6914"),
        spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold"
    )
    style_footer = ParagraphStyle(
        "Footer", parent=styles["Normal"],
        fontSize=8, textColor=colors.grey,
        alignment=TA_CENTER, fontName="Helvetica-Oblique"
    )

    # ── PDF Content build karo ────────────────────────────────
    content = []

    # Header — WoodCraft branding
    content.append(Paragraph("🪵 WoodCraft", style_title))
    content.append(Paragraph("Premium Furniture Quotation System", style_sub))
    content.append(HRFlowable(width="100%", thickness=2,
                               color=colors.HexColor("#D4AF37"),
                               spaceAfter=12))

    # Quotation Info table
    date_str = ""
    if row.get("created_at"):
        dt = row["created_at"]
        if isinstance(dt, str):
            date_str = dt[:16]
        else:
            date_str = dt.strftime("%d %b %Y, %I:%M %p")

    info_data = [
        ["Quotation ID:",  f"# {row['id']}",      "Date:", date_str],
        ["Customer:",      row["customer"],         "Phone:", row.get("phone", "—")],
    ]
    info_table = Table(info_data, colWidths=[3.5*cm, 7*cm, 2.5*cm, 4*cm])
    info_table.setStyle(TableStyle([
        ("FONTNAME",     (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME",     (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",     (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 10),
        ("TEXTCOLOR",    (0,0), (0,-1), colors.HexColor("#8B6914")),
        ("TEXTCOLOR",    (2,0), (2,-1), colors.HexColor("#8B6914")),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("GRID",         (0,0), (-1,-1), 0.3, colors.HexColor("#DDDDDD")),
        ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#FAFAF5")),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.HexColor("#FAFAF5"), colors.white]),
    ]))
    content.append(info_table)
    content.append(Spacer(1, 16))

    # Specifications section
    content.append(Paragraph("📐 Specifications", style_section))
    spec_data = [
        ["Field", "Details"],
        ["Furniture Item", row["item_name"]],
        ["Category", row.get("category", "—")],
        ["Length", f"{row['length']} ft"],
        ["Width / Depth", f"{row['width']} ft"],
        ["Height", f"{row['height']} ft"],
        ["Material", row.get("material", "—")],
        ["Finish", row.get("finish", "—")],
        ["Board Area", f"{row.get('board_area', 0)} sqft"],
    ]
    spec_table = Table(spec_data, colWidths=[5*cm, 12*cm])
    spec_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#D4AF37")),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 10),
        ("FONTNAME",     (0,0), (0,-1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#FAFAF5"), colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ]))
    content.append(spec_table)
    content.append(Spacer(1, 16))

    # Price Breakdown section
    content.append(Paragraph("💰 Price Breakdown", style_section))

    def fmt(val):
        """Number ko Indian format mein dikhao (jaise 1,23,456)"""
        try:
            return f"₹ {int(val):,}"
        except:
            return "₹ 0"

    price_data = [
        ["Cost Component",       "Amount"],
        ["🪵 Material Cost",      fmt(row.get("material_cost", 0))],
        ["👷 Labour & Fitting",   fmt(row.get("labor_cost", 0))],
        ["🎨 Finish & Polish",    fmt(row.get("finish_cost", 0))],
        ["🔧 Hardware",           fmt(row.get("hardware_cost", 0))],
        ["Subtotal",             fmt(row.get("subtotal", 0))],
        ["GST (18%)",            fmt(row.get("gst", 0))],
    ]
    price_table = Table(price_data, colWidths=[12*cm, 5*cm])
    price_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#D4AF37")),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 10),
        ("ALIGN",        (1,0), (1,-1), "RIGHT"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#FAFAF5"), colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        # Subtotal row bold
        ("FONTNAME",     (0,5), (-1,5), "Helvetica-Bold"),
        ("FONTNAME",     (0,6), (-1,6), "Helvetica-Bold"),
        ("TEXTCOLOR",    (0,6), (-1,6), colors.HexColor("#888888")),
    ]))
    content.append(price_table)
    content.append(Spacer(1, 10))

    # TOTAL box (highlight)
    total_data = [["TOTAL ESTIMATE", fmt(row.get("total_price", 0))]]
    total_table = Table(total_data, colWidths=[12*cm, 5*cm])
    total_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",    (0,0), (-1,-1), colors.HexColor("#D4AF37")),
        ("FONTNAME",     (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (0,0), 13),
        ("FONTSIZE",     (1,0), (1,0), 16),
        ("ALIGN",        (1,0), (1,0), "RIGHT"),
        ("BOTTOMPADDING",(0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 12),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), 8),
    ]))
    content.append(total_table)
    content.append(Spacer(1, 20))

    # Footer
    content.append(HRFlowable(width="100%", thickness=1,
                               color=colors.HexColor("#D4AF37"),
                               spaceAfter=8))
    content.append(Paragraph(
        "This is an approximate estimate. Final price may vary based on design complexity and site conditions.<br/>"
        "WoodCraft Furniture | Premium Custom Furniture | Demo System",
        style_footer
    ))

    # ── PDF build karo ────────────────────────────────────────
    doc.build(content)
    buffer.seek(0)

    # Response banao — PDF file as download
    response = make_response(buffer.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f'attachment; filename="WoodCraft_Quote_{quote_id}.pdf"'
    return response


# ════════════════════════════════════════════════════════════════
# ROUTE 7: History Page
# URL: /history
# Template: templates/history.html
# Kya karta hai: MySQL se saari quotations fetch karta hai
# ════════════════════════════════════════════════════════════════
@app.route("/history")
@login_required
def history():
    try:
        rows = get_all_quotations(session['user_id'])
    except Exception as e:
        rows = []
        print(f"[WARNING] Could not fetch history: {e}")
    return render_template("history.html", rows=rows)


# ════════════════════════════════════════════════════════════════
# App start karo
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"[WARNING] DB init failed: {e}")
    print("\n[OK] WoodCraft App running -> http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)

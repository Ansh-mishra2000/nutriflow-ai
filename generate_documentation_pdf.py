import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#059669"))
            self.drawString(54, 11 * 72 - 36, "NutriFlow AI — Architecture, Recommender Science & Engineering Manual")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "v2.0.0 Cloud-Native")
            
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 36, "NutriFlow AI • Clinical AI Nutrition & Delivery Platform • Confidential")
        
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, page_text)
        
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 46, 8.5 * 72 - 54, 46)
        
        self.restoreState()

def build_pdf(filename="NutriFlow_AI_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    C_PRIMARY = colors.HexColor("#059669")     # Emerald 600
    C_SECONDARY = colors.HexColor("#0f172a")   # Slate 900
    C_ACCENT = colors.HexColor("#2563eb")      # Blue 600
    C_DARK = colors.HexColor("#1e293b")        # Slate 800
    C_MUTED = colors.HexColor("#64748b")       # Slate 500
    C_BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50
    C_BORDER = colors.HexColor("#e2e8f0")      # Slate 200

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=C_SECONDARY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=C_SECONDARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_DARK,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_DARK,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0f766e")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_DARK
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=C_SECONDARY
    )

    story = []

    # =========================================================================
    # COVER / HEADER
    # =========================================================================
    story.append(Paragraph("🥗 NutriFlow AI — Comprehensive Engineering & User Manual", title_style))
    story.append(Paragraph("Cloud-Native Precision Health Assessment, AI Nutrition Engine & Calorie-Targeted Food Delivery Platform", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=C_PRIMARY, spaceBefore=0, spaceAfter=12))

    # Meta banner table
    meta_data = [
        [
            Paragraph("<b>Version:</b> 2.0.0 Cloud-Native", table_cell_style),
            Paragraph("<b>Backend:</b> FastAPI / Python 3.10+", table_cell_style),
            Paragraph("<b>Database:</b> SQLite / PostgreSQL", table_cell_style),
            Paragraph("<b>Frontend:</b> Vanilla JS SPA + Leaflet", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[120, 130, 120, 134])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 1: PROJECT OVERVIEW & WHY NUTRIFLOW AI IS UNIQUE
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Why NutriFlow AI is Unique", h1_style))
    story.append(Paragraph(
        "Modern fitness and health management faces a fundamental industry disconnect known as the <b>'Execution Gap'</b>: "
        "traditional calorie tracking applications (such as MyFitnessPal or HealthifyMe) only record nutritional intake <i>after</i> consumption, "
        "while commercial food delivery applications (like Zomato, Swiggy, or UberEats) prioritize consumer cravings without portion control or macro calibration. "
        "Users are left with the tedious cognitive burden of manually computing macros, searching menus, estimating portion sizes, and adjusting ingredients.",
        body_style
    ))
    story.append(Paragraph(
        "<b>NutriFlow AI completely solves this paradigm by uniting clinical diagnostic calculation, automated chef meal planning, and on-demand delivery into an integrated closed-loop platform:</b>",
        body_style
    ))

    story.append(Paragraph("• <b>Precision Clinical Engine:</b> Computes exact physiological parameters (Mifflin-St Jeor BMR, Physical Activity TDEE, Clinical BMI, and goal deficits/surpluses) rather than arbitrary caloric guesses.", bullet_style))
    story.append(Paragraph("• <b>Deterministic Calorie-Targeted Meal Formulation:</b> Automatically distributes daily calories across 4 distinct meal budgets (Breakfast 25%, Lunch 35%, Dinner 30%, Snack 10%) and matches them with chef-curated whole foods.", bullet_style))
    story.append(Paragraph("• <b>Direct Commercial Fulfillment in Indian Rupees (₹ INR):</b> Allows users to order a complete 4-meal daily regimen or single dishes in 1-click with real-time bill calculations (subtotal, 5% GST, ₹0 delivery) and address management.", bullet_style))
    story.append(Paragraph("• <b>Live Interactive GPS & Route Tracking:</b> Features an embedded Leaflet/OpenStreetMap engine that captures real live GPS or 1-click Delhi NCR presets and renders animated rider transit stages.", bullet_style))
    story.append(Paragraph("• <b>Conversational Gemini AI Nutrition Coach:</b> Integrated multi-turn Google Gemini AI for customized recipe substitutions, macro explanations, and lifestyle Q&A.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: RECOMMENDATION ENGINE & MATHEMATICAL FORMULAS
    # =========================================================================
    story.append(Paragraph("2. Recommendation Engine & Mathematical Architecture", h1_style))
    story.append(Paragraph(
        "NutriFlow AI does not rely on random guessing. Every recommendation is derived from validated physiological science through a multi-step deterministic pipeline:",
        body_style
    ))

    math_data = [
        [
            Paragraph("Metric / Stage", table_header_style),
            Paragraph("Governing Formula / Clinical Logic", table_header_style),
            Paragraph("Application in NutriFlow AI", table_header_style)
        ],
        [
            Paragraph("<b>Basal Metabolic Rate (BMR)</b>", table_cell_bold),
            Paragraph("<b>Mifflin-St Jeor Equation:</b><br/>"
                      "• <i>Men:</i> BMR = 10W + 6.25H - 5A + 5<br/>"
                      "• <i>Women:</i> BMR = 10W + 6.25H - 5A - 161<br/>"
                      "(W in kg, H in cm, A in years)", table_cell_style),
            Paragraph("Calculates baseline calories burned at complete metabolic rest with 95% clinical accuracy.", table_cell_style)
        ],
        [
            Paragraph("<b>Total Daily Energy Expenditure (TDEE)</b>", table_cell_bold),
            Paragraph("<b>TDEE = BMR × Activity Multiplier:</b><br/>"
                      "• Sedentary: 1.20 | Light: 1.375<br/>"
                      "• Moderate: 1.55 | Active: 1.725<br/>"
                      "• Very Active: 1.90", table_cell_style),
            Paragraph("Calculates real-world energy expenditure factoring occupational and exercise demands.", table_cell_style)
        ],
        [
            Paragraph("<b>Caloric Target & Goal Offsets</b>", table_cell_bold),
            Paragraph("<b>Target = TDEE + Goal Delta:</b><br/>"
                      "• <i>Weight Loss:</i> -500 kcal/day (~0.5 kg fat loss/week)<br/>"
                      "• <i>Muscle Hypertrophy:</i> +350 kcal/day (lean mass gain)<br/>"
                      "• <i>Maintenance:</i> 0 kcal offset", table_cell_style),
            Paragraph("Prevents starvation responses while driving sustainable body composition results.", table_cell_style)
        ],
        [
            Paragraph("<b>Macronutrient Distribution</b>", table_cell_bold),
            Paragraph("<b>Macro Split Target:</b><br/>"
                      "• <i>Protein:</i> 25% of kcal (4 kcal/g)<br/>"
                      "• <i>Carbohydrates:</i> 50% of kcal (4 kcal/g)<br/>"
                      "• <i>Healthy Fats:</i> 25% of kcal (9 kcal/g)", table_cell_style),
            Paragraph("Calculates daily gram targets for muscle synthesis, sustained glycogen, and hormonal health.", table_cell_style)
        ],
        [
            Paragraph("<b>Meal Calorie Budgets</b>", table_cell_bold),
            Paragraph("<b>Portion Allocation:</b><br/>"
                      "• <i>Breakfast:</i> 25% of daily calories<br/>"
                      "• <i>Lunch:</i> 35% of daily calories<br/>"
                      "• <i>Dinner:</i> 30% of daily calories<br/>"
                      "• <i>Snack:</i> 10% of daily calories", table_cell_style),
            Paragraph("Partitions total daily target into 4 distinct portion budgets for automated dish matching.", table_cell_style)
        ],
        [
            Paragraph("<b>Multi-Offset Dish Rotation</b>", table_cell_bold),
            Paragraph("<b>Permutation Algorithm:</b><br/>"
                      "• <i>Breakfast Idx:</i> variation % N<br/>"
                      "• <i>Lunch Idx:</i> (variation × 2 + 1) % N<br/>"
                      "• <i>Dinner Idx:</i> (variation × 3 + 2) % N<br/>"
                      "• <i>Snack Idx:</i> (variation × 4 + 3) % N", table_cell_style),
            Paragraph("Cycles through 60+ database dishes with non-overlapping step offsets on every 'Regenerate' click.", table_cell_style)
        ]
    ]

    math_table = Table(math_data, colWidths=[110, 210, 184])
    math_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, C_BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(math_table)
    story.append(Spacer(1, 12))

    # =========================================================================
    # SECTION 3: UI BUTTONS & INTERACTIVE CONTROLS GUIDE
    # =========================================================================
    story.append(Paragraph("3. Interactive UI Controls & Button Functionality Guide", h1_style))
    story.append(Paragraph(
        "The NutriFlow AI single-page dashboard provides rich interactive controls designed for zero-friction user workflows. Below is a comprehensive breakdown of all buttons and their underlying technical actions:",
        body_style
    ))

    buttons_data = [
        [
            Paragraph("UI Button / Element", table_header_style),
            Paragraph("Location", table_header_style),
            Paragraph("Functionality & Underlying Technical Action", table_header_style)
        ],
        [
            Paragraph("<b>'Update Metrics'</b>", table_cell_bold),
            Paragraph("Header Navigation", table_cell_style),
            Paragraph("Opens the modal dialog allowing users to modify Age, Gender, Height, Weight, Activity Level, Goal, and Diet. On submit, re-triggers <code>NutritionEngine.evaluate_health()</code> and updates all metrics & meal cards.", table_cell_style)
        ],
        [
            Paragraph("<b>'Regenerate Meals'</b>", table_cell_bold),
            Paragraph("Meal Plan Section Header", table_cell_style),
            Paragraph("Increments <code>currentMealVariation</code>, triggers a rotating spin animation, and queries the backend with the new variation offset. Pulls fresh dishes from the 60+ database catalog and triggers a floating success toast.", table_cell_style)
        ],
        [
            Paragraph("<b>'Order Full Day Plan'</b>", table_cell_bold),
            Paragraph("Meal Plan Section Header", table_cell_style),
            Paragraph("Simultaneously adds <b>all 4 meals</b> (Breakfast, Lunch, Dinner, Snack) into the cart in a single click. Categorizes each item with badges, updates total calories/pricing in ₹ INR, and smoothly slides open the cart drawer.", table_cell_style)
        ],
        [
            Paragraph("<b>'+ Add Meal'</b>", table_cell_bold),
            Paragraph("Each Individual Meal Card", table_cell_style),
            Paragraph("Adds the specific selected meal to the cart, increments the navigation cart counter badge, recalculates totals, and opens the drawer with instant feedback.", table_cell_style)
        ],
        [
            Paragraph("<b>'+' / '–' Qty Buttons</b>", table_cell_bold),
            Paragraph("Delivery Cart Drawer", table_cell_style),
            Paragraph("Dynamically increments or decrements dish quantity. Recalculates item subtotals, overall calorie count, 5% GST, and grand total. Automatically removes item when quantity reaches 0.", table_cell_style)
        ],
        [
            Paragraph("<b>'Clear All'</b>", table_cell_bold),
            Paragraph("Cart Drawer Header", table_cell_style),
            Paragraph("Empties the entire delivery cart in one click, resets badge counters to zero, and displays the empty state placeholder.", table_cell_style)
        ],
        [
            Paragraph("<b>'Place Order & Track Live'</b>", table_cell_bold),
            Paragraph("Cart Drawer Footer", table_cell_style),
            Paragraph("Validates address, creates an order via <code>POST /api/v1/orders/</code>, generates a unique Order ID, opens the Big Live Map modal, and initiates simulated rider GPS dispatch.", table_cell_style)
        ],
        [
            Paragraph("<b>'Live Map Tracking' / Map Window</b>", table_cell_bold),
            Paragraph("Top Nav & Dashboard Card", table_cell_style),
            Paragraph("Opens the full-screen interactive Leaflet map modal with auto-tile rendering, live GPS geolocation button, quick Delhi-NCR address chips, delivery time estimation, and restaurant routing.", table_cell_style)
        ],
        [
            Paragraph("<b>'Ask Coach' (AI Nutritionist)</b>", table_cell_bold),
            Paragraph("AI Coach Floating/Card Widget", table_cell_style),
            Paragraph("Sends multi-turn conversational health queries to the Google Gemini API (<code>gemini-1.5-flash</code> / <code>gemini-2.0-flash</code>) passing the user's current health metrics as system context.", table_cell_style)
        ]
    ]

    buttons_table = Table(buttons_data, colWidths=[120, 110, 274])
    buttons_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, C_BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(buttons_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 4: FOOD CATALOG & CUISINE DIVERSITY
    # =========================================================================
    story.append(Paragraph("4. Nutritious Food Catalog & Dietary Diversity (60+ Meals)", h1_style))
    story.append(Paragraph(
        "The platform includes an extensive, curated database of 60 high-protein, calorie-calibrated meals split evenly across 4 categories and all dietary preferences (Vegetarian, Vegan, Non-Vegetarian, Keto):",
        body_style
    ))

    catalog_summary_data = [
        [
            Paragraph("Meal Category", table_header_style),
            Paragraph("Caloric Budget", table_header_style),
            Paragraph("Sample Chef Dishes (High Protein & INR Pricing)", table_header_style),
            Paragraph("Supported Diets", table_header_style)
        ],
        [
            Paragraph("<b>Breakfast (15)</b>", table_cell_bold),
            Paragraph("320 – 510 kcal", table_cell_style),
            Paragraph("Moong Dal & Paneer Chilla (₹179), Avocado Poached Egg Sourdough (₹249), Oats & Whey (₹189), Steamed Oats Idli (₹169), Masala Omelette (₹199), Smoked Chicken Wrap (₹279), Nutty Banana Oatmeal (₹189).", table_cell_style),
            Paragraph("Veg, Vegan, Non-Veg, Keto", table_cell_style)
        ],
        [
            Paragraph("<b>Lunch (15)</b>", table_cell_bold),
            Paragraph("460 – 620 kcal", table_cell_style),
            Paragraph("Palak Paneer with Multigrain Rotis (₹279), Soya Chunk Curry & Brown Rice (₹229), Amritsari Rajma Quinoa (₹239), Tandoori Chicken Thali (₹349), Salmon Quinoa Bowl (₹449), Lemon Herb Chicken (₹329).", table_cell_style),
            Paragraph("Veg, Vegan, Non-Veg, Keto", table_cell_style)
        ],
        [
            Paragraph("<b>Dinner (15)</b>", table_cell_bold),
            Paragraph("390 – 580 kcal", table_cell_style),
            Paragraph("Yellow Moong Dal Khichdi (₹219), Lentil Dal Makhani (₹239), Paneer Tikka Masala (₹289), Smoked Chicken Tikka (₹329), Mutton Seekh Platter (₹399), Basa Fish & Veggies (₹369), Baingan Bharta (₹219).", table_cell_style),
            Paragraph("Veg, Vegan, Non-Veg, Keto", table_cell_style)
        ],
        [
            Paragraph("<b>Snacks (15)</b>", table_cell_bold),
            Paragraph("140 – 230 kcal", table_cell_style),
            Paragraph("Peri-Peri Roasted Makhana (₹109), Sprouted Moong Chaat (₹129), Masala Boiled Eggs (₹99), Artisanal Energy Bites (₹119), Whey Protein Smoothie (₹179), Greek Yogurt & Pistachios (₹159), Edamame (₹149).", table_cell_style),
            Paragraph("Veg, Vegan, Non-Veg, Keto", table_cell_style)
        ]
    ]

    catalog_table = Table(catalog_summary_data, colWidths=[95, 75, 234, 100])
    catalog_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, C_BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(catalog_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: INSTALLATION & RUN COMMANDS
    # =========================================================================
    story.append(Paragraph("5. Prerequisites & Installation Guide", h1_style))
    story.append(Paragraph(
        "Follow the steps below to run the complete NutriFlow AI platform locally on Linux, macOS, or Windows:",
        body_style
    ))

    story.append(Paragraph("<b>A. System Prerequisites:</b>", h3_style))
    story.append(Paragraph("• <b>Python:</b> Python 3.10, 3.11, or 3.12 installed.<br/>"
                           "• <b>Package Manager:</b> <code>pip</code> or ultra-fast <code>uv</code> installer.<br/>"
                           "• <b>Git:</b> Version control CLI.<br/>"
                           "• <b>Web Browser:</b> Google Chrome, Mozilla Firefox, or Microsoft Edge.<br/>"
                           "• <b>(Optional) Gemini API Key:</b> Set <code>GEMINI_API_KEY</code> environment variable for AI Coach.", body_style))

    story.append(Paragraph("<b>B. Step-by-Step Terminal Commands:</b>", h3_style))

    setup_code = """# 1. Clone or navigate to the project directory
cd /path/to/project

# 2. Create a virtual environment (using standard venv or uv)
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\\Scripts\\activate

# 3. Install backend dependencies
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-multipart python-jose bcrypt httpx jinja2

# 4. (Optional) Set your Gemini API Key for AI Nutrition Coach
export GEMINI_API_KEY="your-google-gemini-api-key"

# 5. Start the FastAPI ASGI server with auto-reload
uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000

# 6. Open your web browser and navigate to:
# Application Dashboard: http://127.0.0.1:8000/
# Interactive Swagger API Docs: http://127.0.0.1:8000/docs"""

    code_table = Table([[Paragraph(setup_code.replace('\n', '<br/>'), code_style)]], colWidths=[504])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: GITHUB PUSH STEP-BY-STEP INSTRUCTIONS
    # =========================================================================
    story.append(Paragraph("6. Step-by-Step GitHub Push Guide", h1_style))
    story.append(Paragraph(
        "To publish your codebase to GitHub, follow these exact terminal commands:",
        body_style
    ))

    git_code = """# Step 1: Open terminal in project root directory
cd /path/to/project

# Step 2: Initialize git repository on 'main' branch
git init -b main

# Step 3: Stage all project files (safe .gitignore prevents large venvs from being added)
git add .

# Step 4: Commit all full-stack project files
git commit -m "feat: NutriFlow AI - Cloud-Native Precision Health, AI Nutrition & Delivery Platform"

# Step 5: Create a new repository on GitHub (e.g. https://github.com/new)
# Then link your local repo to GitHub (replace <YOUR_USERNAME> and <REPO_NAME>)
git remote add origin https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git

# Step 6: Push your code to GitHub
git push -u origin main"""

    git_table = Table([[Paragraph(git_code.replace('\n', '<br/>'), code_style)]], colWidths=[504])
    git_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    # White text for dark terminal box
    git_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38bdf8")),
    ]))
    
    # We create a specific style for dark code
    dark_code_style = ParagraphStyle(
        'DarkCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#38bdf8")
    )
    git_table = Table([[Paragraph(git_code.replace('\n', '<br/>'), dark_code_style)]], colWidths=[504])
    git_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(git_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: CLOUD-NATIVE DEVOPS & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("7. Cloud-Native DevOps & Deployment Architecture", h1_style))
    story.append(Paragraph(
        "NutriFlow AI is enterprise-ready and engineered for containerized multi-cloud deployment:",
        body_style
    ))
    story.append(Paragraph("• <b>Docker Containerization:</b> Multi-stage lightweight Python Dockerfile with non-root security contexts.<br/>"
                           "• <b>Kubernetes (EKS / GKE):</b> Production manifests in <code>/devops/k8s</code> including Deployments, ClusterIP Services, NGINX Ingress, Horizontal Pod Autoscalers (HPA), and ConfigMaps.<br/>"
                           "• <b>Terraform Infrastructure as Code (IaC):</b> Modular AWS infrastructure in <code>/devops/terraform</code> provisioning VPCs, Subnets, Security Groups, and EKS managed node groups.<br/>"
                           "• <b>Ansible Automation:</b> Playbooks in <code>/devops/ansible</code> for server hardening, Docker runtime setup, and automated CI runner provisioning.<br/>"
                           "• <b>GitHub Actions CI/CD:</b> Pipeline in <code>.github/workflows</code> running pytest suites, linting, Docker build/push, and zero-downtime Kubernetes rolling deployment.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Documentation PDF successfully generated: {filename}")

if __name__ == "__main__":
    out_file = "/home/ansh-mishra/Desktop/project/NutriFlow_AI_Documentation.pdf"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    build_pdf(out_file)

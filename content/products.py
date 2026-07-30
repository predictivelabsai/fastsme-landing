"""FastSME's public, open-source Fast* product portfolio."""

GH = "https://github.com/predictivelabsai"

GROUPS = [
    {
        "name": "Work together",
        "description": "An open productivity suite and everyday tools for focused teams.",
        "products": [
            ("FastOffice", "Productivity suite", "One open workspace for documents, spreadsheets, presentations, files, meetings, email, calendars, insights and AI assistance."),
            ("FastCal", "Calendar & scheduling", "Organisation calendars, events, reminders, recurring schedules and conflict-safe public booking pages."),
            ("FastMail", "Email", "Webmail with threaded reading, contacts and AI-assisted drafting."),
            ("FastDrive", "Files", "File and folder management with sharing, permissions and activity history."),
            ("FastDocs", "Documents", "A collaborative block editor with templates, versions and public sharing."),
            ("FastSheets", "Spreadsheets", "A safe formula engine, computed workbooks and AI-assisted analysis."),
            ("FastSlides", "Presentations", "Create, theme and present decks, including prompt-to-deck generation."),
            ("FastMeet", "Meetings", "Scheduling, rooms, participants, agendas and meeting summaries."),
        ],
    },
    {
        "name": "Sell & support",
        "description": "Find customers, manage relationships and keep service moving.",
        "products": [
            ("FastFunnel", "Autonomous marketing", "Plan, create, review, schedule and measure marketing through a bounded AI agency."),
            ("FastCRM", "Sales CRM", "Leads, contacts, activities and a visual deal pipeline."),
            ("FastHelpdesk", "Customer support", "Tickets, teams, knowledge base and live SLA tracking."),
            ("FastESM", "Service management", "A service catalogue, workflows, requests, SLAs and role-based access."),
        ],
    },
    {
        "name": "Run the business",
        "description": "The operational backbone for finance, people and delivery.",
        "products": [
            ("FastERP", "ERP & accounting", "Sales, purchasing, stock, invoicing, receivables and a general ledger."),
            ("FastFPA", "Financial planning & analysis", "Driver-based budgets, rolling forecasts, scenarios, full financial statements and variance analysis."),
            ("FastHRM", "People operations", "Employee records, leave, attendance, payroll and payslips."),
            ("FastPPM", "Projects & portfolios", "Conversational project and transformation-portfolio management."),
            ("FastCMS", "Content management", "Page trees, structured blocks, media, revisions and a headless API."),
        ],
    },
    {
        "name": "Learn & understand",
        "description": "Turn business data and knowledge into decisions.",
        "products": [
            ("FastInsights", "Business intelligence", "SQL, dashboards, Plotly charts and guarded text-to-SQL."),
            ("FastLMS", "Learning management", "Courses, lessons, quizzes, AI tutoring and learner engagement."),
        ],
    },
    {
        "name": "Finance & investment",
        "description": "Specialist workflows for financial and professional firms.",
        "products": [
            ("FastFund", "Family office", "Relationship management, portfolios and multijurisdiction tax intelligence."),
            ("FastVC", "Venture capital", "Startup discovery, founder signals, round and ownership modelling, diligence, IC and portfolio support for venture investment teams."),
            # FastInsure is Streamlit-based; re-enable after its landing/auth migration.
            # ("FastInsure", "Insurance claims", "AI-assisted comparison of claims and invoices against policy contracts."),
        ],
    },
    {
        "name": "Industry operations",
        "description": "Purpose-built platforms for complex, regulated work.",
        "products": [
            ("FastBooking", "Booking & commerce", "Multi-tenant bookings, reservations and inventory for restaurants, hotels, private clinics and ticketed events."),
            ("FastClinic", "Clinic operations", "A multi-specialty operational back office for modern clinics."),
        ],
    },
]

PRODUCTS = [
    {
        "name": name,
        "category": group["name"],
        "label": label,
        "description": description,
        "url": f"{GH}/{name if name != 'FastCMS' else 'FastHTML-CMS'}",
    }
    for group in GROUPS
    for name, label, description in group["products"]
]

for product in PRODUCTS:
    if product["name"] == "FastInsure":
        product["url"] = "https://github.com/kaljuvee/insurance-demo"

LIVE_DEMOS = {
    "FastBooking": "https://booking.fastsme.com",
    "FastOffice": "https://fastoffice.org",
    "FastCal": "https://cal.fastsme.com",
    "FastFunnel": "https://funnel.fastsme.com",
    "FastClinic": "https://clinic.fastsme.com",
    "FastCMS": "https://cms.fastsme.com",
    "FastCRM": "https://crm.fastsme.com",
    "FastDocs": "https://docs.fastsme.com",
    "FastDrive": "https://drive.fastsme.com",
    "FastERP": "https://erp.fastsme.com",
    "FastFPA": "https://fpa.fastsme.com",
    "FastESM": "https://esm.fastsme.com",
    "FastFund": "https://fund.fastsme.com",
    "FastHelpdesk": "https://helpdesk.fastsme.com",
    "FastHRM": "https://hrm.fastsme.com",
    "FastInsights": "https://insights.fastsme.com",
    # FastInsure is intentionally deferred until the Streamlit app is migrated.
    # "FastInsure": "https://insure.fastsme.com",
    "FastLMS": "https://lms.fastsme.com",
    "FastMail": "https://mail.fastsme.com",
    "FastMeet": "https://meet.fastsme.com",
    "FastPPM": "https://ppm.fastsme.com",
    "FastSheets": "https://sheets.fastsme.com",
    "FastSlides": "https://slides.fastsme.com",
}

for product in PRODUCTS:
    product["demo_url"] = LIVE_DEMOS.get(product["name"])

FEATURED = ["FastFunnel", "FastERP", "FastFPA", "FastCRM", "FastInsights", "FastClinic"]

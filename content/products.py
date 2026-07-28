"""FastSME's public, open-source Fast* product portfolio."""

GH = "https://github.com/predictivelabsai"

GROUPS = [
    {
        "name": "Sell & support",
        "description": "Find customers, manage relationships and keep service moving.",
        "products": [
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
            ("FastHRM", "People operations", "Employee records, leave, attendance, payroll and payslips."),
            ("FastPPM", "Projects & portfolios", "Conversational project and transformation-portfolio management."),
            ("FastCMS", "Content management", "Page trees, structured blocks, media, revisions and a headless API."),
        ],
    },
    {
        "name": "Work together",
        "description": "Open everyday tools for focused teams.",
        "products": [
            ("FastMail", "Email", "Webmail with threaded reading, contacts and AI-assisted drafting."),
            ("FastDrive", "Files", "File and folder management with sharing, permissions and activity history."),
            ("FastDocs", "Documents", "A collaborative block editor with templates, versions and public sharing."),
            ("FastSheets", "Spreadsheets", "A safe formula engine, computed workbooks and AI-assisted analysis."),
            ("FastSlides", "Presentations", "Create, theme and present decks, including prompt-to-deck generation."),
            ("FastMeet", "Meetings", "Scheduling, rooms, participants, agendas and meeting summaries."),
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
            ("FastMSR", "Mortgage servicing", "Value, trade and transfer mortgage servicing rights."),
            ("FastInsure", "Insurance claims", "AI-assisted comparison of claims and invoices against policy contracts."),
            ("FastCRE", "Commercial real estate", "An AI deal squad for underwriting, closing and managing CRE assets."),
        ],
    },
    {
        "name": "Industry operations",
        "description": "Purpose-built platforms for complex, regulated work.",
        "products": [
            ("FastClinic", "Clinic operations", "A multi-specialty operational back office for modern clinics."),
            ("FastHealthData", "Health research data", "Research projects, metadata, access governance and cohort analytics."),
            ("FastLCA", "Building carbon", "Whole-building lifecycle carbon assessment aligned with EN 15978."),
            ("FastCity", "Connected operations", "Devices, telemetry, maps, alerts and an open sensor-ingestion API."),
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

FEATURED = ["FastERP", "FastCRM", "FastInsights", "FastDrive", "FastClinic", "FastCRE"]

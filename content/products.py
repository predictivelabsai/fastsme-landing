"""FastSME's public, open-source Fast* product portfolio."""

GH = "https://github.com/predictivelabsai"

GROUPS = [
    {
        "name": "Collaborate & communicate",
        "filter": "collaborate",
        "description": "A connected productivity suite for focused, distributed teams.",
        "products": [
            ("FastOffice", "Productivity suite", "One open workspace for documents, spreadsheets, presentations, files, meetings, email, calendars, insights and AI assistance."),
            ("FastCal", "Calendar & scheduling", "Team availability, event types, public booking links, round-robin scheduling and calendar conflict prevention."),
            ("FastMail", "Email", "Webmail with folders, threaded messages, contacts and AI-assisted summaries and drafting."),
            ("FastDrive", "Files", "File and folder management with sharing, starred and recent views, permissions and activity history."),
            ("FastDocs", "Documents", "A server-rendered block editor with Markdown, folders, templates, versions and public sharing."),
            ("FastSheets", "Spreadsheets", "An editable grid with a real formula engine, multiple sheets and AI-assisted analysis."),
            ("FastSlides", "Presentations", "Create, theme and present decks, including prompt-to-deck generation."),
            ("FastMeet", "Meetings", "Scheduling, rooms, participants, agendas and AI-generated meeting summaries."),
        ],
    },
    {
        "name": "Grow & serve customers",
        "filter": "growth",
        "description": "Find customers, build relationships and keep every service channel moving.",
        "products": [
            ("FastFunnel", "Autonomous marketing", "Plan, create, approve, distribute and measure marketing within explicit publishing and spend guardrails."),
            ("FastCRM", "Sales CRM", "Leads, contacts, organisations, activities and a visual deal pipeline."),
            ("FastHelpdesk", "Customer support", "Ticket queues, conversations, teams, customers, knowledge base and live SLA tracking."),
            ("FastVoice", "Voice automation", "Design and operate self-hosted voice agents with visual workflows, telephony, tools, APIs and MCP."),
            ("FastSocial", "Social media management", "Multi-brand publishing, scheduling, content reuse, performance insights, inboxes, ads and listening."),
            ("FastESM", "Service management", "A cross-department service catalogue with requests, approvals, workflows, RBAC, SLAs and a knowledge base."),
        ],
    },
    {
        "name": "Operate & govern",
        "filter": "operations",
        "description": "The operational backbone for finance, people, delivery, content, data and identity.",
        "products": [
            ("FastERP", "ERP & accounting", "Order-to-cash, procure-to-stock, inventory, accounting and AI-assisted operations."),
            ("FastFPA", "Financial planning & analysis", "Driver-based budgets, rolling forecasts, scenarios, integrated statements and variance analysis."),
            ("FastHRM", "People operations", "Employee records, departments, leave, attendance, payroll and payslips."),
            ("FastPPM", "Projects & portfolios", "Document ingestion, canonical project data, Gantt planning, value tracking, dashboards and an AI analyst."),
            ("FastCMS", "Content management", "Page trees, rich content blocks, media, workflows, revisions, search, forms and a headless API."),
            ("FastDataGov", "Data governance", "A searchable catalogue, glossary, lineage, data quality, stewardship, certification and access requests."),
            ("FastSSO", "Enterprise identity", "An SSO integration broker connecting applications to customer SAML and OIDC identity providers."),
        ],
    },
    {
        "name": "Learn & analyse",
        "filter": "insights",
        "description": "Turn business data and knowledge into better decisions and skills.",
        "products": [
            ("FastBI", "Business intelligence", "Saved queries, Plotly dashboards, SQL and Cypher labs, and conversational text-to-SQL and text-to-Cypher."),
            ("FastLMS", "Learning management", "Courses, quizzes, progress tracking, discussions, AI tutoring, XP, streaks, badges and leaderboards."),
        ],
    },
    {
        "name": "Finance & investment",
        "filter": "finance",
        "description": "Specialist workflows for finance providers, investors and family offices.",
        "products": [
            ("FastFund", "Family office", "Relationship management, portfolios, legal entities, filings and multijurisdiction tax intelligence."),
            ("FastVC", "Venture capital", "Thesis-led sourcing, founder signals, screening, round modelling, diligence, IC, LPs and portfolios."),
            ("FastPE", "Private equity", "Agentic workflows for deal sourcing, LBO underwriting, diligence, investment committee, LPs and portfolio operations."),
            ("FastFactoring", "Invoice finance", "Supplier onboarding, invoice verification, funding, servicing, collections, settlement and auto-invest rules."),
        ],
    },
    {
        "name": "Booking & care",
        "filter": "booking-care",
        "description": "Purpose-built booking, commerce and care operations for service businesses.",
        "products": [
            ("FastBooking", "Booking & commerce", "Multi-tenant bookings and commerce for sports facilities, restaurants, hotels, clinics and events."),
            ("FastClinic", "Clinic operations", "Multi-specialty clinic operations for appointments, availability, invoicing, recall, case mix and revenue."),
        ],
    },
]

PRODUCTS = [
    {
        "name": name,
        "category": group["name"],
        "category_id": group["filter"],
        "label": label,
        "description": description,
        "url": f"{GH}/{name}",
    }
    for group in GROUPS
    for name, label, description in group["products"]
]

LIVE_DEMOS = {
    "FastFunnel": "https://funnel.fastsme.com",
    "FastClinic": "https://clinic.fastsme.com",
    "FastCMS": "https://cms.fastsme.com",
    "FastCRM": "https://crm.fastsme.com",
    "FastDocs": "https://docs.fastsme.com",
    "FastDrive": "https://drive.fastsme.com",
    "FastERP": "https://erp.fastsme.com",
    "FastESM": "https://esm.fastsme.com",
    "FastFund": "https://fund.fastsme.com",
    "FastHelpdesk": "https://helpdesk.fastsme.com",
    "FastHRM": "https://hrm.fastsme.com",
    "FastBI": "https://bi.fastsme.com",
    "FastLMS": "https://lms.fastsme.com",
    "FastMail": "https://mail.fastsme.com",
    "FastMeet": "https://meet.fastsme.com",
    "FastPPM": "https://ppm.fastsme.com",
    "FastSheets": "https://sheets.fastsme.com",
    "FastSlides": "https://slides.fastsme.com",
    "FastOffice": "https://office.fastsme.com",
    "FastFPA": "https://fpa.fastsme.com",
    "FastBooking": "https://booking.fastsme.com",
    "FastVC": "https://vc.fastsme.com",
    "FastPE": "https://pe.fastsme.com",
    "FastCal": "https://cal.fastsme.com",
    "FastSSO": "https://sso.fastsme.com",
    "FastVoice": "https://voice.fastsme.com",
    "FastDataGov": "https://datagov.fastsme.com",
    "FastSocial": "https://fastsocial.org",
    "FastFactoring": "https://fastfactoring.org",
}

for product in PRODUCTS:
    product["demo_url"] = LIVE_DEMOS[product["name"]]

FEATURED = ["FastFunnel", "FastERP", "FastFPA", "FastCRM", "FastBI", "FastClinic"]

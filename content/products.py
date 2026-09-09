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
            ("FastWiki", "Knowledge workspace", "A Confluence-style wiki with rich editing, search, history, comments, attachments and FastOffice suite links."),
        ],
    },
    {
        "name": "Grow & serve customers",
        "filter": "growth",
        "description": "Find customers, build relationships and keep every service channel moving.",
        "products": [
            ("FastFunnel", "Autonomous marketing", "Plan, create, approve, distribute and measure marketing within explicit publishing and spend guardrails."),
            ("FastGTM", "Go-to-market", "Plan campaigns, messaging and launch workflows so product, marketing and sales stay aligned."),
            ("FastCRM", "Sales CRM", "Leads, contacts, organisations, activities and a visual deal pipeline."),
            ("FastATS", "Applicant tracking", "Recruiter-first hiring with AI screening that scores and explains — humans keep every state change."),
            ("FastHelpdesk", "Customer support", "Ticket queues, conversations, teams, customers, knowledge base and live SLA tracking."),
            ("FastVoice", "Voice automation", "Design and operate self-hosted voice agents with visual workflows, telephony, tools, APIs and MCP."),
            ("FastSocial", "Social media management", "Multi-brand publishing, scheduling, content reuse, performance insights, inboxes, ads and listening."),
            ("FastBot", "AI coworkers", "Governed AI coworkers with durable channels, visible activity, policy boundaries and a full audit trail."),
            ("FastSurvey", "Conversational research", "Chat-first survey design, adaptive interviews, structured extraction and evidence-backed synthesis."),
            ("FastCDP", "Customer data platform", "Unify customer profiles, events and audiences so growth and service teams share one governed view."),
            ("FastESM", "Service management", "A cross-department service catalogue with requests, approvals, workflows, RBAC, SLAs and a knowledge base."),
        ],
    },
    {
        "name": "Operate & govern",
        "filter": "operations",
        "description": "The operational backbone for finance, people, delivery, content, data and identity.",
        "products": [
            ("FastERP", "ERP & accounting", "Order-to-cash, procure-to-stock, inventory, accounting and AI-assisted operations."),
            ("FastAccounts", "Bookkeeping", "UK and Estonian bookkeeping for invoices, bills, payments, double-entry ledgers and VAT/KMD workpapers — deliberately not an ERP."),
            ("FastDPS", "Dynamic procurement", "Create dynamic purchasing systems, continuously qualify suppliers, run call-off competitions and keep every decision auditable."),
            ("FastCLM", "Contract lifecycle management", "Upload, review, approve, sign and manage contract versions, obligations, renewals and notice dates."),
            ("FastLegal", "Legal analysis", "AI-powered legal document analysis for review, extraction and grounded answers over your matter files."),
            ("FastFPA", "Financial planning & analysis", "Driver-based budgets, rolling forecasts, scenarios, integrated statements and variance analysis."),
            ("FastHRM", "People operations", "Employee records, departments, leave, attendance, payroll and payslips."),
            ("FastPPM", "Projects & portfolios", "Document ingestion, canonical project data, Gantt planning, value tracking, dashboards and an AI analyst."),
            ("FastCMS", "Content management", "Page trees, rich content blocks, media, workflows, revisions, search, forms and a headless API."),
            ("FastDataGov", "Data governance", "A searchable catalogue, glossary, lineage, data quality, stewardship, certification and access requests."),
            ("FastSSO", "Enterprise identity", "An SSO integration broker connecting applications to customer SAML and OIDC identity providers."),
            ("FastDevOps", "Deployment orchestration", "Provision, configure and deploy the Fast* fleet with Coolify-first operations and an optional Cloud Run path."),
            ("FastLCA", "Building carbon assessment", "Whole-building life-cycle carbon assessment per EN 15978 as an inspectable FastHTML alternative to closed spreadsheets."),
        ],
    },
    {
        "name": "Learn & analyse",
        "filter": "insights",
        "description": "Turn business data and knowledge into better decisions and skills.",
        "products": [
            ("FastBI", "Business intelligence", "Saved queries, Plotly dashboards, SQL and Cypher labs, and conversational text-to-SQL and text-to-Cypher."),
            ("FastComps", "Competitive intelligence", "Track competitors, offerings, published prices and collection coverage across EEA markets with every claim linked to retained source evidence."),
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
            ("FastCRE", "Commercial real estate", "CRE deal workflows for underwriting, closing and managing investments with an AI deal squad."),
            ("FastFactoring", "Invoice finance", "Supplier onboarding, invoice verification, funding, servicing, collections, settlement and auto-invest rules."),
            ("FastMSR", "Mortgage servicing rights", "MSR management with a simulated Freddie Mac Cash-Released XChange for servicing and transfer workflows."),
            ("FastGrants", "Grants & EU funds", "Calls, applications, awards, disbursements, beneficiary reporting and an AI assistant across the grant lifecycle."),
        ],
    },
    {
        "name": "Booking & care",
        "filter": "booking-care",
        "description": "Purpose-built booking, commerce and care operations for service businesses.",
        "products": [
            ("FastBooking", "Booking & commerce", "Multi-tenant bookings and commerce for sports facilities, restaurants, hotels, clinics and events."),
            ("FastClinic", "Clinic operations", "Multi-specialty clinic operations for appointments, availability, invoicing, recall, case mix and revenue."),
            ("FastHealthData", "Health research data", "Research-data platform with project lifecycle, OMOP/FHIR cataloguing, access governance, pseudonymisation and cohort analytics."),
        ],
    },
    {
        "name": "Cities & infrastructure",
        "filter": "cities",
        "description": "Open platforms for civic IoT, telemetry and place-based operations.",
        "products": [
            ("FastCity", "Smart city IoT", "Device registry, telemetry, geo-dashboards, alarms, ingestion APIs and an AI assistant for city operations."),
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
    "FastComps": "https://comps.fastsme.com",
    "FastCMS": "https://cms.fastsme.com",
    "FastCRM": "https://crm.fastsme.com",
    "FastDocs": "https://docs.fastsme.com",
    "FastDrive": "https://drive.fastsme.com",
    "FastERP": "https://erp.fastsme.com",
    "FastDPS": "https://dps.fastsme.com",
    "FastCLM": "https://clm.fastsme.com",
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
    "FastSurvey": "https://fastsurvey.org",
}

for product in PRODUCTS:
    demo_url = LIVE_DEMOS.get(product["name"])
    if demo_url:
        product["demo_url"] = demo_url

FEATURED = ["FastFunnel", "FastERP", "FastFPA", "FastCRM", "FastBI", "FastClinic"]

assert len(PRODUCTS) == 47, len(PRODUCTS)

REPOS = [
    {
        "name": "open-od-toolkit",
        "url": "https://github.com/predictivelabsai/open-od-toolkit",
        "tagline": "Origin-destination matrix synthesis from UK open data — an alternative to commercial GPS licences.",
        "tags": ["Public mobility", "Open data", "Python"],
        "relevance": "HIGH",
    },
    {
        "name": "data-quality-toolkit",
        "url": "https://github.com/predictivelabsai/data-quality-toolkit",
        "tagline": "Transparent profiling, rule-based validation and AI-assisted anomaly detection — open alternative to closed enterprise DQM suites.",
        "tags": ["Data governance", "Open source", "Python"],
        "relevance": "HIGH",
    },
    {
        "name": "traffic-data-analysis",
        "url": "https://github.com/predictivelabsai/traffic-data-analysis",
        "tagline": "Reference implementation for county-scale traffic analytics with open data.",
        "tags": ["Public mobility", "Geospatial", "Python"],
        "relevance": "HIGH",
    },
    {
        "name": "legalai",
        "url": "https://github.com/predictivelabsai/legalai",
        "tagline": "Document intelligence patterns for legal and regulatory workflows.",
        "tags": ["Document AI", "Legal tech", "Python"],
        "relevance": "HIGH",
    },
    {
        "name": "FastLMS",
        "url": "https://github.com/predictivelabsai/FastLMS",
        "tagline": "Open-source learning management system built with FastHTML — AI tutor, XP system, streaks, badges and leaderboards, no JS framework.",
        "tags": ["FastHTML", "Education", "HTMX"],
        "relevance": "HIGH",
    },
    {
        "name": "FastHRM",
        "url": "https://github.com/predictivelabsai/FastHRM",
        "tagline": "FastHTML HR system — employee directory, leave, attendance and payroll, with a grounded AI assistant. Consolidates the earlier openhr public-sector reference.",
        "tags": ["FastHTML", "HR", "HTMX"],
        "relevance": "HIGH",
    },
    {
        "name": "FastClinic",
        "url": "https://github.com/predictivelabsai/FastClinic",
        "tagline": "Open-source GP / general-practice marketing & activation cockpit built with FastHTML — patient activation engines, SMS & email broadcasters, an LLM SEO audit suite and an AI assistant, all on synthetic data.",
        "tags": ["FastHTML", "Healthcare", "Activation"],
        "relevance": "HIGH",
    },
    {
        "name": "teleradiology-toolkit",
        "url": "https://github.com/predictivelabsai/teleradiology-toolkit",
        "tagline": "Open building blocks for teleradiology workflows — E027-va form handling, DICOM/PACS integration, FHIR support and XAdES signing.",
        "tags": ["Healthcare", "DICOM", "FHIR"],
        "relevance": "HIGH",
    },
    {
        "name": "rwd-synth-toolkit",
        "url": "https://github.com/predictivelabsai/rwd-synth-toolkit",
        "tagline": "Synthetic real-world-data cohort generator plus reproducible Kaplan-Meier, hazard-ratio and IPTW helpers for public-sector RWE studies.",
        "tags": ["Healthcare", "RWE", "Python"],
        "relevance": "HIGH",
    },
    {
        "name": "openharvey",
        "url": "https://github.com/predictivelabsai/openharvey",
        "tagline": "AI-powered legal document analysis and contract review platform built with FastHTML and LangChain, supporting multiple LLMs.",
        "tags": ["Document AI", "FastHTML", "LangChain"],
        "relevance": "HIGH",
    },
    {
        "name": "bricksmith",
        "url": "https://github.com/predictivelabsai/bricksmith",
        "tagline": "AI-powered commercial real estate deal squad — underwriting, closing and managing CRE deals.",
        "tags": ["Real estate", "FastHTML", "Python"],
        "relevance": "HIGH",
    },
    {
        "name": "kanvas",
        "url": "https://github.com/predictivelabsai/kanvas",
        "tagline": "AI art advisory, research and education platform — collection management, valuation and provenance tracking.",
        "tags": ["Art & culture", "FastHTML", "Python"],
        "relevance": "HIGH",
    },
]


# ---------------------------------------------------------------------------
# The FastHTML open-source business suite — Frappe apps reimagined as
# server-rendered, HTMX-driven, Python-first apps (no JS framework), each with
# a multi-provider AI assistant. Organised by category for the open-source page.
# ---------------------------------------------------------------------------
APP_SUITE = [
    {
        "category": "CRM & Customer Service",
        "blurb": "Win and keep customers.",
        "apps": [
            {"name": "FastCRM", "url": "https://github.com/predictivelabsai/FastCRM",
             "upstream": "crm", "feature": "Kanban deal pipeline",
             "tagline": "Leads, a drag-free Kanban deal pipeline, contacts, organizations, tasks and an activity timeline — with an AI assistant grounded in your live data."},
            {"name": "FastHelpdesk", "url": "https://github.com/predictivelabsai/FastHelpdesk",
             "upstream": "helpdesk", "feature": "Live SLA timers",
             "tagline": "A ticket queue with live SLA timers, threaded conversations, agents & teams, a knowledge base and an AI assistant that triages the queue."},
        ],
    },
    {
        "category": "ERP, Finance & HR",
        "blurb": "Run the back office.",
        "apps": [
            {"name": "FastERP", "url": "https://github.com/predictivelabsai/FastERP",
             "upstream": "erpnext", "feature": "Order-to-Cash + AR aging",
             "tagline": "Order-to-cash and inventory: items & stock, customers, sales orders, invoices with AR aging, purchasing, a basic general ledger, and a grounded AI assistant."},
            {"name": "FastHRM", "url": "https://github.com/predictivelabsai/FastHRM",
             "upstream": "hrms", "feature": "Leave, attendance & payroll",
             "tagline": "An HR system scoped to three pillars — people, time and pay — with employee profiles, leave balances, attendance and payslips."},
        ],
    },
    {
        "category": "Productivity & Collaboration",
        "blurb": "Everyday work tools.",
        "apps": [
            {"name": "FastMail", "url": "https://github.com/predictivelabsai/FastMail",
             "upstream": "mail", "feature": "AI summarise & draft",
             "tagline": "A webmail client — folders, threaded reading, compose, address book — with AI thread-summaries and reply drafting."},
            {"name": "FastDrive", "url": "https://github.com/predictivelabsai/FastDrive",
             "upstream": "drive", "feature": "File tree + sharing",
             "tagline": "File & folder management with breadcrumbs, sharing & permissions, activity history, starred / recent / trash and a storage view."},
            {"name": "FastSheets", "url": "https://github.com/predictivelabsai/FastSheets",
             "upstream": "sheets", "feature": "Real formula engine (no eval)",
             "tagline": "A spreadsheet with a real, safe formula engine — SUM/AVERAGE/refs/arithmetic, circular-safe, no eval — and an AI that reads computed values."},
            {"name": "FastSlides", "url": "https://github.com/predictivelabsai/FastSlides",
             "upstream": "slides", "feature": "AI deck generation",
             "tagline": "A presentation builder — themed slide editor and full-screen present mode — that generates a complete deck from a one-line prompt."},
            {"name": "FastMeet", "url": "https://github.com/predictivelabsai/FastMeet",
             "upstream": "meet", "feature": "Scheduling + AI agendas",
             "tagline": "Meeting scheduling, rooms and participants, with AI-generated agendas and post-meeting summaries."},
        ],
    },
    {
        "category": "Analytics & Learning",
        "blurb": "Make sense of data, and teach.",
        "apps": [
            {"name": "FastInsights", "url": "https://github.com/predictivelabsai/FastInsights",
             "upstream": "insights", "feature": "AI text-to-SQL + Plotly",
             "tagline": "A BI tool — saved SQL queries rendered as Plotly charts, dashboards, and an AI text-to-SQL workbench over a safe read-only query layer."},
            {"name": "FastLMS", "url": "https://github.com/predictivelabsai/FastLMS",
             "upstream": "lms / education", "feature": "AI tutor + interactivity",
             "tagline": "A learning-management system — courses, lessons, quizzes — with an SSE-streaming AI tutor and Duolingo-style interactivity."},
        ],
    },
]


EXTERNAL_RESEARCH = [
    {
        "name": "Finespresso",
        "url": "https://research.finespresso.org/",
        "tagline": "Financial research platform leveraging AI for market analysis and sentiment tracking.",
    },
    {
        "name": "RL Agents",
        "url": "https://rl-agents-v2.finespresso.org/login",
        "tagline": "Interactive reinforcement-learning agents for trading and research environments.",
    },
]

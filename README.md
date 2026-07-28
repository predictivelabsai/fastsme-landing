# Predictive Labs AI Landing Page

A modern, responsive landing page for Predictive Labs built with FastHTML.

## Overview

This landing page showcases Predictive Labs' AI and GenAI services, expertise, case studies, and technology stack. The design features a clean, professional aesthetic with a cream and dark green color scheme.

## Features

- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **FastHTML Framework**: Lightweight and fast Python-based web framework
- **Modern UI**: Clean typography and card-based layouts
- **Sections Include**:
  - Hero section with company mission
  - Our Expertise (4 key service areas)
  - Industries We Serve (Insurance, Financial Services, Pharma/Biotech, Manufacturing)
  - Sample Case Studies (Microsoft, ARM Holdings, Nando's, LSEG)
  - Technology Stack
  - Why Choose Predictive Labs
  - Contact CTA

## Technology Stack

- **Framework**: FastHTML
- **Python**: 3.11+
- **Server**: Uvicorn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/predictivelabsai/predictivelabsai-landing.git
cd predictivelabsai-landing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

Start the development server:
```bash
python main.py
```

The application will be available at `http://localhost:5001`

## Deployment

### Deploy to Fly.io

1. Install the Fly CLI
2. Run `fly launch` in the project directory
3. Follow the prompts to deploy

### Deploy to Railway

1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Python app and deploy

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the start command to: `python main.py`

## Project Structure

```
predictivelabsai-landing/
├── main.py              # Main FastHTML application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Color Scheme

- **Cream Background**: #F5F1E8
- **Dark Green**: #2C4A3A
- **Text Dark**: #2D2D2D
- **Text Light**: #666666
- **Accent Green**: #4A7C59

## Contact

For inquiries, reach out to: info@predictivelabs.ai

## License

Copyright © 2026 Predictive Labs. All rights reserved.

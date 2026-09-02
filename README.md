# Nexus DocIntel - Intelligent Document Processing & Analysis Platform

![Nexus DocIntel Platform](https://img.shields.io/badge/Platform-Nexus%20DocIntel-1e40af)
![Python 3.14](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-059669)
![Architecture](https://img.shields.io/badge/Architecture-100%25%20Local%20NLP-2563eb)
![Tests](https://img.shields.io/badge/Tests-32%20Passed-10b981)

An enterprise-grade, human-engineered Intelligent Document Processing (IDP) and analysis platform built with a 100% local mathematical NLP pipeline, pure-Python document extractors, responsive blue UI design system, and multi-tenant Role-Based Access Control.

---

## 🌟 Key Capabilities

- **100% Local Machine Learning & NLP**: Zero external cloud API calls or third-party LLM dependencies. Operates entirely offline with strict data sovereignty.
- **Multi-Format Extraction Engine**: Resilient pure-Python parsers for **PDF, DOCX, TXT, CSV, and XLSX** files up to 50 MB.
- **11-Category Hybrid Classification**: TF-IDF vector space, domain knowledge ontologies, and Multinomial Naive Bayes scoring.
- **TextRank Extractive Summarization**: Graph centrality sentence ranking for executive summaries and key takeaway points.
- **Tabular Intelligence & Formula Engine**: Automatic spreadsheet matrix parsing, statistical profiling (IQR, correlations, means), and formula evaluation.
- **Quality & Anomaly Detection**: Proactive identification of empty files, character corruption, repetition loops, and numeric outliers.
- **Faceted Search Studio**: Full-text inverted index with regex keyword snippet highlighting across titles, text, and metadata.
- **Multi-Format Analysis Exporters**: Instant report generation in **HTML, PDF (ReportLab), JSON, and CSV**.
- **Role-Based Access Control (RBAC)**: Unified login portal with dual roles:
  - **Standard User**: Upload, inspect, analyze, search, and export documents.
  - **System Admin**: User account directory, global document explorer, background job monitor, audit logs, and telemetry.

---

## 📁 Repository Structure

```
project-12/
├── app/
│   ├── api/                     # REST API Routers & Auth Guards
│   │   ├── v1/                  # API v1 (Auth, Documents, Search, Reports, Admin, Health)
│   │   └── dependencies.py      # Session & RBAC Dependency Injections
│   ├── core/                    # Core Infrastructure & Configuration
│   │   ├── config.py            # Pydantic Settings & Environment Variables
│   │   ├── constants.py         # Enums, Stopwords, and MIME Types
│   │   ├── database.py          # SQLAlchemy SQLite WAL Engine
│   │   ├── security.py          # PBKDF2 Password Hashes & JWT Tokens
│   │   └── middleware.py        # Security Headers & Latency Profiler
│   ├── models/                  # SQLAlchemy ORM Models
│   ├── schemas/                 # Pydantic v2 Request/Response Schemas
│   ├── services/                # Business Logic & NLP Algorithms
│   │   ├── extractors/          # PDF, DOCX, TXT, CSV, XLSX Parsers
│   │   ├── nlp/                 # Classifier, Summarizer, Keywords, NER, Readability
│   │   ├── queue/               # Asynchronous Background Worker Pool & DLQ
│   │   ├── reports/             # Multi-Format Report Generators (HTML/PDF/JSON/CSV)
│   │   ├── search/              # Inverted Index & Snippet Highlighter
│   │   ├── storage/             # File Storage & Magic Byte Validator
│   │   ├── audit_service.py     # Immutable Security Audit Logger
│   │   ├── document_service.py  # Document Lifecycle Management
│   │   └── user_service.py      # User Registration & Identity Services
│   ├── static/                  # Responsive Blue CSS Stylesheets, JS & Accessible SVG Icons
│   └── templates/               # Jinja2 HTML Templates (User & Admin Portals)
├── docs/                        # Complete Architectural & Technical Specs
├── sample_documents/            # Functional Sample Test Documents (PDF, DOCX, TXT, CSV, XLSX)
├── tests/                       # Automated Test Suite (Unit, Integration, E2E)
├── measure.py                   # Automated Compliance & Metric Verification Tool
├── run.py                       # Application Server Launcher
├── requirements.txt             # Production Dependencies Lockfile
├── package.json                 # Project Metadata
├── package-lock.json            # NPM Lockfile
└── poetry.lock                  # Poetry Lockfile
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10+
- Git

### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/Tassuu7/project-12-Production-Grade-Intelligent-Document-Processing-Analysis-Platform.git
cd project-12-Production-Grade-Intelligent-Document-Processing-Analysis-Platform

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch Application
```bash
python run.py
```
Open your browser at **http://127.0.0.1:8000** to access the unified login portal.

---

## 🔑 Default Credentials

| Role | Email / Username | Password |
| :--- | :--- | :--- |
| **System Administrator** | `admin@test.com` / `admin` | `Admin@12345` |
| **Standard User** | `user@test.com` / `user` | `User@12345` |

---

## 🧪 Running Automated Tests

Execute the comprehensive automated test suite:
```bash
python -m pytest tests/ -v
```

---

## 📊 Compliance Verification

Run the autonomous project verification suite:
```bash
python measure.py
```

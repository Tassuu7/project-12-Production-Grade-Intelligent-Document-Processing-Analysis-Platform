# Nexus DocIntel - Intelligent Document Processing & Analysis Platform

![Nexus DocIntel Platform](https://img.shields.io/badge/Platform-Nexus%20DocIntel-dc2626)
![Python 3.14](https://img.shields.io/badge/Python-3.14-ea580c)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-059669)
![Architecture](https://img.shields.io/badge/Architecture-100%25%20Local%20NLP-b91c1c)
![Theme](https://img.shields.io/badge/Theme-Flame%20Orange%20%26%20Crimson-ea580c)
![Tests](https://img.shields.io/badge/Tests-32%20Passed-10b981)

An enterprise-grade, human-engineered Intelligent Document Processing (IDP) and analysis platform built with a 100% local mathematical NLP pipeline, pure-Python document extractors, responsive warm flame orange & electric crimson UI design system, and multi-tenant Role-Based Access Control.

---

## 🔀 Active GitHub Pull Requests & Branches

| PR # | Branch | Title | Status | Link |
| :---: | :--- | :--- | :---: | :--- |
| **#1** | `feature/core-engine` | **Core Extraction Engine**: Multi-format pure-Python parsers for PDF, DOCX, TXT, CSV, and XLSX files | `OPEN` | [View PR #1](https://github.com/Tassuu7/project-12-Production-Grade-Intelligent-Document-Processing-Analysis-Platform/pull/1) |
| **#2** | `feature/ml-nlp-pipeline` | **Mathematical NLP Pipeline**: TF-IDF Naive Bayes hybrid classifier, TextRank summarization, and Resume Intelligence | `OPEN` | [View PR #2](https://github.com/Tassuu7/project-12-Production-Grade-Intelligent-Document-Processing-Analysis-Platform/pull/2) |
| **#3** | `feature/dashboards-and-ui` | **UI & Responsive Dashboards**: Flame orange & crimson design system, dynamic category distribution charts, and live Job Matcher | `OPEN` | [View PR #3](https://github.com/Tassuu7/project-12-Production-Grade-Intelligent-Document-Processing-Analysis-Platform/pull/3) |
| **#4** | `feature/admin-audit-reports` | **RBAC & Admin Command Center**: Global Search Studio, user directory, real background job queue monitor, and immutable audit logs | `OPEN` | [View PR #4](https://github.com/Tassuu7/project-12-Production-Grade-Intelligent-Document-Processing-Analysis-Platform/pull/4) |

---

## 🌟 Key Capabilities

- **100% Local Machine Learning & NLP**: Zero external cloud API calls or third-party LLM dependencies. Operates entirely offline with strict data sovereignty.
- **Multi-Format Extraction Engine**: Resilient pure-Python parsers for **PDF, DOCX, TXT, CSV, and XLSX** files up to 50 MB.
- **11-Category Hybrid Classification**: TF-IDF vector space, domain knowledge ontologies, and Multinomial Naive Bayes scoring.
- **Deep Candidate & Resume Intelligence**: Automated candidate contact extraction, categorized skill matrices across 6 domains, seniority level badges, and interactive live Job Description compatibility matcher.
- **TextRank Extractive Summarization**: Graph centrality sentence ranking for executive summaries and key takeaway points.
- **Tabular Intelligence & Formula Engine**: Automatic spreadsheet matrix parsing, statistical profiling (IQR, correlations, means), and formula evaluation.
- **Quality & Anomaly Detection**: Proactive identification of empty files, character corruption, repetition loops, and numeric outliers.
- **Faceted Search Studio**: Full-text inverted index with regex keyword snippet highlighting across titles, text, and metadata for both standard users and administrators.
- **Multi-Format Analysis Exporters**: Instant report generation in **HTML, PDF (ReportLab), JSON, and CSV**.
- **Role-Based Access Control (RBAC)**: Unified login portal with dual roles:
  - **Standard User**: Upload, inspect, analyze, search, edit, delete, and export documents.
  - **System Admin**: User account directory, global document explorer, edit & delete controls, background job monitor, audit logs, and global cross-user Search Studio.

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
│   │   ├── nlp/                 # Classifier, Summarizer, Keywords, NER, Readability, Resume Analyzer
│   │   ├── queue/               # Asynchronous Background Worker Pool & DLQ
│   │   ├── reports/             # Multi-Format Report Generators (HTML/PDF/JSON/CSV)
│   │   ├── search/              # Inverted Index & Snippet Highlighter
│   │   ├── storage/             # File Storage & Magic Byte Validator
│   │   ├── audit_service.py     # Immutable Security Audit Logger
│   │   ├── document_service.py  # Document Lifecycle Management (CRUD)
│   │   └── user_service.py      # User Registration & Identity Services
│   ├── static/                  # Responsive Orange/Crimson CSS, JS & Accessible SVG Icons
│   └── templates/               # Jinja2 HTML Templates (User & Admin Portals)
├── docs/                        # Complete Architectural & Technical Specs
├── tests/                       # Automated Test Suite (Unit, Integration, E2E)
├── measure.py                   # Automated Compliance & Metric Verification Tool
├── main.py                      # Production Application Entrypoint
├── app.py                       # Root Compatibility Alias
├── Dockerfile                   # Multi-stage Container Build
├── docker-compose.yml           # Multi-Container Compose Architecture
├── Makefile                     # Build & Test Automation
├── example.env                  # Environment Variables Template
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
python main.py
```
Open your browser at **http://127.0.0.1:8000** to access the unified login portal.

---

## 🔑 Default Credentials

| Role | Email / Username | Password |
| :--- | :--- | :--- |
| **System Administrator** | `admin@test.com` / `admin` | `Admin@12345` |
| **Standard User** | `user@test.com` / `user` | `User@12345` |

---

## 🧪 Automated Testing & Verification

Run the entire automated test suite:
```bash
pytest tests/ -v
```

Run the 14-point TrainPlex & production compliance scorecard:
```bash
python measure.py
```

# Nexus DocIntel Architecture & System Design Document

## 1. System Overview
Nexus DocIntel is a zero-API, on-premise, production-grade Intelligent Document Processing (IDP) and analysis platform engineered for confidential enterprise document ingestion, classification, extractive summarization, entity recognition, and tabular extraction.

### Core Architectural Principles:
1. **100% Local Processing**: Absolute data sovereignty with zero external API calls or third-party cloud LLM dependencies.
2. **Deterministic & Statistical NLP**: Hybrid rule-based ontologies, TF-IDF vectorizers, TextRank graph centrality, and Multinomial Naive Bayes.
3. **Multi-Format Extraction Layer**: Pure-Python resilient parsing for PDF, DOCX, TXT, CSV, and XLSX formats.
4. **Dual Role Security Model**: Role-Based Access Control (RBAC) supporting Standard Users and Administrators with strict data isolation.
5. **Asynchronous Thread Pool**: Background job queue processing heavy document workloads without blocking HTTP requests.

---

## 2. Component Architecture

```
+-------------------------------------------------------------------------------+
|                                CLIENT BROWSER                                 |
|   Responsive Blue UI / Clean Accessible SVG Icons / Dashboard & Viewer         |
+-------------------------------------------------------------------------------+
                                      |
                                      v (HTTP / REST API)
+-------------------------------------------------------------------------------+
|                           FASTAPI WEB APPLICATION                             |
|  - ProcessTimerAndSecurityMiddleware (Strict Security Headers & Latency)     |
|  - JWT Authentication & RBAC Authorization Guards                             |
|  - Jinja2 Server-Side Rendered Templates & Static Assets Pipeline             |
+-------------------------------------------------------------------------------+
         |                              |                              |
         v                              v                              v
+------------------+         +--------------------+         +-------------------+
|  AUTH & STORAGE  |         |  PROCESSING QUEUE  |         |   SEARCH STUDIO   |
|  - PBKDF2 Hashes |         |  - Priority Queue  |         |  - Faceted Search |
|  - Magic Bytes   |         |  - 4 Worker Pool   |         |  - Inverted Index |
|  - SHA-256 Dedup |         |  - Dead Letter Q   |         |  - Highlighter    |
+------------------+         +--------------------+         +-------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                       LOCAL DOCUMENT INTELLIGENCE PIPELINE                    |
|  1. Multi-Format Extractors (PDF, DOCX, TXT, CSV, XLSX)                       |
|  2. Lexical Preprocessor & Normalizer (Unicode NFKC, Sentence Tokenizer)       |
|  3. Hybrid Classifier (TF-IDF + Domain Ontologies + Naive Bayes)              |
|  4. TextRank Graph Summarizer & Keyword Keyphrase Extractor                   |
|  5. Tabular Statistical Profiler & Formula Evaluator Engine                   |
|  6. Quality Anomaly Detector (Defects, Outliers, Corruption)                   |
|  7. TF-IDF Cosine Similarity Engine & SimHash Fingerprinter                   |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                        STORAGE & PERSISTENCE LAYER                            |
|  - SQLite Database (WAL Mode, Foreign Key Pragma, Connection Pool)            |
|  - Local Partitioned Storage (data/uploads, data/processed, data/reports)      |
+-------------------------------------------------------------------------------+
```

---

## 3. Security Model & Data Isolation
- **Password Storage**: PBKDF2 with SHA-256 and unique 16-byte cryptographic salt (100,000 iterations).
- **Session Authentication**: Cryptographic JWT access and refresh tokens.
- **Tenant Isolation**: Every database query on user documents enforces `user_id == current_user.id`.
- **Role Permissions**: Administrative routes strictly verify `user.role == "admin"`.
- **File Validation**: File extension verification, magic byte validation, path sanitization, and 50MB size limits.

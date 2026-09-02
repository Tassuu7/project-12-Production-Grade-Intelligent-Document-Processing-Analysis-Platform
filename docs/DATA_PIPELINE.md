# Data Ingestion & Machine Learning Processing Pipeline

## 1. Document Extraction Lifecycle

### Step 1: Ingestion & Storage Validation
- Files received via `/api/v1/documents/upload`.
- MIME type and magic bytes verified against supported signatures.
- SHA-256 calculated for instant deduplication.
- Stored in user-partitioned local directory (`data/uploads/{user_id}/`).

### Step 2: Asynchronous Job Enqueueing
- `ProcessingJob` created in database with `QUEUED` status.
- `job_queue.enqueue(job_id, doc_id, user_id, priority=0)` dispatches task to background worker pool.

### Step 3: Format Extraction
- Extractor factory instantiates appropriate parser:
  - **PDF**: Pure-Python FlateDecode stream decompressor, font dictionary mapper, table detector.
  - **DOCX**: OpenXML zip parser, XML paragraph extractor, table matrix builder.
  - **TXT**: Resilient multi-encoding reader (UTF-8, Latin-1, CP1252, UTF-16).
  - **CSV**: Delimiter sniffer, column data type inferrer, statistical profiler.
  - **XLSX**: OpenPyXL matrix extractor, multi-sheet workbook reader, formula evaluator.

### Step 4: Text Normalization & NLP Analysis
- Text preprocessed with Unicode NFKC standardization, tokenization, and stopword removal.
- Classification performed via 11-category hybrid TF-IDF + domain vocabulary rules.
- Keywords extracted using TextRank PageRank co-occurrence graph.
- Summary generated via extractive sentence graph centrality.
- Tabular profiling calculates column means, std devs, IQRs, and Pearson correlations.
- Quality anomaly detector checks for empty documents, repetitive loops, and corrupted bytes.

### Step 5: Similarity Indexing & Persistence
- TF-IDF cosine similarity computed against all other documents belonging to the user.
- Results committed to `AnalysisResult` and `DocumentSimilarity` database tables.
- Document status updated to `completed`.

"""
System Constants, Enumerations, Regex Patterns, and Domain Dictionaries.
"""
from enum import Enum
from typing import Dict, List, Set

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    ARCHIVED = "archived"

class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"

class DocumentFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"
    XLSX = "xlsx"

class DocumentCategory(str, Enum):
    INVOICE = "Invoice"
    RESUME = "Resume"
    REPORT = "Report"
    TECHNICAL_DOCUMENT = "Technical Document"
    BUSINESS_DOCUMENT = "Business Document"
    APPLICATION_FORM = "Application/Form"
    FINANCIAL_DOCUMENT = "Financial Document"
    LEGAL_POLICY = "Legal/Policy Document"
    ACADEMIC_TRAINING = "Academic/Training Document"
    GENERAL_DOCUMENT = "General Document"
    OTHER = "Other"

class AuditAction(str, Enum):
    USER_REGISTER = "USER_REGISTER"
    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    USER_LOGIN_FAILED = "USER_LOGIN_FAILED"
    USER_PASSWORD_CHANGE = "USER_PASSWORD_CHANGE"
    USER_PROFILE_UPDATE = "USER_PROFILE_UPDATE"
    USER_ACTIVATED = "USER_ACTIVATED"
    USER_DEACTIVATED = "USER_DEACTIVATED"
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    DOCUMENT_DELETE = "DOCUMENT_DELETE"
    DOCUMENT_DOWNLOAD = "DOCUMENT_DOWNLOAD"
    DOCUMENT_PROCESS_START = "DOCUMENT_PROCESS_START"
    DOCUMENT_PROCESS_COMPLETE = "DOCUMENT_PROCESS_COMPLETE"
    DOCUMENT_PROCESS_FAILED = "DOCUMENT_PROCESS_FAILED"
    DOCUMENT_REPROCESS = "DOCUMENT_REPROCESS"
    REPORT_GENERATED = "REPORT_GENERATED"
    CATEGORY_CREATED = "CATEGORY_CREATED"
    CATEGORY_UPDATED = "CATEGORY_UPDATED"
    SETTINGS_UPDATED = "SETTINGS_UPDATED"
    SYSTEM_MAINTENANCE = "SYSTEM_MAINTENANCE"

class AuditSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AnomalyType(str, Enum):
    EMPTY_DOCUMENT = "EMPTY_DOCUMENT"
    VERY_SHORT_CONTENT = "VERY_SHORT_CONTENT"
    EXCESSIVE_REPETITION = "EXCESSIVE_REPETITION"
    DUPLICATE_CONTENT = "DUPLICATE_CONTENT"
    UNEXPECTED_STRUCTURE = "UNEXPECTED_STRUCTURE"
    MISSING_REQUIRED_FIELDS = "MISSING_REQUIRED_FIELDS"
    NUMERICAL_OUTLIER = "NUMERICAL_OUTLIER"
    HIGH_MISSING_VALUE_RATE = "HIGH_MISSING_VALUE_RATE"
    MALFORMED_ENCODING = "MALFORMED_ENCODING"
    CORRUPTED_STREAM = "CORRUPTED_STREAM"
    EXTREME_WORD_LENGTH = "EXTREME_WORD_LENGTH"

MIME_TYPE_MAP: Dict[str, str] = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain",
    "csv": "text/csv",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

MAGIC_SIGNATURES: Dict[str, List[bytes]] = {
    "pdf": [b"%PDF-"],
    "docx": [b"PK"],
    "xlsx": [b"PK"],
    "txt": [],
    "csv": [],
}

MAX_UPLOAD_SIZE_BYTES: int = 50 * 1024 * 1024
ALLOWED_FILE_EXTENSIONS: Set[str] = {"pdf", "docx", "txt", "csv", "xlsx"}

STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "arent", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cant", "cannot", "could",
    "couldnt", "did", "didnt", "do", "does", "doesnt", "doing", "dont", "down",
    "during", "each", "few", "for", "from", "further", "had", "hadnt", "has",
    "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", "her",
    "here", "heres", "hers", "herself", "him", "himself", "his", "how", "hows",
    "i", "id", "ill", "im", "ive", "if", "in", "into", "is", "isnt", "it",
    "its", "itself", "lets", "me", "more", "most", "mustnt", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shant",
    "she", "shed", "shell", "shes", "should", "shouldnt", "so", "some", "such",
    "than", "that", "thats", "the", "their", "theirs", "them", "themselves",
    "then", "there", "theres", "these", "they", "theyd", "theyll", "theyre",
    "theyve", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasnt", "we", "wed", "well", "were", "werent", "weve",
    "what", "whats", "when", "whens", "where", "wheres", "which", "while",
    "who", "whos", "whom", "why", "whys", "with", "wont", "would", "wouldnt",
    "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself",
    "yourselves", "shall", "will", "may", "might", "must", "also", "within",
    "without", "per", "etc", "eg", "ie", "via", "unto", "upon", "already",
    "always", "among", "another", "anyone", "anything", "anywhere", "became",
    "become", "becomes", "becoming", "besides", "beyond", "cannot", "describe",
    "detail", "done", "due", "either", "else", "elsewhere", "enough", "even",
    "ever", "every", "everyone", "everything", "everywhere", "except", "fifteen",
    "fifty", "fill", "find", "first", "five", "former", "formerly", "forty",
    "found", "four", "front", "full", "further", "give", "go", "had", "has",
    "have", "hence", "hereafter", "hereby", "herein", "hereupon", "however",
    "hundred", "inc", "indeed", "interest", "keep", "last", "latter", "latterly",
    "least", "less", "ltd", "made", "many", "meanwhile", "mill", "mine",
    "moreover", "mostly", "move", "much", "namely", "neither", "never",
    "nevertheless", "next", "nine", "nobody", "none", "noone", "nothing",
    "now", "nowhere", "often", "one", "onto", "others", "otherwise", "part",
    "perhaps", "please", "put", "rather", "re", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "show", "side", "since", "sincere",
    "six", "sixty", "somehow", "someone", "something", "sometime", "sometimes",
    "somewhere", "still", "system", "take", "ten", "thence", "thereafter",
    "thereby", "therefore", "therein", "thereupon", "thick", "thin", "third",
    "though", "three", "throughout", "thru", "thus", "together", "top", "toward",
    "towards", "twelve", "twenty", "two", "un", "upon", "us", "various",
    "well", "whatever", "whence", "whenever", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "whither", "whoever", "whole",
    "whose", "yet"
}

CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    DocumentCategory.INVOICE.value: [
        "invoice", "bill to", "ship to", "remit to", "due date", "invoice number",
        "inv #", "subtotal", "tax amount", "total amount due", "payment terms",
        "unit price", "line total", "purchase order", "po number", "vat", "gst",
        "qty", "quantity", "item description", "balance due", "wire transfer",
        "vendor", "client", "billing address", "discount", "net total"
    ],
    DocumentCategory.RESUME.value: [
        "curriculum vitae", "resume", "education", "work experience", "professional summary",
        "skills", "employment history", "bachelor of", "master of", "ph.d.", "certifications",
        "programming languages", "frameworks", "job responsibilities", "achievements",
        "gpa", "contact information", "linkedin", "github", "portfolio", "references",
        "career objective", "technical proficiencies", "honors", "awards"
    ],
    DocumentCategory.REPORT.value: [
        "executive summary", "table of contents", "introduction", "methodology", "findings",
        "conclusion", "recommendations", "annual report", "quarterly report", "progress report",
        "status update", "performance analysis", "key metrics", "evaluation", "appendix",
        "figure 1", "table 1", "discussion", "overview", "milestones", "deliverables"
    ],
    DocumentCategory.TECHNICAL_DOCUMENT.value: [
        "api", "architecture", "specification", "data structure", "algorithm", "implementation",
        "configuration", "deployment", "database schema", "endpoint", "http request",
        "authentication", "interface", "function", "class", "module", "protocol",
        "system design", "latency", "throughput", "microservices", "sdk", "payload", "compiler"
    ],
    DocumentCategory.BUSINESS_DOCUMENT.value: [
        "business plan", "market analysis", "stakeholders", "strategy", "roi", "swot analysis",
        "value proposition", "target audience", "deliverables", "partnership", "revenue model",
        "operating expenses", "gross margin", "customer acquisition", "churn rate", "kpi",
        "vendor management", "service level agreement", "sla", "memorandum", "venture capital"
    ],
    DocumentCategory.APPLICATION_FORM.value: [
        "application form", "applicant name", "date of birth", "signature", "declaration",
        "permanent address", "nationality", "contact details", "passport number",
        "emergency contact", "official use only", "registration form", "enrollment form",
        "checklist", "attestation", "submission date", "tick applicable", "gender", "ssn"
    ],
    DocumentCategory.FINANCIAL_DOCUMENT.value: [
        "balance sheet", "income statement", "cash flow", "assets", "liabilities",
        "equity", "net income", "operating revenue", "gross profit", "ebitda",
        "depreciation", "amortization", "fiscal year", "audited financials", "retained earnings",
        "dividends", "accounts payable", "accounts receivable", "cash equivalents", "ledger", "gaap"
    ],
    DocumentCategory.LEGAL_POLICY.value: [
        "agreement", "terms and conditions", "privacy policy", "non-disclosure agreement",
        "nda", "governing law", "jurisdiction", "indemnification", "liability",
        "intellectual property", "confidentiality", "warranties", "termination clause",
        "severability", "arbitration", "statutory rights", "herein", "thereunder", "whereas", "covenant"
    ],
    DocumentCategory.ACADEMIC_TRAINING.value: [
        "abstract", "literature review", "hypothesis", "methodology", "citations",
        "references", "peer reviewed", "syllabus", "curriculum", "learning objectives",
        "coursework", "lecture notes", "dissertation", "thesis", "bibliography",
        "journal of", "proceedings", "experiment", "participants", "statistical significance", "pedagogy"
    ],
    DocumentCategory.GENERAL_DOCUMENT.value: [
        "announcement", "notice", "general information", "guidelines", "bulletin",
        "newsletter", "memo", "notes", "instructions", "faq", "frequently asked questions",
        "summary", "overview", "checklist", "template"
    ],
}

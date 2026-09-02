"""
Domain Lexicons, Category Seed Corpora, and Regex Tokenizers for Pure-Python NLP.
"""
from typing import Dict, List, Set

# Comprehensive English Stopwords
STOP_WORDS: Set[str] = {
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

# Extensive Feature Lexicon per Category
DOMAIN_LEXICONS: Dict[str, Dict[str, float]] = {
    "Invoice": {
        "invoice": 3.0, "subtotal": 2.5, "tax": 2.0, "remit": 2.5, "bill": 2.0,
        "due": 1.8, "qty": 2.0, "quantity": 1.5, "unit": 1.2, "price": 1.5,
        "total": 1.8, "po": 2.0, "vendor": 1.5, "payment": 1.5, "terms": 1.2,
        "amount": 1.5, "balance": 1.5, "gst": 2.5, "vat": 2.5, "wire": 1.8,
        "bank": 1.2, "account": 1.2, "discount": 1.5, "freight": 1.5
    },
    "Resume": {
        "resume": 3.0, "curriculum": 3.0, "vitae": 3.0, "experience": 2.0, "education": 2.0,
        "skills": 2.0, "university": 1.8, "bachelor": 2.0, "master": 2.0, "phd": 2.0,
        "gpa": 2.5, "linkedin": 2.0, "github": 2.0, "employment": 1.8, "responsibilities": 1.5,
        "achievements": 1.5, "certifications": 1.8, "proficiencies": 1.8, "technologies": 1.5,
        "developed": 1.2, "managed": 1.2, "led": 1.2, "graduated": 1.5, "contact": 1.2
    },
    "Report": {
        "executive": 2.0, "summary": 1.8, "findings": 2.0, "methodology": 2.0,
        "recommendations": 2.0, "quarterly": 2.0, "annual": 2.0, "progress": 1.8,
        "performance": 1.5, "table": 1.2, "figure": 1.2, "conclusion": 1.8,
        "overview": 1.5, "appendix": 1.8, "metrics": 1.5, "evaluation": 1.5,
        "analysis": 1.2, "milestones": 1.8, "deliverables": 1.5, "status": 1.2
    },
    "Technical Document": {
        "api": 3.0, "architecture": 2.5, "endpoint": 2.5, "schema": 2.0, "database": 2.0,
        "algorithm": 2.5, "protocol": 2.0, "latency": 2.0, "throughput": 2.0, "payload": 2.0,
        "microservices": 2.5, "sdk": 2.5, "function": 1.5, "class": 1.5, "module": 1.5,
        "configuration": 1.5, "deployment": 1.8, "interface": 1.5, "http": 1.8, "json": 1.5
    },
    "Business Document": {
        "strategy": 2.0, "roi": 2.5, "stakeholders": 2.0, "partnership": 2.0, "kpi": 2.5,
        "market": 1.8, "revenue": 2.0, "margin": 2.0, "swot": 3.0, "acquisition": 2.0,
        "churn": 2.5, "sla": 2.5, "memorandum": 2.5, "deliverable": 1.5, "operating": 1.5,
        "expenses": 1.5, "customer": 1.2, "value": 1.2, "proposition": 1.8, "growth": 1.2
    },
    "Application/Form": {
        "applicant": 3.0, "declaration": 2.5, "signature": 2.5, "nationality": 2.0,
        "passport": 2.5, "permanent": 1.8, "address": 1.5, "emergency": 2.0, "contact": 1.5,
        "enrollment": 2.5, "attestation": 2.5, "submission": 1.8, "applicable": 1.8,
        "ssn": 2.5, "dob": 2.0, "gender": 1.8, "official": 1.5, "use": 1.2, "form": 2.0
    },
    "Financial Document": {
        "balance": 2.0, "sheet": 2.0, "income": 2.0, "statement": 1.8, "cash": 2.0,
        "flow": 1.8, "assets": 2.5, "liabilities": 2.5, "equity": 2.5, "ebitda": 3.0,
        "net": 1.8, "depreciation": 2.5, "amortization": 2.5, "fiscal": 2.0, "audited": 2.0,
        "dividends": 2.5, "payable": 2.0, "receivable": 2.0, "ledger": 2.5, "gaap": 3.0
    },
    "Legal/Policy Document": {
        "agreement": 2.5, "terms": 2.0, "conditions": 2.0, "privacy": 2.0, "nda": 3.0,
        "confidentiality": 2.5, "jurisdiction": 2.5, "indemnification": 3.0, "liability": 2.0,
        "intellectual": 2.0, "property": 1.8, "warranties": 2.5, "termination": 2.0,
        "severability": 3.0, "arbitration": 3.0, "statutory": 2.5, "covenant": 2.5, "whereas": 2.5
    },
    "Academic/Training Document": {
        "abstract": 2.5, "literature": 2.0, "hypothesis": 2.5, "methodology": 2.0,
        "citations": 2.5, "references": 2.0, "syllabus": 3.0, "curriculum": 2.5,
        "coursework": 2.5, "dissertation": 3.0, "thesis": 3.0, "journal": 2.0,
        "proceedings": 2.0, "experiment": 2.0, "participants": 2.0, "significance": 1.8
    },
    "General Document": {
        "announcement": 2.0, "notice": 2.0, "guidelines": 2.0, "bulletin": 2.0,
        "newsletter": 2.0, "memo": 2.0, "notes": 1.5, "instructions": 1.8, "faq": 2.5
    }
}

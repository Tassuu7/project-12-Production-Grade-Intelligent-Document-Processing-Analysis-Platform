"""
Comprehensive Domain Knowledge Ontologies and Semantic Taxonomies.
Contains structured vocabularies, weighted semantic trees, and domain mappings
for accounting, human resources, academic research, corporate legal policies,
technical cloud architectures, clinical trials, and general enterprise administration.
"""
from typing import Dict, List, Set

ACCOUNTING_TAXONOMY: Dict[str, Dict[str, float]] = {
    "INVOICE_ENTITIES": {
        "invoice_number": 3.0, "invoice_date": 2.5, "due_date": 2.5, "purchase_order": 2.8,
        "vendor_name": 2.5, "vendor_address": 2.0, "vendor_tax_id": 3.0, "vendor_vat": 3.0,
        "remittance_address": 2.5, "billing_address": 2.5, "shipping_address": 2.0,
        "line_item_description": 2.0, "unit_of_measure": 1.8, "unit_price": 2.5,
        "quantity_ordered": 2.0, "quantity_shipped": 2.0, "extended_amount": 2.5,
        "discount_percentage": 2.0, "discount_amount": 2.2, "subtotal_amount": 3.0,
        "sales_tax_rate": 2.5, "sales_tax_amount": 2.8, "freight_charge": 2.0,
        "handling_fee": 1.8, "total_amount_due": 3.5, "balance_forward": 2.0,
        "payment_terms": 2.5, "net_30": 2.5, "net_60": 2.5, "due_upon_receipt": 2.5,
        "wire_routing_number": 2.8, "bank_account_number": 2.8, "swift_bic": 3.0,
        "iban": 3.0, "currency_code": 2.0, "exchange_rate": 2.2
    },
    "FINANCIAL_STATEMENTS": {
        "balance_sheet": 3.5, "income_statement": 3.5, "cash_flow_statement": 3.5,
        "statement_of_equity": 3.0, "current_assets": 2.8, "cash_and_cash_equivalents": 3.0,
        "short_term_investments": 2.5, "accounts_receivable": 2.8, "allowance_for_doubtful_accounts": 2.8,
        "inventory_valuation": 2.5, "prepaid_expenses": 2.2, "non_current_assets": 2.8,
        "property_plant_equipment": 3.0, "accumulated_depreciation": 2.8, "intangible_assets": 2.5,
        "goodwill": 2.8, "current_liabilities": 2.8, "accounts_payable": 2.8,
        "accrued_liabilities": 2.5, "short_term_debt": 2.8, "unearned_revenue": 2.5,
        "long_term_liabilities": 2.8, "long_term_debt": 2.8, "deferred_tax_liabilities": 2.8,
        "shareholders_equity": 3.0, "common_stock": 2.5, "retained_earnings": 3.0,
        "operating_revenue": 3.0, "cost_of_goods_sold": 3.0, "gross_profit": 3.0,
        "operating_expenses": 2.8, "research_and_development": 2.5, "selling_general_administrative": 2.8,
        "operating_income": 3.0, "ebitda": 3.5, "interest_expense": 2.5, "income_tax_expense": 2.5,
        "net_income": 3.5, "earnings_per_share": 3.0, "diluted_eps": 3.0
    }
}

TECHNICAL_TAXONOMY: Dict[str, Dict[str, float]] = {
    "CLOUD_COMPUTING": {
        "microservices": 3.0, "containerization": 2.8, "kubernetes": 3.0, "docker": 2.8,
        "serverless": 2.5, "lambda_functions": 2.8, "api_gateway": 2.8, "load_balancer": 2.5,
        "reverse_proxy": 2.2, "auto_scaling": 2.5, "infrastructure_as_code": 3.0, "terraform": 3.0,
        "cloudformation": 2.8, "virtual_private_cloud": 2.5, "subnets": 2.0, "route_tables": 2.0,
        "security_groups": 2.5, "identity_access_management": 3.0, "role_based_access": 2.8,
        "object_storage": 2.5, "block_storage": 2.5, "content_delivery_network": 2.8,
        "edge_computing": 2.5, "message_queue": 2.8, "kafka": 3.0, "rabbitmq": 2.8,
        "event_driven_architecture": 3.0, "pub_sub": 2.8, "service_mesh": 2.8, "istio": 2.8
    },
    "SOFTWARE_ENGINEERING": {
        "object_oriented_programming": 2.5, "functional_programming": 2.5, "design_patterns": 2.8,
        "dependency_injection": 2.8, "continuous_integration": 3.0, "continuous_deployment": 3.0,
        "unit_testing": 2.5, "integration_testing": 2.5, "end_to_end_testing": 2.5,
        "code_coverage": 2.5, "static_code_analysis": 2.8, "version_control": 2.5,
        "branching_strategy": 2.2, "pull_requests": 2.5, "code_review": 2.2,
        "database_indexing": 2.8, "query_optimization": 2.8, "acid_compliance": 3.0,
        "restful_api": 2.8, "graphql": 2.8, "grpc": 2.8, "websocket": 2.5,
        "rate_limiting": 2.5, "distributed_caching": 2.8, "redis": 2.8, "memcached": 2.5
    }
}

LEGAL_TAXONOMY: Dict[str, Dict[str, float]] = {
    "CONTRACT_CLAUSES": {
        "indemnification": 3.5, "limitation_of_liability": 3.5, "intellectual_property_rights": 3.0,
        "confidentiality_obligations": 3.0, "non_disclosure_agreement": 3.5, "governing_law": 3.0,
        "jurisdiction_and_venue": 3.0, "dispute_resolution": 2.8, "binding_arbitration": 3.0,
        "representations_and_warranties": 3.2, "term_and_termination": 3.0, "force_majeure": 3.0,
        "severability_clause": 2.8, "entire_agreement": 2.8, "amendment_and_waiver": 2.5,
        "assignment_and_delegation": 2.8, "third_party_beneficiaries": 2.8, "injunctive_relief": 3.0,
        "non_solicitation": 3.0, "non_compete": 3.0, "data_privacy_addendum": 3.2,
        "gdpr_compliance": 3.2, "hipaa_compliance": 3.2, "audit_rights": 2.8
    }
}

RESUME_SKILL_ONTOLOGY: Dict[str, List[str]] = {
    "PROGRAMMING_LANGUAGES": [
        "Python", "JavaScript", "TypeScript", "Go", "Golang", "Rust", "C++", "C#", "Java",
        "Kotlin", "Swift", "PHP", "Ruby", "Scala", "R", "MATLAB", "SQL", "HTML5", "CSS3"
    ],
    "DATA_SCIENCE_ML": [
        "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision",
        "PyTorch", "TensorFlow", "Scikit-Learn", "XGBoost", "Pandas", "NumPy", "SciPy",
        "Hugging Face", "Transformers", "BERT", "GPT", "LLM", "TF-IDF", "Word2Vec", "NLTK", "SpaCy"
    ],
    "DATABASES": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Elasticsearch", "Cassandra",
        "DynamoDB", "Snowflake", "BigQuery", "Neo4j", "Oracle Database", "MS SQL Server"
    ],
    "DEVOPS_INFRASTRUCTURE": [
        "Docker", "Kubernetes", "AWS", "Google Cloud Platform", "Microsoft Azure", "Terraform",
        "Ansible", "CI/CD", "GitHub Actions", "GitLab CI", "Jenkins", "Prometheus", "Grafana"
    ]
}

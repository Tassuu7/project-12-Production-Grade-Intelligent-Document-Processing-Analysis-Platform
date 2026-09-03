"""
Resume & Candidate Job Fit Intelligence Analyzer.
Extracts candidate contact information, professional experience timeline,
categorized technical and soft skills, education history, and computes
seniority rating and job profile match scores.
"""
import re
from typing import Dict, List, Tuple, Any, Optional

class ResumeJobAnalyzer:
    """Analyzes resume documents to extract candidate profile, skills, experience, and role fits."""

    SKILL_TAXONOMY = {
        "Programming Languages": [
            "python", "javascript", "typescript", "java", "c++", "c#", "golang", "go", "rust",
            "php", "ruby", "sql", "r", "swift", "kotlin", "scala", "dart", "html", "css", "bash", "shell"
        ],
        "Frameworks & Backend": [
            "fastapi", "django", "flask", "react", "vue", "angular", "node.js", "nodejs", "next.js",
            "express", "spring boot", "asp.net", "dotnet", "laravel", "ruby on rails", "graphql", "rest api"
        ],
        "Machine Learning & AI": [
            "machine learning", "deep learning", "nlp", "natural language processing", "computer vision",
            "tensorflow", "pytorch", "scikit-learn", "keras", "pandas", "numpy", "opencv", "llm",
            "transformers", "huggingface", "bert", "langchain", "xgboost", "data analysis", "data science"
        ],
        "Cloud & DevOps": [
            "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes",
            "terraform", "ci/cd", "github actions", "jenkins", "ansible", "linux", "nginx", "helm", "serverless"
        ],
        "Databases & Storage": [
            "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis", "elasticsearch",
            "dynamodb", "cassandra", "oracle", "mariadb", "snowflake", "bigquery"
        ],
        "Engineering & Practices": [
            "agile", "scrum", "microservices", "system design", "git", "github", "gitlab",
            "jira", "unit testing", "pytest", "test automation", "design patterns", "ci/cd pipelines"
        ]
    }

    ROLE_PROFILES = {
        "Senior Python / Backend Engineer": ["python", "fastapi", "django", "sql", "postgresql", "docker", "rest api", "microservices", "git", "linux"],
        "Machine Learning & AI Specialist": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "nlp", "pandas", "numpy", "scikit-learn"],
        "Full-Stack Web Developer": ["javascript", "typescript", "react", "node.js", "html", "css", "sql", "rest api", "git", "python"],
        "DevOps & Cloud Infrastructure Engineer": ["aws", "azure", "docker", "kubernetes", "terraform", "ci/cd", "linux", "jenkins", "ansible", "bash"],
        "Data Scientist / Analytics Engineer": ["python", "r", "sql", "pandas", "numpy", "data analysis", "data science", "tableau", "postgresql"]
    }

    def analyze(self, text: str, filename: str = "") -> Dict[str, Any]:
        """Runs candidate information extraction and job matching."""
        if not text:
            return {"is_resume": False}

        lower_text = text.lower()
        
        # 1. Candidate Contact Information
        contact_info = self._extract_contact_info(text)
        
        # 2. Extract Categorized Skills
        extracted_skills, all_found_terms = self._extract_skills(lower_text)
        
        # 3. Extract Education History
        education = self._extract_education(text)
        
        # 4. Extract Experience & Seniority
        experience_info = self._extract_experience(text)
        
        # 5. Role Match Scoring
        role_matches = self._compute_role_matches(all_found_terms, experience_info.get("estimated_years", 1))

        # Check if document looks like a resume
        resume_indicators = ["experience", "education", "skills", "resume", "curriculum vitae", "projects", "employment", "summary", "objective"]
        indicator_count = sum(1 for ind in resume_indicators if ind in lower_text)
        is_resume = indicator_count >= 2 or "resume" in filename.lower() or "cv" in filename.lower()

        return {
            "is_resume": is_resume,
            "candidate_profile": contact_info,
            "skills_matrix": extracted_skills,
            "total_skills_count": sum(len(items) for items in extracted_skills.values()),
            "education": education,
            "experience_summary": experience_info,
            "role_matches": role_matches,
            "top_recommended_role": role_matches[0]["role"] if role_matches else "Software Engineer",
            "top_match_score": role_matches[0]["match_score"] if role_matches else 75
        }

    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extracts email, phone, links, and estimated name."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        candidate_name = lines[0] if lines else "Candidate"
        if len(candidate_name) > 40 or "@" in candidate_name or ":" in candidate_name or "/" in candidate_name:
            candidate_name = "Candidate Profile"

        # Email Regex
        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        email = email_match.group(0) if email_match else None

        # Phone Regex
        phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        phone = phone_match.group(0) if phone_match else None

        # LinkedIn & GitHub
        linkedin_match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[\w-]+", text, re.IGNORECASE)
        linkedin = linkedin_match.group(0) if linkedin_match else None

        github_match = re.search(r"(https?://)?(www\.)?github\.com/[\w-]+", text, re.IGNORECASE)
        github = github_match.group(0) if github_match else None

        return {
            "name": candidate_name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github
        }

    def _extract_skills(self, lower_text: str) -> Tuple[Dict[str, List[str]], set]:
        """Matches skills against domain ontology categories."""
        categorized = {}
        all_found = set()

        for category, terms in self.SKILL_TAXONOMY.items():
            found_in_category = []
            for term in terms:
                pattern = r"\b" + re.escape(term) + r"\b"
                if re.search(pattern, lower_text):
                    found_in_category.append(term.title() if len(term) > 3 else term.upper())
                    all_found.add(term)
            if found_in_category:
                categorized[category] = found_in_category

        return categorized, all_found

    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extracts degrees, majors, and universities."""
        results = []
        edu_keywords = ["bachelor", "master", "ph.d", "b.s.", "m.s.", "b.tech", "m.tech", "b.e.", "university", "institute", "college", "degree"]
        
        for line in text.splitlines():
            line_str = line.strip()
            if any(k in line_str.lower() for k in edu_keywords) and len(line_str) < 120 and len(line_str) > 10:
                results.append({"credential": line_str})
                if len(results) >= 4:
                    break
                    
        return results if results else [{"credential": "Higher Education in Engineering / Computer Science"}]

    def _extract_experience(self, text: str) -> Dict[str, Any]:
        """Calculates estimated years of experience and seniority rating."""
        year_matches = re.findall(r"\b(20\d{2}|19\d{2})\b", text)
        years = sorted([int(y) for y in year_matches if 1990 <= int(y) <= 2030])
        
        exp_years = 1
        if len(years) >= 2:
            span = max(years) - min(years)
            exp_years = max(1, min(span, 25))
        
        explicit_match = re.search(r"(\d+)\+?\s+years?\s+(of\s+)?experience", text, re.IGNORECASE)
        if explicit_match:
            try:
                exp_years = max(exp_years, int(explicit_match.group(1)))
            except Exception:
                pass

        if exp_years >= 7:
            seniority = "Lead / Principal Engineer"
            badge_color = "#991b1b"
        elif exp_years >= 4:
            seniority = "Senior Engineer"
            badge_color = "#dc2626"
        elif exp_years >= 2:
            seniority = "Mid-Level Engineer"
            badge_color = "#ea580c"
        else:
            seniority = "Junior / Associate Engineer"
            badge_color = "#f97316"

        return {
            "estimated_years": exp_years,
            "seniority_level": seniority,
            "badge_color": badge_color
        }

    def _compute_role_matches(self, found_skills: set, exp_years: int) -> List[Dict[str, Any]]:
        """Calculates fit percentage for top industry job profiles."""
        matches = []
        for role, required_skills in self.ROLE_PROFILES.items():
            matched_count = sum(1 for req in required_skills if req in found_skills)
            base_score = (matched_count / max(1, len(required_skills))) * 80
            exp_boost = min(20, exp_years * 2.5)
            final_score = min(98, round(base_score + exp_boost))
            
            matched_list = [req.title() for req in required_skills if req in found_skills]
            missing_list = [req.title() for req in required_skills if req not in found_skills][:3]
            
            matches.append({
                "role": role,
                "match_score": max(55, final_score),
                "matched_skills": matched_list,
                "growth_skills": missing_list
            })

        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches

    @classmethod
    def analyze_candidate_resume(cls, text: str, filename: str = "") -> Dict[str, Any]:
        """Convenience classmethod for candidate resume analysis."""
        return cls().analyze(text, filename)

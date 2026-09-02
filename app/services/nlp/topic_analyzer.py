"""
Topic Analysis and Discovery Engine.
Groups co-occurring terms into distinct thematic topics with distribution weights.
"""
import math
from typing import List, Dict, Any, Set
from collections import defaultdict
from app.services.nlp.text_preprocessor import TextPreprocessor

class TopicAnalyzer:
    """Local clustering-based topic modeler discovering latent themes in document text."""

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def analyze(self, text: str, max_topics: int = 4) -> List[Dict[str, Any]]:
        """Analyze document text and generate top thematic clusters."""
        sentences = self.preprocessor.split_sentences(text)
        tokens = self.preprocessor.tokenize_words(text, remove_stopwords=True)
        
        if len(tokens) < 15:
            return [{
                "name": "General Content",
                "score": 1.0,
                "top_terms": list(set(tokens))[:5]
            }]
        
        # Compute sentence-level term co-occurrences
        term_freq: Dict[str, int] = defaultdict(int)
        co_occur: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        
        for s in sentences:
            s_tokens = list(set(self.preprocessor.tokenize_words(s, remove_stopwords=True)))
            for i in range(len(s_tokens)):
                w1 = s_tokens[i]
                term_freq[w1] += 1
                for j in range(i + 1, len(s_tokens)):
                    w2 = s_tokens[j]
                    co_occur[w1][w2] += 1
                    co_occur[w2][w1] += 1
        
        # Select top seed terms with highest frequencies
        sorted_seeds = sorted([t for t in term_freq if len(t) > 2], key=lambda x: term_freq[x], reverse=True)[:max_topics * 3]
        
        topics: List[Dict[str, Any]] = []
        used_terms: Set[str] = set()
        
        for seed in sorted_seeds:
            if seed in used_terms:
                continue
            
            # Find closest co-occurring neighbors
            neighbors = sorted(co_occur[seed].items(), key=lambda x: x[1], reverse=True)
            topic_terms = [seed]
            used_terms.add(seed)
            
            for n_term, count in neighbors:
                if n_term not in used_terms and len(n_term) > 2:
                    topic_terms.append(n_term)
                    used_terms.add(n_term)
                if len(topic_terms) >= 5:
                    break
            
            # Compute topic score
            topic_score = sum(term_freq.get(t, 1) for t in topic_terms)
            topic_name = f"{seed.capitalize()} & {topic_terms[1].capitalize()}" if len(topic_terms) > 1 else seed.capitalize()
            
            topics.append({
                "name": topic_name,
                "raw_score": topic_score,
                "top_terms": topic_terms
            })
            
            if len(topics) >= max_topics:
                break
                
        if not topics:
            return [{
                "name": "Primary Document Theme",
                "score": 1.0,
                "top_terms": tokens[:5]
            }]
        
        # Normalize scores to sum to 1.0
        total_raw = sum(t["raw_score"] for t in topics) or 1.0
        formatted_topics = []
        for t in topics:
            formatted_topics.append({
                "name": t["name"],
                "score": round(t["raw_score"] / total_raw, 4),
                "top_terms": t["top_terms"]
            })
            
        return formatted_topics

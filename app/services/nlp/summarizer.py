"""
Extractive Summarization Engine.
"""
import math
from typing import List, Dict, Any, Set
from collections import defaultdict
from app.services.nlp.text_preprocessor import TextPreprocessor

class ExtractiveSummarizer:
    """Graph-based sentence centrality summarizer for high-fidelity extractive summaries."""

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def summarize(self, text: str, sentence_count: int = 4) -> Dict[str, Any]:
        sentences = self.preprocessor.split_sentences(text)
        if not sentences:
            return {
                "summary": "Document content is empty or contains insufficient text.",
                "sentences": [],
                "key_points": []
            }
        
        if len(sentences) <= sentence_count:
            return {
                "summary": " ".join(sentences),
                "sentences": [{"index": i, "text": s, "score": 1.0} for i, s in enumerate(sentences)],
                "key_points": sentences
            }
        
        sentence_tokens = [self.preprocessor.tokenize_words(s, remove_stopwords=True) for s in sentences]
        
        df: Dict[str, int] = defaultdict(int)
        for tokens in sentence_tokens:
            for t in set(tokens):
                df[t] += 1
        
        total_docs = len(sentences)
        n = len(sentences)
        matrix: List[List[float]] = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            tokens_i = sentence_tokens[i]
            if not tokens_i:
                continue
            tf_i = defaultdict(int)
            for t in tokens_i:
                tf_i[t] += 1
            
            vec_i = {t: tf_i[t] * math.log(1.0 + total_docs / (1.0 + df[t])) for t in tf_i}
            norm_i = math.sqrt(sum(v * v for v in vec_i.values()))
            if norm_i == 0:
                continue
                
            for j in range(i + 1, n):
                tokens_j = sentence_tokens[j]
                if not tokens_j:
                    continue
                tf_j = defaultdict(int)
                for t in tokens_j:
                    tf_j[t] += 1
                
                vec_j = {t: tf_j[t] * math.log(1.0 + total_docs / (1.0 + df[t])) for t in tf_j}
                norm_j = math.sqrt(sum(v * v for v in vec_j.values()))
                if norm_j == 0:
                    continue
                
                common_terms = set(vec_i.keys()).intersection(vec_j.keys())
                dot_product = sum(vec_i[t] * vec_j[t] for t in common_terms)
                sim = dot_product / (norm_i * norm_j)
                
                matrix[i][j] = sim
                matrix[j][i] = sim
        
        ranks = [1.0] * n
        damping = 0.85
        for _ in range(25):
            new_ranks = [0.0] * n
            for i in range(n):
                rank_sum = 0.0
                for j in range(n):
                    if i != j:
                        row_sum = sum(matrix[j])
                        if row_sum > 0:
                            rank_sum += matrix[j][i] * ranks[j] / row_sum
                pos_bias = 1.0 + (1.0 / (1.0 + i * 0.5))
                new_ranks[i] = ((1 - damping) + damping * rank_sum) * pos_bias
            ranks = new_ranks
        
        ranked_indices = sorted(range(n), key=lambda i: ranks[i], reverse=True)
        top_indices = sorted(ranked_indices[:sentence_count])
        
        max_score = max(ranks) if ranks else 1.0
        selected_sentences = [sentences[i] for i in top_indices]
        summary_paragraph = " ".join(selected_sentences)
        
        ranked_items = [
            {
                "index": i,
                "text": sentences[i],
                "score": round(ranks[i] / max_score, 4)
            }
            for i in top_indices
        ]
        
        key_points = [sentences[i] for i in ranked_indices[:min(5, len(sentences))]]
        
        return {
            "summary": summary_paragraph,
            "sentences": ranked_items,
            "key_points": key_points
        }

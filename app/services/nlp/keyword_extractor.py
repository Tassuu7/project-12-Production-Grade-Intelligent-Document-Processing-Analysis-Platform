"""
Keyword and Keyphrase Extraction Engine.
Uses TF-IDF local scoring and TextRank Co-occurrence Graph Centrality
to extract meaningful single words and bi-gram phrases.
"""
import math
import re
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
from app.services.nlp.text_preprocessor import TextPreprocessor

class KeywordExtractor:
    """Extracts explainable keywords and keyphrases from text."""

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def extract(self, text: str, top_k: int = 15) -> List[Dict[str, Any]]:
        """Extract ranked keywords and keyphrases with relevance scores and frequencies."""
        tokens = self.preprocessor.tokenize_words(text, remove_stopwords=True)
        if not tokens:
            return []
        
        # 1. Term Frequency calculation
        tf: Dict[str, int] = defaultdict(int)
        for t in tokens:
            tf[t] += 1
        
        total_tokens = len(tokens)
        
        # 2. Build Co-occurrence Graph for TextRank (Window size = 4)
        graph: Dict[str, Set[str]] = defaultdict(set)
        window_size = 4
        for i in range(len(tokens)):
            w1 = tokens[i]
            for j in range(i + 1, min(i + window_size, len(tokens))):
                w2 = tokens[j]
                if w1 != w2:
                    graph[w1].add(w2)
                    graph[w2].add(w1)
        
        # 3. Compute PageRank iterations over graph
        ranks: Dict[str, float] = {node: 1.0 for node in graph}
        damping = 0.85
        iterations = 20
        
        for _ in range(iterations):
            new_ranks: Dict[str, float] = {}
            for node in graph:
                rank_sum = sum(ranks[neighbor] / len(graph[neighbor]) for neighbor in graph[node] if len(graph[neighbor]) > 0)
                new_ranks[node] = (1 - damping) + damping * rank_sum
            ranks = new_ranks
        
        # Combine TF and TextRank scores
        scored_terms: List[Tuple[str, float, int]] = []
        for term, freq in tf.items():
            if len(term) <= 2:
                continue
            tr_score = ranks.get(term, 0.5)
            # Composite score: TextRank centrality * log(1 + freq)
            score = tr_score * math.log(1.0 + freq)
            scored_terms.append((term, score, freq))
        
        # Extract bigram phrases that occur >= 2 times
        bigrams = self.preprocessor.generate_ngrams(tokens, n=2)
        bigram_tf = defaultdict(int)
        for bg in bigrams:
            bigram_tf[bg] += 1
            
        for bg, freq in bigram_tf.items():
            if freq >= 2:
                w1, w2 = bg.split()
                bg_score = (ranks.get(w1, 0.5) + ranks.get(w2, 0.5)) * math.log(1.0 + freq) * 1.2
                scored_terms.append((bg, bg_score, freq))
        
        # Sort descending
        scored_terms.sort(key=lambda x: x[1], reverse=True)
        
        # Normalize top score to 1.0 scale
        max_score = scored_terms[0][1] if scored_terms else 1.0
        
        results: List[Dict[str, Any]] = []
        seen = set()
        for term, raw_score, freq in scored_terms:
            if term not in seen:
                seen.add(term)
                norm_score = round(min(1.0, raw_score / max_score), 4)
                results.append({
                    "term": term,
                    "score": norm_score,
                    "frequency": freq
                })
            if len(results) >= top_k:
                break
                
        return results

"""
Pure-Python Multinomial Naive Bayes Classifier Engine.
"""
import math
from typing import Dict, List, Tuple
from collections import defaultdict

class MultinomialNaiveBayesClassifier:
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.class_priors: Dict[str, float] = {}
        self.word_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.class_total_words: Dict[str, int] = defaultdict(int)
        self.vocabulary: set = set()
        self.total_documents: int = 0
        self.class_doc_counts: Dict[str, int] = defaultdict(int)

    def train(self, documents: List[Tuple[str, List[str]]]) -> None:
        self.total_documents = len(documents)
        for category, tokens in documents:
            self.class_doc_counts[category] += 1
            for t in tokens:
                self.word_counts[category][t] += 1
                self.class_total_words[category] += 1
                self.vocabulary.add(t)

        for cat, count in self.class_doc_counts.items():
            self.class_priors[cat] = math.log(count / self.total_documents)

    def predict(self, tokens: List[str]) -> Tuple[str, float]:
        if not self.class_priors:
            return "Other", 0.0

        vocab_size = max(1, len(self.vocabulary))
        scores: Dict[str, float] = {}

        for category, log_prior in self.class_priors.items():
            score = log_prior
            denom = self.class_total_words[category] + self.alpha * vocab_size
            for t in tokens:
                if t in self.vocabulary:
                    count = self.word_counts[category].get(t, 0)
                    prob = (count + self.alpha) / denom
                    score += math.log(prob)
            scores[category] = score

        max_log = max(scores.values())
        exp_scores = {c: math.exp(s - max_log) for c, s in scores.items()}
        total_exp = sum(exp_scores.values())
        probs = {c: exp_scores[c] / total_exp for c in exp_scores}

        best_cat = max(probs, key=probs.get)
        return best_cat, probs[best_cat]

"""
Document Similarity Engine.
Calculates TF-IDF Vector Space Model and Cosine Similarity Matrix
between documents with strict tenant isolation.
"""
import math
import json
import logging
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.analysis_result import AnalysisResult
from app.models.document_similarity import DocumentSimilarity
from app.services.nlp.text_preprocessor import TextPreprocessor

logger = logging.getLogger("app.services.nlp.similarity")

class DocumentSimilarityEngine:
    """Calculates cosine similarity matrices across documents belonging to a single user."""

    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def update_user_similarities(self, db: Session, user_id: int, min_threshold: float = 0.12) -> None:
        """Recalculate pairwise document similarities for all completed documents of user."""
        try:
            # Query all completed documents with analysis results for this user
            docs = (
                db.query(Document)
                .join(AnalysisResult, Document.id == AnalysisResult.document_id)
                .filter(Document.user_id == user_id, Document.status == "completed", Document.is_deleted == False)
                .all()
            )
            
            if len(docs) < 2:
                return
            
            # Extract tokenized texts
            doc_ids = [d.id for d in docs]
            corpus = []
            for d in docs:
                txt = d.analysis_result.extracted_text if d.analysis_result else ""
                corpus.append(self.preprocessor.tokenize_words(txt, remove_stopwords=True))
            
            # Compute Document Frequencies across corpus
            df: Dict[str, int] = {}
            for doc_tokens in corpus:
                for term in set(doc_tokens):
                    df[term] = df.get(term, 0) + 1
            
            total_docs = len(corpus)
            
            # Compute TF-IDF vectors
            tfidf_vectors: List[Dict[str, float]] = []
            norms: List[float] = []
            
            for doc_tokens in corpus:
                tf: Dict[str, int] = {}
                for t in doc_tokens:
                    tf[t] = tf.get(t, 0) + 1
                
                vec: Dict[str, float] = {}
                total_t = len(doc_tokens) or 1
                for t, count in tf.items():
                    idf = math.log((1.0 + total_docs) / (1.0 + df.get(t, 1))) + 1.0
                    vec[t] = (count / total_t) * idf
                
                norm = math.sqrt(sum(v * v for v in vec.values()))
                tfidf_vectors.append(vec)
                norms.append(norm if norm > 0 else 1.0)
            
            # Clear old similarities for this user
            db.query(DocumentSimilarity).filter(DocumentSimilarity.user_id == user_id).delete()
            db.commit()
            
            # Compute pairwise cosine similarities
            new_similarities: List[DocumentSimilarity] = []
            for i in range(len(docs)):
                for j in range(i + 1, len(docs)):
                    vec_i = tfidf_vectors[i]
                    vec_j = tfidf_vectors[j]
                    
                    shared_keys = set(vec_i.keys()).intersection(vec_j.keys())
                    dot_product = sum(vec_i[k] * vec_j[k] for k in shared_keys)
                    cosine_sim = dot_product / (norms[i] * norms[j])
                    
                    if cosine_sim >= min_threshold:
                        # Top 5 shared vocabulary terms
                        shared_ranked = sorted(
                            list(shared_keys),
                            key=lambda k: vec_i[k] * vec_j[k],
                            reverse=True
                        )[:5]
                        
                        # Add bidirectional similarity records
                        new_similarities.append(DocumentSimilarity(
                            user_id=user_id,
                            source_document_id=doc_ids[i],
                            target_document_id=doc_ids[j],
                            similarity_score=round(cosine_sim, 4),
                            shared_terms_json=json.dumps(shared_ranked),
                            calculation_method="TFIDF_COSINE"
                        ))
                        new_similarities.append(DocumentSimilarity(
                            user_id=user_id,
                            source_document_id=doc_ids[j],
                            target_document_id=doc_ids[i],
                            similarity_score=round(cosine_sim, 4),
                            shared_terms_json=json.dumps(shared_ranked),
                            calculation_method="TFIDF_COSINE"
                        ))
            
            if new_similarities:
                db.bulk_save_objects(new_similarities)
                db.commit()
                logger.info(f"Updated {len(new_similarities)} similarity links for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error updating similarities for user {user_id}: {str(e)}")
            db.rollback()

"""
Document Processing Task Runner.
Orchestrates content extraction, ML classification, NLP keywords/topics/summary,
similarity analysis, anomaly detection, and database status persistence.
"""
import time
import json
import logging
from datetime import datetime, timezone
from app.core.database import SessionLocal
from app.models.document import Document
from app.models.processing_job import ProcessingJob
from app.models.analysis_result import AnalysisResult
from app.services.extractors.extractor_factory import DocumentExtractorFactory

logger = logging.getLogger("app.services.queue.task_runner")

def execute_processing_job(job_id: int, document_id: int, user_id: int) -> None:
    """Execute full end-to-end processing pipeline for a single document."""
    db = SessionLocal()
    start_time = time.perf_counter()
    
    try:
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        doc = db.query(Document).filter(Document.id == document_id).first()
        
        if not doc or not job:
            logger.error(f"Job {job_id} or Document {document_id} not found in database.")
            return

        # Update Job & Document status to RUNNING / PROCESSING
        job.status = "RUNNING"
        job.started_at = datetime.now(timezone.utc)
        job.attempts += 1
        doc.status = "processing"
        db.commit()

        # Step 1: Content Extraction
        extractor = DocumentExtractorFactory.get_extractor(doc.file_type)
        extraction_result = extractor.extract(doc.file_path)

        # Step 2: NLP & ML Pipeline (local imports to avoid circular dependencies)
        from app.services.nlp.text_preprocessor import TextPreprocessor
        from app.services.nlp.classifier import DocumentClassifier
        from app.services.nlp.keyword_extractor import KeywordExtractor
        from app.services.nlp.topic_analyzer import TopicAnalyzer
        from app.services.nlp.summarizer import ExtractiveSummarizer
        from app.services.nlp.anomaly_detector import QualityAnomalyDetector
        from app.services.nlp.similarity_engine import DocumentSimilarityEngine

        # Preprocess text
        preprocessor = TextPreprocessor()
        cleaned_text = preprocessor.clean_text(extraction_result.raw_text)

        # Classification
        classifier = DocumentClassifier()
        clf_result = classifier.classify(cleaned_text, doc.original_filename)

        # Keywords Extraction
        kw_extractor = KeywordExtractor()
        keywords = kw_extractor.extract(cleaned_text)

        # Topic Modeling
        topic_analyzer = TopicAnalyzer()
        topics = topic_analyzer.analyze(cleaned_text)

        # Extractive Summarization
        summarizer = ExtractiveSummarizer()
        summary_res = summarizer.summarize(cleaned_text)

        # Quality & Anomaly Checks
        anomaly_detector = QualityAnomalyDetector()
        anomalies = anomaly_detector.analyze(doc, extraction_result, cleaned_text)

        # Persist Analysis Results
        existing_res = db.query(AnalysisResult).filter(AnalysisResult.document_id == doc.id).first()
        if existing_res:
            db.delete(existing_res)
            db.commit()

        tables_serialized = [t.model_dump() for t in extraction_result.tables]
        
        analysis = AnalysisResult(
            document_id=doc.id,
            extracted_text=extraction_result.raw_text,
            extracted_structure_json=json.dumps({"headings": extraction_result.structural_headings}),
            tables_data_json=json.dumps(tables_serialized),
            category_predicted=clf_result["predicted_category"],
            category_confidence=clf_result["confidence"],
            alternative_categories_json=json.dumps(clf_result["alternative_categories"]),
            classifier_version=clf_result["classifier_version"],
            keywords_json=json.dumps(keywords),
            topics_json=json.dumps(topics),
            summary_text=summary_res["summary"],
            summary_sentences_json=json.dumps(summary_res["sentences"]),
            key_points_json=json.dumps(summary_res["key_points"]),
            anomaly_findings_json=json.dumps(anomalies),
            tabular_stats_json=json.dumps(extraction_result.tabular_statistics) if extraction_result.tabular_statistics else None
        )
        db.add(analysis)

        # Update Document quantitative metrics
        duration_ms = (time.perf_counter() - start_time) * 1000
        doc.status = "completed"
        doc.page_count = extraction_result.page_count
        doc.word_count = extraction_result.word_count
        doc.character_count = extraction_result.character_count
        doc.line_count = extraction_result.line_count
        doc.table_count = extraction_result.table_count
        doc.processed_at = datetime.now(timezone.utc)
        doc.processing_duration_ms = duration_ms
        doc.error_message = None

        # Update Job Status
        job.status = "COMPLETED"
        job.completed_at = datetime.now(timezone.utc)
        job.duration_ms = duration_ms
        job.error_message = None
        db.commit()

        # Step 3: Recalculate Document Similarity Matrix for this user
        sim_engine = DocumentSimilarityEngine()
        sim_engine.update_user_similarities(db, user_id)

        logger.info(f"Successfully processed Document ID {doc.id} in {duration_ms:.2f}ms")

    except Exception as e:
        db.rollback()
        duration_ms = (time.perf_counter() - start_time) * 1000
        error_msg = str(e)
        logger.error(f"Error processing Document ID {document_id}: {error_msg}")
        
        try:
            job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
            doc = db.query(Document).filter(Document.id == document_id).first()
            if job:
                job.status = "FAILED"
                job.completed_at = datetime.now(timezone.utc)
                job.duration_ms = duration_ms
                job.error_message = error_msg
            if doc:
                doc.status = "failed"
                doc.error_message = error_msg
            db.commit()
        except Exception:
            pass
    finally:
        db.close()

"""Unit tests for Multinomial Naive Bayes."""
from app.services.nlp.naive_bayes_engine import MultinomialNaiveBayesClassifier

def test_naive_bayes_training_and_prediction():
    train_data = [
        ("Invoice", ["invoice", "tax", "subtotal", "due"]),
        ("Resume", ["education", "experience", "skills", "gpa"])
    ]
    clf = MultinomialNaiveBayesClassifier()
    clf.train(train_data)
    cat, prob = clf.predict(["invoice", "tax"])
    assert cat == "Invoice"
    assert prob > 0.5

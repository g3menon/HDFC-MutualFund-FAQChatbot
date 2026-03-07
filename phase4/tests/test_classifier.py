import pytest
from phase4.rag.query_classifier import QueryClassifier, QueryType

@pytest.fixture
def classifier():
    return QueryClassifier()

def test_classify_personal_info(classifier):
    assert classifier.classify("My PAN is ABCDE1234F", set()) == QueryType.REFUSE_PERSONAL

def test_classify_investment_advice(classifier):
    assert classifier.classify("Should I buy HDFC Pharma?", {"HDFC Pharma and Healthcare Fund"}) == QueryType.REFUSE_ADVICE

def test_classify_comparison(classifier):
    assert classifier.classify("Compare HDFC Pharma and HDFC Banking", {"HDFC Pharma and Healthcare Fund", "HDFC Banking & Financial Services Fund"}) == QueryType.REFUSE_COMPARISON

def test_classify_procedural(classifier):
    assert classifier.classify("How to download capital gains statement?", set()) == QueryType.PROCEDURAL

def test_classify_off_topic(classifier):
    assert classifier.classify("What is the capital of India?", set()) == QueryType.REFUSE_OFF_TOPIC

def test_classify_factual(classifier):
    assert classifier.classify("What is the expense ratio of HDFC Pharma?", {"HDFC Pharma and Healthcare Fund"}) == QueryType.FACTUAL

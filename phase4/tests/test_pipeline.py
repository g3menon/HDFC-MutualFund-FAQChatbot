import pytest
from unittest.mock import patch, MagicMock
from phase4.rag.pipeline import RAGPipeline
from phase4.rag.query_classifier import QueryType

@pytest.fixture
def mock_retriever():
    mock = MagicMock()
    mock.retrieve.return_value = [{"content": "Dummy chunk about HDFC Pharma expense ratio 0.95%.", "source_url": "https://example.com"}]
    return mock

@pytest.fixture
def mock_llm():
    mock = MagicMock()
    mock.generate_response.return_value = "The expense ratio is 0.95% (Source: https://example.com). Disclaimer: This information is for educational purposes only and should not be considered investment advice."
    return mock

@pytest.fixture
def pipeline(mock_retriever, mock_llm):
    p = RAGPipeline()
    p.retriever = mock_retriever
    p.llm = mock_llm
    return p

def test_pipeline_refuse_advice(pipeline):
    response = pipeline.generate_response("Should I buy HDFC Pharma?")
    assert "cannot provide investment advice" in response.lower()

def test_pipeline_refuse_comparison(pipeline):
    response = pipeline.generate_response("Compare HDFC Pharma and HDFC Banking")
    assert "one fund at a time" in response.lower()

def test_pipeline_refuse_personal(pipeline):
    response = pipeline.generate_response("My PAN is ABCDE1234F")
    assert "personal information" in response.lower()

def test_pipeline_valid_query(pipeline):
    response = pipeline.generate_response("What is the expense ratio of HDFC Pharma?")
    assert "expense ratio is 0.95%" in response.lower()
    

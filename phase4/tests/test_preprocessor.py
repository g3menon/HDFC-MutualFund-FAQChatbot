import pytest
from phase4.rag.query_preprocessor import QueryPreprocessor
from phase4.rag.config import SUPPORTED_FUNDS

@pytest.fixture
def preprocessor():
    return QueryPreprocessor()

def test_extract_funds_single(preprocessor):
    funds = preprocessor.extract_funds("What is the expense ratio of HDFC Pharma Fund?")
    assert len(funds) == 1
    assert "HDFC Pharma and Healthcare Fund" in funds

def test_extract_funds_multiple(preprocessor):
    funds = preprocessor.extract_funds("Compare HDFC Pharma and HDFC Banking")
    assert len(funds) == 2
    assert "HDFC Pharma and Healthcare Fund" in funds
    assert "HDFC Banking & Financial Services Fund" in funds

def test_extract_funds_none(preprocessor):
    funds = preprocessor.extract_funds("What is the weather today?")
    assert len(funds) == 0

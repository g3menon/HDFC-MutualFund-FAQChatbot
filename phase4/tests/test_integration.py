import pytest
from phase4.rag.pipeline import RAGPipeline

@pytest.mark.integration
def test_expense_ratio_hdfc_banking():
    """
    Test Phase 4 RAG Pipeline Integration with LLM and Vectorstore.
    This test ensures that a query about the expense ratio of HDFC Banking & Financial Services Fund
    returns the correct answer along with the source URL.
    """
    pipeline = RAGPipeline()
    query = "What is the Expense ratio of HDFC Banking & Financial Services Fund ?"
    
    response = pipeline.generate_response(query)
    
    # Assert that the response contains the correct expense ratio and URL
    assert "0.8" in response or "0.8%" in response, f"Expected expense ratio '0.8%' not found in response: {response}"
    assert "https://www.indmoney.com/mutual-funds/hdfc-banking-financial-services-fund-direct-growth-1006661" in response, f"Expected URL not found in response: {response}"

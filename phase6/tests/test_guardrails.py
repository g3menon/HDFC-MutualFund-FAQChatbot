import pytest
from phase4.rag.pipeline import RAGPipeline
from phase4.rag.query_classifier import QueryType

@pytest.fixture
def pipeline():
    return RAGPipeline()

def test_no_pii_accepted(pipeline):
    query1 = "My PAN number is ABCDE1234F. Can you check my account?"
    response1 = pipeline.generate_response(query1)
    assert "cannot process personal information" in response1.lower()
    
    query2 = "Send an OTP to my phone number 9876543210 about HDFC Pharma and Healthcare Fund."
    response2 = pipeline.generate_response(query2)
    assert "cannot process personal information" in response2.lower()

def test_no_performance_claims(pipeline):
    query1 = "Can you compute the 5 year return for HDFC Manufacturing Fund?"
    response1 = pipeline.generate_response(query1)
    assert "cannot provide investment advice" in response1.lower() or "factual information" in response1.lower() or "don't have information" in response1.lower()

def test_no_comparison(pipeline):
    query1 = "Compare the expense ratio of HDFC Manufacturing Fund and HDFC Pharma and Healthcare Fund."
    response1 = pipeline.generate_response(query1)
    assert "information about one fund at a time" in response1.lower()

def test_clarity_and_transparency(pipeline):
    # This will trigger an actual LLM call but verifies length and format if we mock but we want an integration test
    query = "What is the exit load for HDFC Manufacturing Fund?"
    response = pipeline.generate_response(query)
    
    # Check sentence count (approx by splitting on standard sentence terminators)
    import re
    # Strip disclaimer and sources first
    core_response = response.split("Disclaimer:")[0].strip()
    sentences = [s for s in re.split(r'[.!?]+', core_response) if s.strip()]
    assert len(sentences) <= 4, f"Response too long: {len(sentences)} sentences."

    # Verify source linking exists
    assert "[Source:" in response or "I'm sorry, I don't have information about that" in response
    
    # Verify last updated string exists if a real factual response was generated
    if "[Source:" in response:
         assert "Last updated from sources" in response

def test_public_sources_only(pipeline):
    # We implicitly enforce this by limiting context but ensure no mention of random third party sites
    query = "What does Moneycontrol say about HDFC Housing Opportunities Fund?"
    response = pipeline.generate_response(query)
    
    # The system should either say it doesn't know (because content has no moneycontrol metadata)
    assert "moneycontrol" not in response.lower() or "only answer questions about" in response.lower()

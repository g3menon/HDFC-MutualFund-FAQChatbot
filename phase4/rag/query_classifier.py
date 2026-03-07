from enum import Enum
from phase4.rag.config import SUPPORTED_FUNDS
import re

class QueryType(Enum):
    FACTUAL = "factual"
    PROCEDURAL = "procedural"
    GENERAL = "general"
    REFUSE_COMPARISON = "refuse_comparison"
    REFUSE_PERSONAL = "refuse_personal"
    REFUSE_ADVICE = "refuse_advice"
    REFUSE_OFF_TOPIC = "refuse_off_topic"

class QueryClassifier:
    """Classifies the query based on intent and constraints."""
    
    def __init__(self):
        self._personal_keywords = {"pan", "aadhaar", "email", "phone number", "bank account", "account number", "otp"}
        self._advice_keywords = {"buy", "sell", "invest", "recommend", "should i", "predict", "compute return"}
        self._procedural_keywords = {"how to", "download", "statement", "steps"}
        self._general_keywords = {"tell me about", "overview", "what is hdfc"}
        
    def classify(self, query: str, matched_funds: set[str]) -> QueryType:
        lower_query = query.lower()
        
        # Check constraints first
        
        # C3: No Personal Info
        if any(keyword in lower_query for keyword in self._personal_keywords):
            return QueryType.REFUSE_PERSONAL
            
        # C5: No Investment Advice
        if any(keyword in lower_query for keyword in self._advice_keywords):
            return QueryType.REFUSE_ADVICE
            
        # C4: No Comparisons
        if len(matched_funds) > 1 or "compare" in lower_query:
            return QueryType.REFUSE_COMPARISON
            
        # Out of Scope / Off Topic
        # If no funds matched and it's not a generic procedural question about hdfc/indmoney
        if not matched_funds:
            is_procedural_no_fund = any(kw in lower_query for kw in self._procedural_keywords) and "capital gains" in lower_query
            if not is_procedural_no_fund:
                 return QueryType.REFUSE_OFF_TOPIC

        # C1 / C2 procedural (e.g., How to download capital-gains statement?)
        if any(kw in lower_query for kw in self._procedural_keywords):
            return QueryType.PROCEDURAL
            
        # General overview
        if any(kw in lower_query for kw in self._general_keywords):
            return QueryType.GENERAL
            
        # Otherwise factual
        return QueryType.FACTUAL

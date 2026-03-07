import re
from typing import Optional, List, Set
from phase4.rag.config import SUPPORTED_FUNDS

class QueryPreprocessor:
    def __init__(self, supported_funds: List[str] = SUPPORTED_FUNDS):
        self.supported_funds = supported_funds

    def normalize(self, query: str) -> str:
        # Strip extra spaces and punctuation for simpler matching
        q = re.sub(r'[^\w\s]', '', query).lower()
        return q.strip()

    def extract_funds(self, query: str) -> Set[str]:
        norm_q = self.normalize(query)
        words = norm_q.split()
        
        matched_funds = set()
        
        # very simple mapping, assuming unique keywords for these 5 funds
        if "banking" in words or "financial" in words:
            matched_funds.add("HDFC Banking & Financial Services Fund")
        if "pharma" in words or "healthcare" in words:
            matched_funds.add("HDFC Pharma and Healthcare Fund")
        if "housing" in words or "opportunities" in words:
            matched_funds.add("HDFC Housing Opportunities Fund")
        if "manufacturing" in words:
            matched_funds.add("HDFC Manufacturing Fund")
        if "transportation" in words or "logistics" in words:
            matched_funds.add("HDFC Transportation and Logistics Fund")
            
        return matched_funds

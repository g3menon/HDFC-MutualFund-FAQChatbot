import logging
from typing import Optional, Dict, Any

from phase4.rag.query_preprocessor import QueryPreprocessor
from phase4.rag.query_classifier import QueryClassifier, QueryType
from phase4.rag.prompt_builder import PromptBuilder
from phase4.rag.llm_client import LLMClient
from phase4.rag.response_validator import ResponseValidator
from phase3.vectorstore.retriever import Retriever
from phase4.rag.config import SUPPORTED_FUNDS

logger = logging.getLogger("phase4")

class RAGPipeline:
    def __init__(self):
        self.preprocessor = QueryPreprocessor()
        self.classifier = QueryClassifier()
        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient()
        self.validator = ResponseValidator()

    def generate_response(self, user_query: str, chat_history: list = None) -> str:
        # Step 1: Extract matched funds
        matched_funds = self.preprocessor.extract_funds(user_query)
        
        # Context Retention: If no fund mentioned, check chat history
        if not matched_funds and chat_history:
            for msg in reversed(chat_history):
                if msg.get('role') == 'user':
                    historic_funds = self.preprocessor.extract_funds(msg.get('content', ''))
                    if historic_funds:
                        matched_funds = historic_funds
                        fund_name = list(historic_funds)[0]
                        user_query = f"{user_query} {fund_name}"
                        break

        # Step 2: Classify Query
        q_type = self.classifier.classify(user_query, matched_funds)
        
        # Step 3: Check early refusals
        if q_type == QueryType.REFUSE_COMPARISON:
            return "I'm sorry, I can only provide information about one fund at a time. Please ask about a specific fund."
        elif q_type == QueryType.REFUSE_PERSONAL:
            return "I'm sorry, I cannot process personal information. This chatbot only provides factual information about HDFC Mutual Fund schemes."
        elif q_type == QueryType.REFUSE_ADVICE:
            return "I cannot provide investment advice. Please consult a qualified financial advisor for investment decisions."
        elif q_type == QueryType.REFUSE_OFF_TOPIC:
            return "I appreciate your question, but I can only assist with queries about select HDFC Mutual Funds. Please ask about fund details like expense ratio, exit load, NAV, SIP amounts, or holdings."

        # Step 4: Map Fund name to ID
        fund_filter = None
        fund_id_map = {
            "HDFC Banking & Financial Services Fund": "hdfc_banking_financial_services",
            "HDFC Pharma and Healthcare Fund": "hdfc_pharma_healthcare",
            "HDFC Housing Opportunities Fund": "hdfc_housing_opportunities",
            "HDFC Manufacturing Fund": "hdfc_manufacturing",
            "HDFC Transportation and Logistics Fund": "hdfc_transportation_logistics"
        }
        
        if len(matched_funds) == 1:
            fund_name = list(matched_funds)[0]
            fund_filter = fund_id_map.get(fund_name)
            
        # Step 5: Retrieval
        # If it's a procedural question without a specific fund, don't filter by fund.
        if q_type == QueryType.PROCEDURAL and not fund_filter:
            retrieved_chunks = self.retriever.retrieve(user_query, top_k=3)
        else:
            retrieved_chunks = self.retriever.retrieve(user_query, top_k=3, fund_filter=fund_filter)

        fund_list_str = ", ".join(SUPPORTED_FUNDS)

        if not retrieved_chunks:
             return f"I'm sorry, I don't have information about that in my current data. I can only answer questions about the following HDFC Mutual Funds: {fund_list_str}. Please try rephrasing your question."

        # Step 6: Prompt construction
        prompt = self.prompt_builder.build_prompt(user_query, retrieved_chunks, chat_history)

        # Step 7: LLM inference
        raw_response = self.llm.generate_response(prompt)

        # Step 8: Response Validation & Formatting
        final_response = self.validator.validate_response(raw_response, retrieved_chunks)

        return final_response

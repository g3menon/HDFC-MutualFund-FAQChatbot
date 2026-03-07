import re

class ResponseValidator:
    def __init__(self):
        self.disclaimer = "Disclaimer: This information is for educational purposes only and should not be considered investment advice."

    def validate_response(self, response: str, retrieved_chunks: list[dict]) -> str:
        # Check disclaimer
        if "disclaimer: " not in response.lower():
            if not response.endswith("\n"):
                response += "\n\n"
            response += self.disclaimer
            
        # Check source URL
        if retrieved_chunks and "[source:" not in response.lower() and "http" in retrieved_chunks[0].get("source_url", ""):
            chunk = retrieved_chunks[0]
            fund_name = chunk.get("fund_name", "HDFC Mutual Fund")
            source_url = chunk.get("source_url", "")
            if source_url:
                if not response.endswith("\n"):
                    response += "\n\n"
                response += f"\n\n[Source: {fund_name}]({source_url})"
                
        # Append Data Freshness string if not present
        if retrieved_chunks and "last updated from sources:" not in response.lower():
            last_date = max([c.get("last_updated", "") for c in retrieved_chunks if c.get("last_updated")])
            if last_date:
                response += f"\n\nLast updated from sources: {last_date}"
                
        return response

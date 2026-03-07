import os
from datetime import datetime
from phase4.rag.config import SUPPORTED_FUNDS

class PromptBuilder:
    def __init__(self, prompt_template_path: str = "phase4/prompts/system_prompt.txt"):
        self.prompt_template_path = prompt_template_path
        with open(self.prompt_template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()

    def build_prompt(self, user_query: str, retrieved_chunks: list[dict], chat_history: list[dict] = None) -> str:
        # Format chunk context
        context_parts = []
        last_updated_set = set()
        
        for i, chunk in enumerate(retrieved_chunks):
            content = chunk.get("content", "")
            source_url = chunk.get("source_url", "Unknown Source")
            fund_name = chunk.get("fund_name", "Unknown")
            last_idx = chunk.get("last_updated", "")
            
            if last_idx:
                last_updated_set.add(last_idx)
                
            context_str = f"--- Chunk {i+1} ---\nFund: {fund_name}\nContent: {content}\nSource URL: {source_url}"
            context_parts.append(context_str)
            
        context_text = "\n\n".join(context_parts)
        
        if last_updated_set:
            last_updated = list(last_updated_set)[0]
        else:
            last_updated = datetime.now().strftime("%Y-%m-%d")

        fund_list = ", ".join(SUPPORTED_FUNDS)
        
        # Format chat history
        chat_text = "No previous context."
        if chat_history:
            history_parts = []
            for msg in chat_history:
                history_parts.append(f"{msg['role'].capitalize()}: {msg['content']}")
            chat_text = "\n".join(history_parts[-6:]) # keep last 3 turns
        
        prompt = self.template.format(
            chat_history=chat_text,
            retrieved_chunks=context_text,
            last_updated=last_updated,
            user_query=user_query,
            fund_list=fund_list,
            source_url="{source_url}"
        )
        return prompt

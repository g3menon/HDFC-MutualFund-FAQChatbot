import argparse
import sys
from phase4.rag.pipeline import RAGPipeline

def main():
    parser = argparse.ArgumentParser(description="Run RAG Pipeline Queries")
    parser.add_argument("query", type=str, nargs="?", help="Query to ask")
    args = parser.parse_args()

    pipeline = RAGPipeline()
    
    if args.query:
        print(f"\nUser Query: {args.query}")
        print("-" * 50)
        response = pipeline.generate_response(args.query)
        print(f"RAG Response:\n{response}")
        return

    print("HDFC Mutual Fund RAG Chatbot (Type 'exit' to quit)")
    print("-" * 50)
    while True:
        try:
            query = input("You: ")
            if query.lower() in ("exit", "quit", "q"):
                break
            
            response = pipeline.generate_response(query)
            print(f"\nBot: {response}\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()

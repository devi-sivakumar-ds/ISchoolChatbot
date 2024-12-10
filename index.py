import os
from rag.rag_system import RAGSystem

# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDhSrIRMh5ZpHuTYcR__FvnrV9fDj8txqE"

def main():
    
    rag = RAGSystem("data/processed")
    
    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        answer = rag.ask_question(question)
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    main()
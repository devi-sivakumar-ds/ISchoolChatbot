from flask import Flask, render_template, request
from rag.rag_system import RAGSystem

app = Flask(__name__)

# Initializing the RAG system
rag = RAGSystem("data/processed")

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None 
    if request.method == "POST":
        # Getting the question from the form
        question = request.form.get("question")
        if question:
            answer = rag.ask_question(question)
    
    # Rendering the template with the question and answer
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)

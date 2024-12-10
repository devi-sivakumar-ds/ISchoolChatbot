from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain.schema import Document
import os

# Set your Gemini API key here
os.environ["GOOGLE_API_KEY"] = ""

class RAGSystem:
    # Initializing the RAG system with pre-processed documents
    def __init__(self, processed_documents_path="data/processed"):
        self.processed_documents_path = processed_documents_path
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.documents = self._load_documents()
        self.vectorstore = self._create_vectorstore()
        self.rag_chain = self._create_rag_chain()

    # Function to load and split all documents from the processed documents
    def _load_documents(self):
        documents = []
        for file_name in os.listdir(self.processed_documents_path):
            file_path = os.path.join(self.processed_documents_path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Converting each file into a Document object
                documents.append(Document(page_content=content, metadata={"source": file_name}))
        return documents

    # Function to create a vector store for efficient document retrieval. The retriever object can be used for similarity-based search.
    def _create_vectorstore(self):
        vectorstore = Chroma.from_documents(documents=self.documents, embedding=self.embeddings)
        return vectorstore.as_retriever(search_kwargs={"k": 3})

    # Function to create a RAG chain for question answering
    def _create_rag_chain(self):
        system_prompt = """
        You are a knowledgeable assistant. Provide clear, concise answers based on the given context. 
        If the information is not in the context, state that the answer is unavailable. 
        Use a maximum of three sentences.

        Context:
        {context}
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        document_chain = create_stuff_documents_chain(llm=self.llm, prompt=prompt)
        return create_retrieval_chain(self.vectorstore, document_chain)

    # Function to query the system with a user question.
    def ask_question(self, question):
        response = self.rag_chain.invoke({"input": question})
        return response["answer"]

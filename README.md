# ISchoolChatbot
A chatbot for the I School website designed to assist prospective students by answering their questions about programs, admissions, and campus life, while also helping current students quickly locate information on resources, events, and support services.

# Project Structure
project/
│
├── crawlers/
│   └── web_crawler.py  # Crawls the web and saves data into text files
│
├── processors/
│   └── document_processor.py  # Processes the text 
│
├── rag/
│   └── rag_system.py  # Implements RAG and calls GenAI
│
├── data/
│   └── raw_text/  # Directory for raw text files from web crawling
│   └── processed/  # Directory for processed text
│
├── chatbot.py  # Main Flask application
│
├── index.py  # Logic for running in terminal
│
├── README.md 
│
└── requirements.txt  # Dependencies for the project


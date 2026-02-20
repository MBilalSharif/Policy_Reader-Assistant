📄 Document Assistant – RAG-Based PDF Question Answering System

An intelligent Retrieval-Augmented Generation (RAG) system that reads PDF documents and answers user queries based on their content.

This project allows users to upload a PDF and ask natural language questions. The system retrieves the most relevant sections from the document and generates accurate answers using an LLM.

🚀 Features

📥 Upload and process PDF documents

✂️ Smart text chunking with overlap

🔎 Semantic search using embeddings

🧠 Retrieval-Augmented Generation (RAG) pipeline

💬 Natural language question answering

⚡ Fast and context-aware responses

🏗️ Architecture Overview

PDF Loader – Extracts text from uploaded PDF

Text Chunking – Splits text into manageable chunks

Embedding Model – Converts text into vector representations

Vector Database – Stores embeddings for similarity search

Retriever – Finds top-K relevant chunks

LLM – Generates answer using retrieved context

🛠️ Tech Stack

Python

LangChain

Hugging Face 

ChromaDB

Streamlit 



⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/MBilalSharif/Policy_Reader-Assistant.git
cd Policy_Reader-Assistant
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Run the Application
python app.py

If using Streamlit:

streamlit run app.py
🧠 How It Works (RAG Flow)

User Query → Convert to Embedding → Retrieve Top-K Similar Chunks →
Send Context + Query to LLM → Generate Final Answer

📌 Example

User Question:

What is the company’s refund policy?

System Response:

The refund policy states that customers can request a refund within 30 days of purchase, provided the product is unused and in original condition.

📈 Future Improvements

Multi-PDF support

Chat history memory

Better UI design

Deployment on cloud (Render / Vercel )

Authentication system

🎯 Use Cases

Policy document assistants

Legal document Q&A

Research paper assistant

Company internal knowledge base

Educational document chatbot

👨‍💻 Author

Muhammad Bilal Sharif
AI/ML Enthusiast | RAG & Generative AI Developer

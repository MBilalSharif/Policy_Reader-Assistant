import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_output_tokens=2000,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

def get_prompt():
    return PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer only from the provided context.
        If the context is insufficient, just say I don't know the answer.

        {context}
        Question: {question}
        """,
        input_variables=['context', 'question']
    )
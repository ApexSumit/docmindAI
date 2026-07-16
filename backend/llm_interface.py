# backend/llm_interface.py (Cohere Version)
import cohere
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize Cohere (Make sure you have your COHERE_API_KEY in environment variables)
llm = ChatCohere(model="command-r-plus", temperature=0.2)

# --- 1. Q&A CHAIN ---
qa_template = """You are a strict legal assistant. 
Answer ONLY using the provided context. 
Cite every fact like this: (See Clause X, Page N).

Context: {context}
User Role: {user_role}
Question: {question}
Answer:"""
qa_prompt = ChatPromptTemplate.from_template(qa_template)
qa_chain = qa_prompt | llm | StrOutputParser()

# --- 2. SUMMARIZATION CHAIN ---
summary_template = """Summarize the context into 5 bullet points with citations.

Context: {context}
User Role: {user_role}
Summary:"""
summary_prompt = ChatPromptTemplate.from_template(summary_template)
summary_chain = summary_prompt | llm | StrOutputParser()

def generate_response(question, retrieved_chunks, mode="qa", user_role="Legal Professional"):
    context = ""
    for chunk in retrieved_chunks:
        context += f"[Clause: {chunk['clause']} | Page: {chunk['page']}]\n{chunk['text']}\n\n"
    
    if mode == "qa":
        return qa_chain.invoke({"context": context, "question": question, "user_role": user_role})
    elif mode == "summary":
        return summary_chain.invoke({"context": context, "user_role": user_role})
    else:
        return "Invalid mode"
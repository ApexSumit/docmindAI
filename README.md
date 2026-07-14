# 📄 DocMind AI - Legal Document & Lengthy Document Reader Bot

> **An AI assistant that reads, summarizes, and answers questions from long legal contracts, agreements, and policy documents with precise source page and clause citations.**

---

## 📌 Table of Contents
- [Overview](#overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Outcomes](#-project-outcomes)
- [Installation & Setup](#-installation--setup)
- [How to Use](#-how-to-use)
- [Project Structure](#-project-structure)
- [Team](#-team)
- [License](#-license)

---

## 📖 Overview

**DocMind AI** is a Streamlit-based web application that processes lengthy legal PDFs (100+ pages). It uses **Retrieval-Augmented Generation (RAG)** to extract, chunk, and index legal clauses, enabling users to:

- Ask specific contract-related questions.
- Generate executive summaries of the entire document.

**Crucially, every answer and summary is backed by direct citations**—including the **exact clause number and page number**—making it reliable and auditable for legal professionals.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **📑 Long Document Processing** | Handles 100+ page legal PDFs using PyMuPDF and pdfplumber. |
| **⚖️ Legal Text Chunking** | Splits documents by legal sections (e.g., "Section 4.2", "ARTICLE 3") and preserves clause metadata. |
| **🔍 Contract Q&A** | Ask natural language questions (e.g., *"What is the termination penalty?"*) and get precise answers. |
| **📝 Summary Generation** | Generate an executive summary of the entire document in seconds. |
| **📎 Source Page Citation** | Every answer includes *"(See Clause X, Page N)"* for full transparency. |
| **🔒 100% Private & Local** | Runs entirely on your machine using Ollama (Mistral) and ChromaDB. No data leaves your computer. |

---

## 🧠 System Architecture

The following diagram illustrates the complete data flow of DocMind AI:

```mermaid
flowchart TD
    A[User Uploads Legal PDF (100+ pages)] --> B[PyMuPDF / pdfplumber]
    B --> C[Page-aware Text Extraction]
    C --> D[Clause/Section Chunker]
    D --> E[Adds page_num + clause metadata tags]
    E --> F[ChromaDB Vector Database]
    
    G[User Query / "Generate Summary"] --> H[Retrieve Top-k Clauses]
    F --> H
    H --> I[Ollama - Mistral 7B]
    I --> J[Answer + 'See Clause X, Page N']
    J --> K[Display to User]

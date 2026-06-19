```markdown
# 🩺 FAIR-RAG Medical AI System

A professional Medical AI Assistant designed to provide reliable health-related information by analyzing medical guidelines (WHO, ICMR, DGHS) using Retrieval-Augmented Generation (RAG) technology.

## 🚀 Key Features

*   **Retrieval Augmented Generation (RAG):** Extracts precise information from medical documents and guidelines to answer user queries accurately.
*   **Translation Sandwich:** A seamless pipeline that translates Bengali queries to English, processes them through the RAG system, and provides the final response in Bengali.
*   **Keyword Injection:** Automatically enhances general user queries with professional clinical terminology to improve retrieval relevance.
*   **Professional UI:** A modern, gradient-themed dashboard built with Streamlit for a user-friendly experience.
*   **Safety First:** Includes built-in AI disclaimers and authoritative source tracking to ensure responsible AI usage.

## 🛠 Tech Stack

*   **Frontend:** Streamlit
*   **AI Engine:** Groq (Llama 3.1-8b-instant)
*   **Vector Database:** ChromaDB
*   **Embeddings:** HuggingFace (all-MiniLM-L6-v2)
*   **Orchestration:** LangChain

## 🏗 System Architecture

*   **Input:** User's natural language health query in Bengali.
*   **Processing:** Query translation $\rightarrow$ Clinical term injection $\rightarrow$ Vector search.
*   **Retrieval:** Context fetching from the Chroma vector database.
*   **Generation:** Context-aware response generation by the LLM.
*   **Output:** Bengali-translated professional medical response.

## 📋 Setup & Installation

### Prerequisites
*   Python 3.9 or higher.
*   Groq API Key.

### Steps to Run
1. **Clone the repository:**
```bash
   git clone [https://github.com/mizanur-rahman-21/FAIR-RAG-Medical-Assistant.git](https://github.com/mizanur-rahman-21/FAIR-RAG-Medical-Assistant.git)
   cd FAIR-RAG-Medical-Assistant

```

2. **Set up virtual environment:**

```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate

```

3. **Install dependencies:**

```bash
   pip install -r requirements.txt

```

4. **Configure environment variables:**
Create a `.env` file in the root directory and add your API Key:

```text
   GROQ_API_KEY=your_actual_api_key_here

```

5. **Run the application:**

```bash
   streamlit run app.py

```

## 👨‍💻 Developer

**Mizanur Rahman**

*Undergraduate Student, Dept. of Industrial Engineering and Management (IEM)*

*Khulna University of Engineering & Technology (KUET)*

---

*⚠️ **Disclaimer:** This system is developed for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified physician with any questions regarding a medical condition.*

```

```

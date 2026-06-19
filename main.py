import os
import warnings
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.translator import MedicalTranslator
from src.keyword_injector import inject_clinical_terms

warnings.filterwarnings("ignore")
load_dotenv()

def main():
    print("=== FAIR-RAG: Keyword Injection Testing ===")
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    translator = MedicalTranslator()

    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.1-8b-instant", temperature=0.1)

    system_prompt = (
        "You are a medical assistant. Use the following retrieved context to answer. "
        "If you don't know, say 'I do not know'.\n\nContext: {context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    rag_chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))

    # ৩টি স্পেসিফিক প্রশ্ন যেখানে সাধারণ মানুষ লোকাল শব্দ ব্যবহার করে
    test_queries = [
        "আমার খুব বমি বমি ভাব এবং মাথা ব্যথা হচ্ছে, ম্যালেরিয়া হতে পারে?",
        "গর্ভাবস্থায় ম্যালেরিয়া হলে কি শ্বাসকষ্ট হয়?",
        "যাদের সুগার আছে তাদের কি ডেঙ্গু হলে বেশি ঝুঁকি?"
    ]

    print("\n[Testing] Baseline vs Keyword-Injection...\n")
    
    for i, bn_question in enumerate(test_queries, 1):
        print(f"প্রশ্ন {i}: {bn_question}")
        
        # Baseline Translation
        baseline_en = translator.translate_to_english(bn_question)
        print(f"[-] Baseline Query: {baseline_en}")
        
        # Keyword Injected Translation
        injected_en = inject_clinical_terms(bn_question, baseline_en)
        print(f"[+] Enhanced Query: {injected_en}")
        
        # RAG থেকে ইনজেক্ট করা প্রশ্নের উত্তর আনা
        response = rag_chain.invoke({"input": injected_en})
        bn_answer = translator.translate_to_bengali(response['answer'])
        
        print(f"[Final Answer]: {bn_answer}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()
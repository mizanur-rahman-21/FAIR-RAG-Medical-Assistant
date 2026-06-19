import streamlit as st
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

# এনভায়রনমেন্ট ও ওয়ার্নিং সেটআপ
warnings.filterwarnings("ignore")
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# পেজ কনফিগারেশন
st.set_page_config(page_title="Med-AI | Professional Assistant", layout="wide", page_icon="🩺")

# গর্জিয়াস ডিজাইনের জন্য কাস্টম CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%); }
    .title-box {
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }
    .identity-card {
        background-color: #ffffff;
        padding: 20px;
        border-left: 6px solid #1f77b4;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# সাইডবার: পরিচয় ও স্ট্যাটাস
with st.sidebar:
    st.markdown('<div class="identity-card">', unsafe_allow_html=True)
    st.markdown("### 👨‍💻 Developer Profile")
    st.write("**Name:** Mizanur Rahman")
    st.write("**University:** KUET")
    st.write("**Dept:** IEM")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("✅ System Status: Online")
    st.warning("⚠️ **ডিসক্লেইমার:** এটি একটি এআই মডেল। জরুরি প্রয়োজনে ডাক্তারের পরামর্শ নিন।")

# মেইন হেডার
st.markdown('<div class="title-box"><h1>🩺 FAIR-RAG Medical AI System</h1><p>নির্ভরযোগ্য মেডিকেল গাইডলাইন অ্যানালাইসিস প্ল্যাটফর্ম</p></div>', unsafe_allow_html=True)

# RAG আর্কিটেকচার ডায়াগ্রাম
st.subheader("System Workflow")


# সিস্টেম কম্পোনেন্ট লোড করা
@st.cache_resource
def load_system():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY পাওয়া যায়নি! অনুগ্রহ করে .env ফাইলটি চেক করুন।")
        st.stop()
        
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    translator = MedicalTranslator()
    llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.1-8b-instant", temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert medical assistant. Use the provided context to answer. If unsure, say 'I do not know'. \n\nContext: {context}"),
        ("human", "{input}"),
    ])
    
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))
    return translator, chain

translator, rag_chain = load_system()

# চ্যাট হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ইউজার ইনপুট ও প্রসেসিং
if user_input := st.chat_input("আপনার রোগের লক্ষণ বা স্বাস্থ্য জিজ্ঞাসা লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("মেডিকেল ডাটাবেস বিশ্লেষণ করা হচ্ছে..."):
            try:
                # অনুবাদ ও কি-ওয়ার্ড ইনজেকশন লজিক
                en_q = translator.translate_to_english(user_input)
                injected_q = inject_clinical_terms(user_input, en_q)
                
                # রিয়েল ডাটা ইনভোকেশন
                res = rag_chain.invoke({"input": injected_q})
                bn_ans = translator.translate_to_bengali(res['answer'])
                
                st.markdown(bn_ans)
                st.session_state.messages.append({"role": "assistant", "content": bn_ans})
                
                st.divider()
                st.caption("উৎস: WHO, ICMR, DGHS মেডিকেল গাইডলাইনস")
            except Exception as e:
                st.error(f"দুঃখিত, সিস্টেমটি সাময়িকভাবে সাড়া দিচ্ছে না: {e}")
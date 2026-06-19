import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_pdfs(pdf_dir="data/pdfs"):
    print("[1/4] PDF ingestion শুরু হচ্ছে...")
    all_chunks = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50
    )

    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
        print(f"ফোল্ডার {pdf_dir} তৈরি করা হয়েছে। এখানে PDF রাখো।")
        return []

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_dir, filename)
            loader = PyMuPDFLoader(filepath)
            docs = loader.load()
            
            chunks = text_splitter.split_documents(docs)
            print(f"Processing: {filename} -> {len(docs)} pages, {len(chunks)} chunks")
            all_chunks.extend(chunks)
            
    print(f"মোট chunks: {len(all_chunks)}")
    return all_chunks
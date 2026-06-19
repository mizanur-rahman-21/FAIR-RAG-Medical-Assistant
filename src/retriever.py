from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_vector_db(chunks, persist_directory="./chroma_db"):
    print("[2/4] Indexing ChromaDB...")
    
    if not chunks:
        print("কোনো ডাটা পাওয়া যায়নি!")
        return None

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # ChromaDB একবারে সব নিতে পারে না, তাই ৫০০০ করে ভাগ করে দিচ্ছি
    batch_size = 5000
    vector_db = None

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i : i + batch_size]
        print(f"ব্যাচ সেভ হচ্ছে... ({len(batch_chunks)} chunks)")

        if vector_db is None:
            # প্রথম ব্যাচ দিয়ে ডাটাবেস তৈরি
            vector_db = Chroma.from_documents(
                documents=batch_chunks,
                embedding=embeddings,
                persist_directory=persist_directory
            )
        else:
            # পরের ব্যাচগুলো আগের ডাটাবেসে যোগ করা
            vector_db.add_documents(batch_chunks)
    
    print(f"Database ready: {len(chunks)} chunks stored")
    return vector_db
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai

# =========
# Setup
# =========
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in your .env")

genai.configure(api_key=GEMINI_API_KEY)

class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """
    Minimal wrapper so Chroma can call Gemini embeddings automatically.
    """
    def __init__(self, model_name: str = "text-embedding-004"):
        self.model_name = model_name

    def __call__(self, texts):
        print(f"Embedding via Gemini... {texts}")
        if isinstance(texts, str):
            texts = [texts]

        vectors = []
        for t in texts:
            # Gemini returns either {'embedding': [...]} or {'embedding': {'values': [...]}} (version dependent)
            res = genai.embed_content(model=self.model_name, content=t)
            emb = res.get("embedding")
            if isinstance(emb, dict) and "values" in emb:
                emb = emb["values"]
            if not isinstance(emb, list):
                raise RuntimeError("Unexpected embedding response from Gemini")
            vectors.append(emb)
        print(f"Embedded {len(texts)} texts via Gemini.")
        return vectors

gemini_ef = GeminiEmbeddingFunction(model_name="text-embedding-004")
chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")

collection_name = "my_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    embedding_function=gemini_ef   # Chroma will call Gemini to embed docs & queries
)

#Loading documents
def load_documents_from_directory(directory_path):
    print("=== Loading documents from directory ===")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                documents.append({"id" : filename, "text": file.read()})
    return documents

def split_text(text, chunk_size=1000, overlap=20):
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# =========
# Load + chunk + upsert into Chroma (Gemini embeds automatically)
# =========
directory_path = "./my_data"
documents = load_documents_from_directory(directory_path)
print(f"Loaded {len(documents)} documents from {directory_path}")

#Function to split documents into chunks
chunked_documents = []
for doc in documents:
    chunks = split_text(doc["text"])
    for i, chunk in enumerate(chunks):
        chunked_documents.append({
            "id": f"{doc['id']}_chunk_{i}",
            "text": chunk
        })
print(f"Split documents into {len(chunked_documents)} chunks")

# Add to Chroma (no manual embedding step needed)
collection.add(
    ids=[c["id"] for c in chunked_documents],
    documents=[c["text"] for c in chunked_documents]
)
print("Indexed chunks into Chroma with Gemini embeddings.")

def rag_answer(question: str, top_k: int = 5, chat_model: str = "gemini-1.5-flash"):
    # 1) Retrieve
    hits = collection.query(query_texts=[question], n_results=top_k)
    docs = hits.get("documents", [[]])[0] if hits else []
    context = "\n\n".join(docs)

    # 2) Generate with Gemini
    prompt = (
        "You are a concise RAG assistant. Use ONLY the provided context. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )

    model = genai.GenerativeModel(chat_model)
    resp = model.generate_content(prompt)
    return resp.text

if __name__ == "__main__":
    print("RAG chat ready. Type 'exit' to quit.")
    try:
        while True:
            user_q = input("You: ").strip()
            if not user_q:
                continue
            if user_q.lower() in {"exit", "quit", "q"}:
                break
            answer = rag_answer(user_q)
            print(f"Assistant: {answer}")
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
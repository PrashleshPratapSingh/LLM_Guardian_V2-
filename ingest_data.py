import chromadb
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
from chromadb.utils import embedding_functions

print(" STARTING ENTERPRISE INGESTION...")

# 1. SETUP DATABASE
# We persist data to disk so we don't reload it every time
chroma_client = chromadb.PersistentClient(path="./chroma_db_storage")
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = chroma_client.get_or_create_collection(
    name="jailbreak_signatures",
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"}
)

# 2. DOWNLOAD REAL DATA
# We use a known dataset from HuggingFace that contains prompt injections
print(" Downloading Dataset (deepset/prompt-injections)...")
dataset = load_dataset("deepset/prompt-injections", split="train")

# Filter for the 'injection' label (1 = Attack, 0 = Safe)
attacks = [row['text'] for row in dataset if row['label'] == 1]
safe_prompts = [row['text'] for row in dataset if row['label'] == 0]

# Let's limit it to 500 attacks for speed (or remove [:500] for full power)
attacks = attacks[:1000] 
print(f"⚡ Found {len(attacks)} distinct attack patterns.")

# 3. INGEST INTO CHROMA
print(" Vectorizing and storing attacks... (This may take a moment)")

# We process in batches to be safe
batch_size = 50
for i in range(0, len(attacks), batch_size):
    batch = attacks[i:i+batch_size]
    ids = [f"attack_{i+j}" for j in range(len(batch))]
    
    collection.add(
        documents=batch,
        ids=ids,
        metadatas=[{"type": "jailbreak"} for _ in batch]
    )
    print(f"   Processed {i + len(batch)}/{len(attacks)}...")

print(f" SUCCESS! Database now contains {collection.count()} vectors.")
print("   Location: ./chroma_db_storage")
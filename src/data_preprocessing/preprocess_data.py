import sqlite3
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from src.core.summarization import summarize_movie_text
import json
import os
import argparse
from tqdm import tqdm
import config

# Argument Parser
parser = argparse.ArgumentParser(description="Preprocess movie data and build vector database.")
parser.add_argument('--vd', nargs='+', choices=['faiss', 'qdrant'], default=['faiss'], help='List of vector databases to build index for. Options: faiss, qdrant')
args = parser.parse_args()

# Database connection
conn = sqlite3.connect('data/processed/movies.db')

# Load data into pandas DataFrame
df = pd.read_sql_query("SELECT * FROM movies", conn)
conn.close()


# Text Consolidation
intermediate_file = 'data/processed/movies_processed_intermediate.json'
processed_data = {}
# Load intermediate data if it exists
if os.path.exists(intermediate_file):
    with open(intermediate_file, 'r') as f:
        processed_data = json.load(f)

combined_texts = []
# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    print(f"Processing index {index}/{len(df)}")

    # Skip if already processed
    if str(index) in processed_data:
        print(f"Skipping index {index} as it's already processed.")
        combined_texts.append(processed_data[str(index)])
        continue
    
    # Summarize movie text
    combined_text = summarize_movie_text(row)
    combined_texts.append(combined_text)
    processed_data[str(index)] = combined_text
    # Save to json file after each row with indentation
    with open(intermediate_file, 'w') as f:
        json.dump(processed_data, f, indent=4)

df = df[:len(combined_texts)]
df["generated_summary"] = combined_texts

# Generate Embeddings
print("Generating embeddings...")
model = SentenceTransformer(config.EMBEDDING_MODEL)
embeddings_list = []
# Iterate over each row in the DataFrame
for i, row in tqdm(df.iterrows(), total=len(df)):
    text = str(row["genres"]) + ". " + str(row["stars"]) + ". " + str(row["directors"]) + ". " + str(row["generated_summary"])

    embeddings_list.append(model.encode(text))

df["embeddings"] = embeddings_list

vector_databases = args.vd
print(f"Vector databases selected: {vector_databases}")

print("Building Vector Database...")

# Build FAISS index
if str(vector_databases[0]).lower() == 'faiss':
    # Build Vector Database
    embeddings = np.array(df["embeddings"].tolist()).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, "data/faiss_index.bin")
elif vector_databases.lower() == 'qdrant':
    pass
else:
    raise Exception("No existing vector database such as ", vector_databases)

# Save processed data (for now, saving to a new db)
conn_processed = sqlite3.connect('data/processed/movies_summaries.db')
df.to_sql("movies_summaries", conn_processed, if_exists="replace", index=False)
conn_processed.close()

print("Data preprocessing completed.")

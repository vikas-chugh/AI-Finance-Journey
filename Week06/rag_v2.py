"""
Project 3: RAG Regulatory Knowledge Assistant - Version 2

Description:
Introduces the document ingestion pipeline for a Retrieval-Augmented
Generation (RAG) system. A regulatory document is loaded from a text
file, split into overlapping character-based chunks, and enriched with
basic metadata for future embedding and retrieval.

Key Features:
- Load document from a text file.
- Character-based chunking with configurable chunk size and overlap.
- Basic metadata creation (chunk ID and source file).
- Foundation for embedding generation in later versions.

Learning Concepts:
- Document ingestion.
- Chunking.
- Chunk overlap.
- Metadata.
"""

"""
Loads the complete document from a text file and
returns it as a single string.
"""

def load_document(filename):

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    return text


"""
Splits a document into overlapping character-based chunks.

Each new chunk starts after (chunk_size - overlap) characters,
preserving context between adjacent chunks.
"""
def chunk_document(text, chunk_size=200, overlap=50):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


"""
Creates metadata records for every chunk.

Each record stores a unique chunk ID, the chunk text,
and the source document name.
"""
def create_chunk_records(chunks, source):

    records = []

    for index, chunk in enumerate(chunks):

        record = {
            "chunk_id": index,
            "text": chunk,
            "source": source
        }

        records.append(record)

    return records



import os

BASE_DIR = os.path.dirname(__file__)

regulations = os.path.join(BASE_DIR,"regulatory_rules.txt")

document = load_document(regulations)

chunks = chunk_document(
    document,
    chunk_size=200,
    overlap=50
)

records = create_chunk_records(
    chunks,
    "regulatory_rules.txt"
)


for record in records:

    print("----- CHUNK -----")
    print("ID:", record["chunk_id"])
    print("Source:", record["source"])
    print(record["text"])
    print()
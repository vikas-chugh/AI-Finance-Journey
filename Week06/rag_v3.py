"""
Project 3: RAG Regulatory Knowledge Assistant - Version 3

Description:
Improves the chunking strategy by preserving document structure instead
of splitting text at fixed character positions. Each document heading is
combined with its corresponding content paragraph to create semantically
meaningful chunks.

Key Features:
- Structure-aware chunking using headings and paragraphs.
- Preserves semantic boundaries.
- Produces cleaner chunks for embeddings and retrieval.
- Retains metadata generation from Version 2.

Learning Concepts:
- Structure-aware chunking.
- Paragraph splitting.
- enumerate().
- range(start, stop, step).
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
Splits the document into semantic chunks by combining
each heading with the paragraph immediately following it.

This preserves section boundaries and produces cleaner
retrieval units than character-based chunking.
"""
def chunk_document(text):

    paragraphs = text.split("\n\n")

    chunks = []

    for index in range(0, len(paragraphs), 2):

        heading = paragraphs[index].strip()
        content = paragraphs[index + 1].strip()

        chunk = heading + "\n" + content

        chunks.append(chunk)

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

chunks = chunk_document(document)


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

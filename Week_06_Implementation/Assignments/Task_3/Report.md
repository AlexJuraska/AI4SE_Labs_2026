## Task 3 - Chunk embedding and retrieval

The scripts embed the overlapping repository chunks from Task 2 and provide semantic search over them. The file embed_chunks.py writes a NumPy embedding matrix and matching JSON metadata, while retrieve.py embeds a query, ranks chunks by cosine similarity, and optionally merges adjacent overlapping hits.

### Design decisions

- **Model:** BAAI/bge-small-en-v1.5 was chosen, it runs locally on CPU. Code specific models are much larger and unnecessary for this smaller repository.
- **Embedded text:** Each chunk is embedded with its file path and line range. Docstrings and type hints already describe the code, so no extra summaries are generated. .gitignore chunks are skipped as noise.
- **Storage:** Vectors are saved in a NumPy file and metadata in a JSON file, in the same order. This is simple and loads instantly.
- **Retrieval:** Cosine similarity is computed with a single matrix product.
- **Merging:** Neighbouring chunks share 10 lines, so they often appear in the results together. Hits from the same file that overlap are combined into one result, leaving room for other relevant files.

Run from this directory:

```
pip install -r requirements.txt
python embed_chunks.py
python retrieve.py <search query>
```

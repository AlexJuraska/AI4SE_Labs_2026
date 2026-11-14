## Task 4 - Matching task embeddings to chunks

match_chunks.py takes an embedding of a coding task and returns the n most relevant repository chunks from the Task 3 output. embed_task() turns task text into an embedding, and match_task() combines both steps for use by the agent.

### Design decisions

- **Reuse of Task 3:** The stored embeddings, metadata, model and merging logic are imported from Task 3's retrieve.py, instead of copied, so both tasks always use the same vectors and rules. Task 3 included a basic text search to check the stored embeddings. This script separates the matching step so it takes an embedding directly.
- **Same model for queries:** The task text is turned into a vector with the same model used for the chunks. It also gets the short search prefix that this model expects in front of queries.
- **Similarity:** Cosine similarity, computed as a dot product because all vectors are normalised. The input vector is normalised too, so any embedding from the same model works.
- **Search:** Exact search over all stored vectors.
- **Merging:** Overlapping hits from the same file are combined, and further candidates are taken until n distinct results exist.
- **Optional score threshold:** min_score can drop weak matches so irrelevant code is not sent to the model.

Run from this directory:

```
python match_chunks.py <query>
```
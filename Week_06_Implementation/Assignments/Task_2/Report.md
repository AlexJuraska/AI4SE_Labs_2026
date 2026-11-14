## Task 2 - Repository chunking

The script chunk_repository.py creates a JSON data
structure containing the text of the cloned AI4SE_Playground repository. Each item stores an identifier, relative file path, start and end line numbers (indexing from 1), chunk number within the file (indexing from 0), and the chunk text.

### Design decisions

- **Chunk size:** 80 lines keeps related functions and their surrounding context together while keeping individual retrieval results small enough for a prompt.
- **Overlap:** Adjacent chunks share 10 lines. This reduces the chance that a function or class split at a boundary loses important context during retrieval.
- **Splitting method:** Files are split independently by lines, rather than by a fixed character count. Line boundaries keep Python and documentation readable and make source locations easy to cite.
- **Included content:** Text files are included recursively. Common generated or dependency directories are excluded, and files containing NUL bytes or invalid UTF-8 are skipped as binary.
- **Output:** chunks.json is a portable list of records and can be loaded directly by a later retrieval step.

The solution for Task 2 can be run from this directory with:

```
python chunk_repository.py
```

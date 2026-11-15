## Task 5 - Solving tasks with the RAG pipeline

solve_tasks.py reads each entry in missing_code.json, retrieves the top 5 chunks with Task 4's match_task(), sends the task, the empty method and the chunks to gpt-5-mini, and writes the returned method into the target file. It then runs the repository's unit tests.

### Results

- **Methods:** 10/10 implemented, all on the first attempt.
- **Unit tests:** 481/481 passed (full output in test_results.txt).
- **Retrieval:** The file containing the empty method was among the top 5 chunks for every task, and ranked first for 9 of 10.

### Observations

- **Context changed the answer:** For "InventoryLedger.\_\_contains\_\_", the method description says a product only counts if it’s in stock, but one of the retrieved tests expects it to count even after its stock has run out. The model followed the test, so the method passed.
- **Code quality:** Some methods are more defensive than needed (extra type checks in transition, a redundant check in price, an unnecessary inner generator in by_status). They are correct but more wordy than hand-written code.

Run from this directory (requires `OPENAI_API_KEY`):

```
python solve_tasks.py
```
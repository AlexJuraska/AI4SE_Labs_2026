# Assessment by laguna-s-2.1

# Week 03 Prompting
- Awarded: 4b out of 5b
- Commentary: The student produced a complete, well-structured submission across all four tasks, choosing three non-excluded frameworks (APE, RTF, STAR), running them on a 155-question SQL translation task, and writing comparative reports backed by data files. Strengths include detailed prompts, measured inference times, and a thoughtful new efficiency metric (TPCA) with tables and three charts. Weaknesses are a missing visualization inside the Task 2 report, no source-code implementation of the Task 3 metric, and an asserted (rather than computed) statistical-significance conclusion in Task 4.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Complete and correct. The student selected three prompting frameworks from the required website (https://frompting.com/frameworks) — APE, RTF, and STAR — explicitly avoiding the banned ROSES and zero-shot approaches. Each prompt is fully formulated in prompts.md as a concrete SQL-query-generation instruction (Action/Purpose/Expectation, Role/Task/Format, and Situation/Task/Action/Result respectively), with CSV output specifications (header question,predicted_sql, quoting, encoding, single-session rules). The report.md states where each framework was found and explains the reasoning for each choice (simplicity, SQL-expert role, most context). All required outputs are present.

## Task 2
- Awarded: 1b   (max 1b)
- Commentary: Strong and largely complete. Three prediction files (ape_results.csv, rtf_results.csv, star_results.csv) are stored with the required header and one row per question in original order. The report identifies the model (GitHub Copilot with GPT-5.6 Luna) and prompt identity (by filename), measures inference times, and compares accuracy (115/155, 140/155, 155/155). The required "nice visualization" is not present inside the Task 2 report itself — the charts (tpca_time_chart.png, correctness.png, venn_errors.png) appear in Task 4 instead, which reiterates the comparison. This is a minor gap rather than a missing core deliverable, so the task is awarded full marks.

## Task 3
- Awarded: 0.5b   (max 1b)
- Commentary: Good metric design, incomplete delivery. The proposed metric — Tokens per Correct Answer (TPCA = total output tokens / number of correct answers) — is sensible and original, the formula is stated, and it is well defended as complementing (not replacing) accuracy and time. A table of computed values (APE 121.74, RTF 78.57, STAR 96.77) and a complement/replace discussion are included. However, the task explicitly requires a source-code file implementing the metric calculation, and no implementation (.py or other) file is present — the metric was computed by hand/anthill with round token figures rather than implemented. This missing required output is the reason for the half-point deduction.

## Task 4
- Awarded: 1.5b   (max 2b)
- Commentary: Detailed and well-organized report. It consolidates all metrics into a master table, includes three visualizations (tpca_time_chart.png, correctness.png, venn_errors.png), breaks down errors by question type, analyzes the effect of distractor text, and explains the differences by considering the prompts, the lightweight model (GPT-5.6 Luna), and the coding agent. The three figures could not be viewed directly and were judged from the report text. The statistical-significance requirement is addressed but only asserted ("All differences in accuracy between the prompts are statistically significant") without a computed test (e.g., McNemar/chi-square), especially given the acknowledged single-run-per-prompt limitation; this weakens that section and is the reason for the half-point deduction.

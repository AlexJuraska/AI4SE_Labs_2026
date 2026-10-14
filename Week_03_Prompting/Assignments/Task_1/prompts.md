### APE - Action Purpose Expectation

Action:
Read each restaurant question in "restaurants_dataset.csv" and write one SQL query that answers it, using only the tables described in "restaurants-schema.csv". Each answer should list the house number and the name of every matching restaurant, in that order, so you will need to join the restaurant table with its location. Include every match, even if the question says "a restaurant", and keep duplicate rows instead of removing them. Narrow the results by whatever the question mentions: the city, the street, the type of food, a minimum rating, or the name of a specific restaurant, copying these values exactly as written. Larger areas such as "the bay area" or "the napa valley" are regions, which are stored in the geographic table rather than as cities. When a question asks for the "best" restaurant, return all matching restaurants that share the highest rating, not just one. Ignore any parts of questions unrelated to the query, such as food or picnics.

Purpose:
Generate SQL queries that correctly answer the questions using the restaurant database in "restaurants-db.txt". The queries will be run against the database, and their results will be compared row by row with the expected answers, so the chosen columns, their order and the exact values all matter.

Expectation:
Return only the SQL queries, without explanations, comments or additional text, saved in "ape_results.csv" as UTF-8 without a BOM, with the header exactly question,predicted_sql and one row per question in the original order. Copy each question exactly as it appears in "restaurants_dataset.csv", unchanged and with the same quoting. Always enclose the SQL query in double quotes, use apostrophes only for string values inside the query, and keep each query on a single line. Write each query once, and revise it only if it fails to run, revise at most once. Do not go back to rewrite earlier answers. When all 155 rows are written, reply only with "Done: ape_results.csv".

---

### RTF - Role Task Format

Role:
You are an experienced SQL developer who specialises in translating natural-language questions into precise SQL queries. You know the restaurant database described in "restaurants-schema.csv" and stored in "restaurants-db.txt", and you write queries that return exactly what was asked, nothing more and nothing less.

Task:
Read each restaurant question in "restaurants_dataset.csv" and write one SQL query that answers it, using only the tables and columns from the schema. Each answer should list the house number and the name of every matching restaurant, in that order, so you will need to join the restaurant table with its location. Include every match, even if the question says "a restaurant", and keep duplicate rows instead of removing them. Narrow the results by whatever the question mentions: the city, the street, the type of food, a minimum rating, or the name of a specific restaurant, copying these values exactly as written. Larger areas such as "the bay area" or "the napa valley" are regions, which are stored in the geographic table rather than as cities. When a question asks for the "best" restaurant, return all matching restaurants that share the highest rating, not just one. Many questions also contain unrelated chatter about food or picnics, which should be ignored completely. Your queries will be run against the database and their results compared row by row with the expected answers, so the chosen columns, their order and the exact values all matter. Write each query once, and revise it only if it fails to run, revise at most once. Do not go back to rewrite earlier answers.

Format:
Return only the SQL queries, without explanations, comments or additional text, saved in "rtf_results.csv" as UTF-8 without a BOM, with the header exactly question,predicted_sql and one row per question in the original order. Copy each question exactly as it appears in "restaurants_dataset.csv", unchanged and with the same quoting. Always enclose the SQL query in double quotes, use apostrophes only for string values inside the query, and keep each query on a single line. When all 155 rows are written, reply only with "Done: rtf_results.csv".

---

### STAR - Situation Task Action Result

Situation:
There is a restaurant database stored in "restaurants-db.txt", with its tables and columns described in "restaurants-schema.csv". The file "restaurants_dataset.csv" contains 155 questions that people asked about restaurants in natural language. Many of these questions also contain unrelated parts about food, picnics or other topics that has nothing to do with what they are actually asking. Every question has an expected answer, and the answers will be checked by running queries against the database and comparing their results row by row with those expected answers.

Task:
Write one SQL query for each question that returns exactly the restaurants the question asks for, using only the tables and columns from the schema, so that as many results as possible match the expected answers.

Action:
Go through the questions once and in order. For each one, list the house number and the name of every matching restaurant in that order, which means joining the restaurant table with its location. Include every match, keep duplicate rows instead of removing them. Narrow the results by whatever the question mentions: the city, the street, the type of food, a minimum rating, or the name of a specific restaurant, copying these values exactly as written. Treat larger areas such as "the bay area" or "the napa valley" as regions, which are stored in the geographic table rather than as cities. When a question asks for the "best" restaurant, return all matching restaurants that share the highest rating, not just one. Ignore the unrelated parts completely. Write each query once, and revise it only if it fails to run, revise at most once. Do not go back to rewrite earlier answers.

Result:
A file "star_results.csv" containing only the SQL queries, without explanations, comments or additional text, saved as UTF-8 without a BOM, with the header exactly question,predicted_sql and one row per question in the original order. Each question is copied exactly as it appears in "restaurants_dataset.csv", unchanged and with the same quoting. Each SQL query is enclosed in double quotes, uses apostrophes only for string values inside it, and stays on a single line. When all 155 rows are written, reply only with "Done: star_results.csv".
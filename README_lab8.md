# CPI Data Loading Strategies

## Usage Instructions
1. Run `python init_db.py` to initialize the DuckDB database with January 2024 data (`PCPI24M1.csv`).
2. Run `python update_db.py` to simulate the February 2025 data pull (`PCPI25M2.csv`) and apply three different loading strategies.
3. Use the DuckDB CLI (`duckdb cpi.db`) to query and inspect the row counts and data consistency in each table.

## Expected Results After Running Updates

* **`cpi_append` table:** * **Expectation:** Data duplication and inconsistency.
  * **Why:** The script blindly adds all rows from the 2025 file to the bottom of the table. Any dates that existed in the 2024 file and were revised in 2025 will now appear twice with different CPI values.

* **`cpi_trunc` table:**
  * **Expectation:** Perfect consistency, matching the 2025 file exactly.
  * **Why:** The script deletes all existing data and completely replaces it with the new file. It's clean but computationally expensive for large datasets.

* **`cpi_inc` (Incremental) table:**
  * **Expectation:** Perfect consistency, matching the 2025 file exactly.
  * **Why:** The script identifies which dates are in the new 2025 file, deletes only those specific older dates from the database, and then inserts the new data. No duplicates, handles revisions correctly, and is more efficient than truncation.

## Discussion
1. Append resulted in duplicate records. It is the fastest operation but completely fails to handle historical data revisions, leading to an inflated row count and inconsistent data.

2. Truncate correctly handled the historical revisions by replacing everything. The table perfectly matches the 2025 source file. However, deleting and reloading the entire dataset is computationally inefficient and doesn't scale well for large databases.

3. Incremental also resulted in perfect data consistency, properly updating the revised historical figures. By only targeting and overwriting the specific dates that were present in the new file, it avoids the heavy cost of a full table refresh, making it the most optimal ETL strategy among the three.
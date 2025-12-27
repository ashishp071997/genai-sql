import duckdb
import os

db_path = "numbers_genai_sql/db/numbers.db"

# Ensure directory exists
os.makedirs("numbers_genai_sql/db", exist_ok=True)

# DuckDB will CREATE the DB if it does not exist
con = duckdb.connect(db_path)

con.execute("""
DROP TABLE IF EXISTS sales;

CREATE TABLE sales AS
SELECT *
FROM read_csv(
    'numbers_genai_sql/data/sales_data_sample.csv',
    header=True,
    delim=',',
    ignore_errors=True
)
""")

#print(con.execute("SHOW TABLES").fetchdf())
#print(con.execute("SELECT COUNT(*) AS row_count FROM sales").fetchdf())
#print(con.execute("SELECT * FROM sales LIMIT 5").fetchdf())
print(con.execute("DESCRIBE sales").fetchdf())


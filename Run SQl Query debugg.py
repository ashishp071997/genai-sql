import duckdb


db_path = "numbers_genai_sql/db/numbers.db"

con = duckdb.connect(db_path)

print(con.execute("DESCRIBE sales").fetchdf())


print(con.execute("SELECT * FROM sales LIMIT 5").fetchdf())
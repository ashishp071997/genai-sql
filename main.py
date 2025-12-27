from fastapi import FastAPI
from pydantic import BaseModel
import duckdb
from llm import generate_sql
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="GenAI SQL API")

# ---------- Paths (SAFE) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "numbers.db")
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "sql_prompt.txt")

# ---------- Request model ----------
class QueryRequest(BaseModel):
    question: str

# ---------- Helpers ----------
def load_prompt():
    with open(PROMPT_PATH, "r") as f:
        return f.read()

def clean_sql(sql: str) -> str:
    return sql.replace("```sql", "").replace("```", "").strip()

def normalize_sql(sql: str) -> str:
    mappings = {
        "sale_amount": "SALES",
        "amount": "SALES",
        "revenue": "SALES",
        "product_id": "PRODUCTCODE",
        "item_id": "PRODUCTCODE"
    }

    for wrong, correct in mappings.items():
        sql = sql.replace(wrong, correct)
        sql = sql.replace(wrong.upper(), correct)

    return sql

# ---------- API ----------
@app.post("/query")
def query_data(req: QueryRequest):
    prompt = load_prompt()
    sql = generate_sql(req.question, prompt)
    sql = clean_sql(sql)
    sql = normalize_sql(sql)
    # Create connection PER request (SAFE)
    con = duckdb.connect(DB_PATH)
    df = con.execute(sql).fetchdf()

    return {
        "question": req.question,
        "sql": sql,
        "rows": df.to_dict(orient="records")
    }



'''import duckdb
from llm import generate_sql
#from utils import load_prompt  # optional helper


def load_prompt(path):
    with open(path, "r") as f:
        return f.read()
    
def clean_sql(sql: str) -> str:
    sql = sql.strip()
    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "")
    return sql.strip()

def normalize_sql(sql: str) -> str:
    mappings = {
        "product_id": "PRODUCTCODE",
        "item_id": "PRODUCTCODE",
        "sale_amount": "SALES",
        "amount": "SALES",
        "revenue": "SALES"
    }
    for k, v in mappings.items():
        sql = sql.replace(k, v).replace(k.upper(), v)
    return sql

SQL_PROMPT = load_prompt("numbers_genai_sql/prompts/sql_prompt.txt")

con = duckdb.connect("numbers_genai_sql/db/numbers.db")

prompt = load_prompt("numbers_genai_sql/prompts/sql_prompt.txt")

question = input("Ask your data: ")
sql = generate_sql(question, prompt)

sql = clean_sql(sql)

sql = normalize_sql(sql)

print("Generated SQL:\n", sql)
print(con.execute(sql).df())
'''

def load_prompt(path):
    with open(path, "r") as f:
        return f.read()

SQL_PROMPT = load_prompt("numbers_genai_sql/prompts/sql_prompt.txt")



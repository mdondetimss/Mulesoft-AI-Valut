#Step1: Extract Schema
from sqlalchemy import create_engine, inspect
import json
import re
import sqlite3

db_url = "sqlite:///amazon.db"

def extract_schema(db_url):
    engine = create_engine(db_url)
    inspector = inspect(engine)
    schema = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [col['name'] for col in columns]
    return json.dumps(schema)


#Step2: Text to SQL (DeepSeek with Ollama)
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


def text_to_sql(schema, prompt):
    SYSTEM_PROMPT = """
    You are an expert SQL generator. Given a database schema and a user prompt, generate a valid SQL query that answers the prompt. 
    Only use the tables and columns provided in the schema. ALWAYS ensure the SQL syntax is correct and avoid using any unsupported features. 
    Output only the SQL as your response will be directly used to query data from the database. No preamble please. Do not use <think> tags.
    """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Schema:\n{schema}\n\nQuestion: {user_prompt}\n\nSQL Query:")
    ])

    model = OllamaLLM(model="qwen2.5-coder:3b", temperature=0) #Use any other model if you want

    chain = prompt_template | model

    raw_response = chain.invoke({"schema": schema, "user_prompt": prompt})
    cleaned_response = re.sub(r"<think>.*?</think>", "", raw_response, flags=re.DOTALL)
    return cleaned_response.strip()


import time
# from logging import log_sql_query
from sql_logger import log_sql_query

# def get_data_from_database(prompt):
#     schema = extract_schema(db_url)
#     sql_query = text_to_sql(schema, prompt)
#     conn = sqlite3.connect("amazon.db")
#     cursor = conn.cursor()
#     res = cursor.execute(sql_query)
#     results = res.fetchall()
#     conn.close()
#     return results

def get_data_from_database(prompt):
    schema = extract_schema(db_url)
    sql_query = text_to_sql(schema, prompt)

    start_time = time.perf_counter()
    conn = sqlite3.connect("amazon.db")
    cursor = conn.cursor()

    try:
        res = cursor.execute(sql_query)
        results = res.fetchall()
        end_time = time.perf_counter()

        log_sql_query(
            user_prompt=prompt,
            schema=schema,
            sql_query=sql_query,
            start_time=start_time,
            end_time=end_time,
            success=True,
            error=None
        )

        return results

    except Exception as e:
        end_time = time.perf_counter()

        log_sql_query(
            user_prompt=prompt,
            schema=schema,
            sql_query=sql_query,
            start_time=start_time,
            end_time=end_time,
            success=False,
            error=e
        )

        raise  # never swallow execution errors

    finally:
        conn.close()

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import sqlite3
    
DB_PATH = "data/budget.db" 

class SQLiteQueryToolInput(BaseModel):
    """Input schema for SQLiteQueryTool."""
    sql_query: str = Field(..., description="A valid SQLite SQL query to be executed on the database.")

class SQLiteQueryTool(BaseTool):
    name: str = "Execute SQLite SQL Query"
    description: str = (
        "Executes SQLite queries on the budget database and returns structured results. "
        "Use this tool to run validated SQL queries and retrieve actual data for analysis. "
        "Ideal for testing query correctness, fetching budget/spending data, and getting results for user questions. "
        "Works with SELECT, INSERT, UPDATE, DELETE operations. "
        "Returns success with data array or error with diagnostic information."
    )
    args_schema: Type[BaseModel] = SQLiteQueryToolInput

    def _run(self, sql_query: str) -> str:
        print(f"[DEBUG] Executing SQL Query: {sql_query}")
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute(sql_query)
                rows = cur.fetchall()
                colnames = [description[0] for description in cur.description]
                print(f"[DEBUG] Query executed successfully. Columns: {colnames}, Rows: {rows}")
                result = [dict(zip(colnames, row)) for row in rows]
                return str({"status": "success", "data": result})
        except Exception as e:
            print(f"[DEBUG] Error executing query: {e}")
            return str({"status": "error", "message": str(e), "query": sql_query})
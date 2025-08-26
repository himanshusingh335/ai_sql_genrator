from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import sqlite3
    
DB_PATH = "data/budget.db" 

class DatabaseSchemaToolInput(BaseModel):
    """Input schema for DatabaseSchemaTool."""
    database_path: Optional[str] = Field(default=None, description="Optional path to the SQLite database file. Defaults to budget.db")

class DatabaseSchemaTool(BaseTool):
    name: str = "Database Schema Inspector"
    description: str = (
        "Inspects the default SQLite database and returns comprehensive schema information including: "
        "all table names, column details (name, type, constraints), and top 5 sample rows from each table. "
        "This tool uses the default database and does not require arguments."
    )
    args_schema: Type[BaseModel] = DatabaseSchemaToolInput

    def _run(self, database_path: str = None) -> str:
        if not database_path:
            database_path = DB_PATH
        print(f"[DEBUG] Inspecting database schema: {database_path}")
        try:
            with sqlite3.connect(database_path) as conn:
                cur = conn.cursor()
                
                # Get all table names
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cur.fetchall()]
                
                if not tables:
                    return str({"status": "success", "message": "No tables found in database", "data": {}})
                
                schema_info = {}
                
                for table_name in tables:
                    print(f"[DEBUG] Processing table: {table_name}")
                    table_info = {
                        "table_name": table_name,
                        "columns": [],
                        "sample_data": []
                    }
                    
                    # Get table schema (column information)
                    cur.execute(f"PRAGMA table_info({table_name});")
                    columns_info = cur.fetchall()
                    
                    for col_info in columns_info:
                        column_detail = {
                            "column_id": col_info[0],
                            "name": col_info[1],
                            "type": col_info[2],
                            "not_null": bool(col_info[3]),
                            "default_value": col_info[4],
                            "primary_key": bool(col_info[5])
                        }
                        table_info["columns"].append(column_detail)
                    
                    # Get top 5 sample rows
                    try:
                        cur.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                        sample_rows = cur.fetchall()
                        colnames = [description[0] for description in cur.description]
                        
                        # Convert rows to dictionaries
                        sample_data = [dict(zip(colnames, row)) for row in sample_rows]
                        table_info["sample_data"] = sample_data
                        table_info["row_count"] = len(sample_data)
                        
                        # Get total row count
                        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
                        total_rows = cur.fetchone()[0]
                        table_info["total_rows"] = total_rows
                        
                    except Exception as e:
                        print(f"[DEBUG] Error getting sample data for {table_name}: {e}")
                        table_info["sample_data"] = []
                        table_info["row_count"] = 0
                        table_info["total_rows"] = 0
                        table_info["error"] = str(e)
                    
                    schema_info[table_name] = table_info
                
                print(f"[DEBUG] Schema inspection completed. Found {len(tables)} tables.")
                return str({
                    "status": "success", 
                    "database_path": database_path,
                    "total_tables": len(tables),
                    "data": schema_info
                })
                
        except Exception as e:
            print(f"[DEBUG] Error inspecting database schema: {e}")
            return str({
                "status": "error", 
                "message": str(e), 
                "database_path": database_path
            })
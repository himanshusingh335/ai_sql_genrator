from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from datetime import datetime

class CurrentDateToolInput(BaseModel):
    """Input schema for CurrentDateTool."""
    date_format: str = Field(
        default="%Y-%m-%d",
        description="Optional date format in Python's datetime strftime format (default: YYYY-MM-DD)."
    )

class CurrentDateTool(BaseTool):
    name: str = "Get Current Date"
    description: str = (
        "Returns the current date in the specified format. "
        "If no format is provided, it defaults to YYYY-MM-DD."
    )
    args_schema: Type[BaseModel] = CurrentDateToolInput

    def _run(self, date_format: str) -> str:
        print(f"[DEBUG] Getting current date with format: {date_format}")
        try:
            current_date = datetime.now().strftime(date_format)
            print(f"[DEBUG] Current date generated: {current_date}")
            return str({"status": "success", "date": current_date})
        except Exception as e:
            print(f"[DEBUG] Error generating date: {e}")
            return str({"status": "error", "message": str(e)})
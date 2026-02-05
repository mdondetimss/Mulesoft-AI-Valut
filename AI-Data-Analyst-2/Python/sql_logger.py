import json
import datetime
import traceback
from pathlib import Path

LOG_FILE = Path("sql_query_log.jsonl")

def log_sql_query(
    *,
    user_prompt: str,
    schema: str,
    sql_query: str,
    start_time: float,
    end_time: float,
    success: bool,
    error: Exception | None = None
):
    """
    Append a structured log entry for a model-generated SQL query.
    This function must NEVER raise.
    """
    try:
        log_entry = {
            "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
            "user_prompt": user_prompt,
            "schema_snapshot": schema,
            "generated_sql": sql_query,
            "execution": {
                "success": success,
                "duration_ms": round((end_time - start_time) * 1000, 2),
                "error_type": type(error).__name__ if error else None,
                "error_message": str(error) if error else None,
                "traceback": traceback.format_exc() if error else None,
            }
        }

        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    except Exception:
        # Logging must never break the main application
        pass

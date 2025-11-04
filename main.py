from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.query_tool import query_company_db
import uvicorn
import os
import traceback
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Company REST API Connector")
API_KEY = os.getenv("API_KEY")

class QueryRequest(BaseModel):
    sql: str

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Company REST API Connector is running",
        "endpoints": ["/query"]
    }

@app.post("/query")
def query_db(request: QueryRequest):
    sql = request.sql.strip()

    if not sql.lower().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT statements are allowed.")
    if "company." not in sql.lower():
        raise HTTPException(status_code=403, detail="Only queries on the 'company' schema are allowed.")

    try:
        result = query_company_db(sql)
        return {"status": "success", "rows": len(result), "results": result}
    except Exception as e:
        # Debug: log full traceback to stdout/stderr (visible in heroku logs)
        tb = traceback.format_exc()
        logger.error("Exception in /query: %s\n%s", str(e), tb)
        # Return the exception message and traceback in the response temporarily
        # WARNING: This can leak sensitive info. Remove after debugging.
        raise HTTPException(status_code=500, detail={"error": str(e), "traceback": tb})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

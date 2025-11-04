from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.query_tool import query_company_db
import uvicorn
import os

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
        # Return sanitized error to client but include detail for logs
        raise HTTPException(status_code=500, detail="Internal server error. Check logs for details.")

if __name__ == "__main__":
    # Use the Heroku-provided PORT when available
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

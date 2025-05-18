from fastapi import FastAPI, Query
from googlesearch import search

app = FastAPI()

@app.get("/search")
def google_search(q: str = Query(..., description="Search query string"), num_results: int = 10):
    try:
        # 'search' returns an iterable of URLs
        results = list(search(q, num_results=num_results))
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

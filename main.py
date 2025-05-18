from fastapi import FastAPI, Query
from googlesearch import search

app = FastAPI()

@app.get("/search")
def google_search(
    q: str = Query(..., description="Search query string"),
    num_results: int = Query(10, ge=1, le=1000, description="Number of results to return"),
    start_result: int = Query(0, ge=0, le=1000, description="Start result index for pagination"),
    region: str = Query("in", description="Region code (country) for search results, e.g. 'in' for India"),
    sleep_interval: int = Query(5, ge=0, le=60, description="Sleep interval between requests in seconds")
):
    try:
        results = search(
            q,
            num_results=num_results,
            advanced=True,
            region=region,
            sleep_interval=sleep_interval,
            start_result=start_result
        )
        output = []
        for item in results:
            output.append({
                "title": item.title,
                "url": item.url,
                "description": item.description
            })
        return {"results": output}
    except Exception as e:
        return {"error": str(e)}

from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
import requests
import urllib.parse

app = FastAPI()

def fetch_google_html(query: str, num_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"

    response = requests.get(url, headers=headers)
    return response.text, response.status_code

@app.get("/search", response_class=PlainTextResponse)
def search(q: str = Query(..., description="Search query string")):
    html, status_code = fetch_google_html(q)
    return PlainTextResponse(content=html, status_code=status_code)

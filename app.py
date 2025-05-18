from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import requests
import urllib.parse

app = FastAPI()

def google_search(query: str, num_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Google search failed with status code {response.status_code}"}

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for g in soup.find_all('div', class_='tF2Cxc'):
        link_tag = g.find('a')
        if link_tag:
            title = link_tag.text
            link = link_tag['href']
            results.append({"title": title, "link": link})

    return results

@app.get("/search")
def search(q: str = Query(..., description="Search query string")):
    results = google_search(q)
    return JSONResponse(content={"results": results})

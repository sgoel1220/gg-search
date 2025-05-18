from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from pyppeteer import launch

app = FastAPI()

class SearchQuery(BaseModel):
    query: str

async def fetch_google_search_html(query: str) -> str:
    browser = await launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()

    await page.goto('https://www.google.com')

    # Accept cookies if any popup appears
    try:
        await page.waitForSelector('#L2AGLb', timeout=3000)
        await page.click('#L2AGLb')
    except Exception:
        pass

    await page.type('input[name="q"]', query)
    await page.keyboard.press('Enter')
    await page.waitForSelector('div#search')

    content = await page.content()
    await browser.close()
    return content

@app.post("/search")
async def search(payload: SearchQuery):
    if not payload.query:
        raise HTTPException(status_code=400, detail="Missing query")

    try:
        html = await fetch_google_search_html(payload.query)
        return html
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

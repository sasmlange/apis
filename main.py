from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/thrawn")
def root(max_char: int = 300):
    """
    Your dose of the Grand Admiral Thrawn. Enjoy.

    *pipe organ starts playing*
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36'

    }

    url = "http://www.goodreads.com/work/quotes/51766424-star-wars-thrawn-star-wars-thrawn-"

    all_quotes = []
    for page in range(1, 4):
        page_content = requests.get(url + str(page), headers=headers)
        book_soup = BeautifulSoup(page_content.content, features="html.parser")
        raw_quotes = book_soup.find_all("div", {"class": "quoteText"})

        for raw_quote in raw_quotes:
            quote = "".join(raw_quote.find_all(string=True, recursive=False))
            quote = quote.replace("“", '"')
            quote = quote.replace("”", '"')
            quote = quote.split('"')

            if len(quote[1]) < max_char:
                all_quotes.append(quote[1])

    return {
        "quotes": all_quotes,
        "count": len(all_quotes),
    }

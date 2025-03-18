import time
import requests
from bs4 import BeautifulSoup
import shelve

db = shelve.open("pages_db")

def get_page(url):
    if url not in db:
        response = requests.get(url)
        db[url] = response.text
    return db[url]

def get_article(url):
    response = get_page(url)
    soup = BeautifulSoup(response, "html.parser")

    title = soup.find("title").text.strip() if soup.find("title") else "No Title"
    meta_desc = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc["content"].strip() if meta_desc else "No Description"

    article_body = soup.find("article")
    article_text = article_body.get_text("\n").strip() if article_body else "No Article Found"

    filename = url.replace("http://", "").replace("https://", "").replace("/", "_") + ".txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Title: {title}\n")
        file.write(f"Description: {meta_desc}\n\n")
        file.write(article_text)

    print(f"Saved: {filename}")

def get_folders(url):
    html = get_page(url)
    soup = BeautifulSoup(html, "html.parser")
    return [url + link.get("href") for link in soup.find_all("a") if link.get("href") and link.get("href").endswith("/")]

url = "https://natura.di.uminho.pt/~jj/bs4/folha8-2023/"
folders = get_folders(url)[1:] # ignore parent

print(f"Found {len(folders)} folder URLs.")
#print(folders)

for url in folders:
    get_article(url)
    time.sleep(1)

db.close()

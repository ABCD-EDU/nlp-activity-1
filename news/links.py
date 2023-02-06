from selenium import webdriver
from bs4 import BeautifulSoup
import re

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")

browser = webdriver.Chrome(options=options)

def get_links(page):
  browser.get("https://balita.net.ph/category/balita-main/page/" + str(page))

  html = browser.page_source
  soup = BeautifulSoup(html, "html.parser")

  link_collection = []

  for link in [link.get("href") for link in soup.find_all("a")]:
    if "2023" in link:
      link = link.replace("/#comments", "")
      if link[len(link) - 1] == "/":
        link = link[:-1]
      link_collection.append(link)

  unique_links = list(set(link_collection))

  with open("links.csv", "a") as file:
    for link in unique_links:
      file.write(link + ",\n")

for page in range(1, 100):
  get_links(page)

browser.close()
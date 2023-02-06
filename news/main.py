import requests
from bs4 import BeautifulSoup
import json
import re
import csv

def scrape_body(url=None):
  if url is None:
    return ""

  try:
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

    # Make a GET request to the URL
    response = requests.get(url, headers=headers)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # find the script tag that contains the JSON data
    script = soup.findAll("script", type="application/ld+json")

    # extract the text content of the script tag
    json_text = script[2].text # 1 is the index of the script tag that contains the news JSON data

    # parse the JSON data into a Python dictionary
    data = json.loads(json_text)

    # parse news content
    news = data["articleBody"]

    # remove "<!-- wp:paragraph -->"
    news = re.sub(r"<!-- wp:paragraph -->", "", news)

    # remove "<!-- /wp:paragraph -->"
    news = re.sub(r"<!-- /wp:paragraph -->", "", news)

    # remove html tags
    news = re.sub(r'<.*?>', '', news)

    # remove new lines
    news = re.sub(r"\n", "", news)

    news = re.sub(r'\s{2,}', ' ', news)

    return news
  except:
    return ""

with open('links.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        link = row[0]
        text = scrape_body(link).strip()
        text = re.sub(r'http\S+', '', text)
        # TODO: more intensive data cleaning
        with open('news.txt', 'a', encoding="utf8") as file:
          file.write(text + " \n")
          file.close()

        with open('words.txt', 'a', encoding="utf8") as file:
          for word in re.findall(r'[\w-]+', text):
            file.write(word + ",\n")
          file.close()
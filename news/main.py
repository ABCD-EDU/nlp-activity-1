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
    news = re.sub(r'&[a-z]+;', '', news)

    # remove new lines
    news = re.sub(r"\n", " ", news)
    news = re.sub(r'\s{2,}', ' ', news)

    # remove numbers
    news = re.sub(r'\d+(,\d+)*', '', news)

    # remove special characters
    news = re.sub(r'[^a-zA-Z0-9\s-]', '', news)

    # double spaces
    news = re.sub(' +', ' ', news)

    news = re.sub(r'--', '', news)
    news = re.sub(r' --', '', news)

    return news
  except:
    return ""

all_string = ""

with open('links.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print("Scraping: " + row[0])
        link = row[0]
        text = scrape_body(link).strip()
        text = re.sub(r'http\S+', '', text)
        # TODO: more intensive data cleaning
        with open('news.txt', 'a', encoding="utf8") as file:
          all_string += text + " "
          print("Total word count: " + str(len(all_string.split(" "))))

          if len(all_string.split(" ")) <= 50000 and text != "":
            print("Writing to file...")
            file.write(text.strip() + "\n")
          else:
            file.close()
            exit(1)
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt

def create_wordcloud(text, filename):
  path = "./word-clouds/" + filename
  wordcloud = WordCloud(width=800, height=800,
                        background_color='white',
                        stopwords=None,
                        min_font_size=10).generate(text)

  plt.figure(figsize=(8, 8), facecolor=None)
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.tight_layout(pad=0)

  plt.savefig(path, dpi=300, bbox_inches='tight')
  image = Image.open(path)
  image.save(path, "PNG")

# TODO: Change the paths and the names of the files you want to create word clouds for
NEWS = {
  "path": "./news/news.txt",
  "name": "news"
}
BIBLE = {
  "path": "",
  "name": ""
}
WIKI_TL = {
  "path": "",
  "name": ""
}

topics = [NEWS, BIBLE, WIKI_TL]

for topic in topics:
  if topic["path"] != "":
    with open(topic["path"], "r", encoding="utf8") as file:
      text = file.read()
      print("Exporting word cloud for " + topic["name"] + "...")
      create_wordcloud(text, topic["name"] + ".png")


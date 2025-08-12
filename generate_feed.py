import feedparser
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring

feeds = [
    "https://www.livemint.com/rss/markets",
    "https://www.livemint.com/rss/news",
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://www.moneycontrol.com/rss/mostpopular.xml"
]

all_items = []
for url in feeds:
    data = feedparser.parse(url)
    for e in data.entries:
        all_items.append({
            "title": e.title,
            "link": e.link,
            "description": e.get("summary", ""),
            "pubDate": datetime(*e.published_parsed[:6])
        })

top50 = sorted(all_items, key=lambda x: x["pubDate"], reverse=True)[:50]

rss = Element("rss", version="2.0")
channel = SubElement(rss, "channel")
SubElement(channel, "title").text = "Combined Indian Markets Feed"
SubElement(channel, "link").text = "https://rss-fee.netlify.app/feed.xml"
SubElement(channel, "description").text = "Top 50 items from LiveMint and Moneycontrol"
SubElement(channel, "lastBuildDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0530")

for item in top50:
    it = SubElement(channel, "item")
    SubElement(it, "title").text = item["title"]
    SubElement(it, "link").text = item["link"]
    SubElement(it, "description").text = item["description"]
    SubElement(it, "guid").text = item["link"]
    SubElement(it, "pubDate").text = item["pubDate"].strftime("%a, %d %b %Y %H:%M:%S +0530")

with open("feed.xml", "wb") as f:
    f.write(tostring(rss, encoding="utf-8", xml_declaration=True))

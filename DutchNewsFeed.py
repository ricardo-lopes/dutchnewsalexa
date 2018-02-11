import feedparser
import urllib3
from bs4 import BeautifulSoup


def get_feed_object():
    feed = feedparser.parse('http://www.dutchnews.nl/feed/?news')
    return feed


def get_feed_item(i):
    feed = get_feed_object()
    return feed.entries[i]


def get_feed_title(i):
    feed = get_feed_object()
    entry = feed.entries[i]
    response = f"Breaking news: {entry.title}. <break time=\"1s\"/>"
    return response


def scrape_feed_item(i):
    item = get_feed_item(i)
    http = urllib3.PoolManager()
    link = item.link
    page = http.request('GET', link)
    soup = BeautifulSoup(page.data, 'html.parser')
    content = soup.find('div', attrs={'class': 'entry-content'})
    for s in content.findAll('script'):
        s.decompose()
    for s in content.findAll('span'):
        s.decompose()
    for s in content.findAll('blockquote'):
        s.decompose()
    decomposed_text = content.text.replace('\r', ' ').replace('\n', ' ')
    decomposed_text = decomposed_text.replace('.', '.<break time=\"1s\"/>')
    return decomposed_text

# print(scrape_feed_item(0))
# print(scrape_feed_item(1))
# print(scrape_feed_item(2))
# print(scrape_feed_item(3))
# print(scrape_feed_item(4))
# print(scrape_feed_item(5))
# print(scrape_feed_item(6))
# print(scrape_feed_item(7))
# print(scrape_feed_item(8))
# print(scrape_feed_item(9))

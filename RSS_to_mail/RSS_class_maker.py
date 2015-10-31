import datetime, json

class RSSFeed:
    def __init__(self, url, send_url_content=1):
        self.url = url
        self.send_url_content = send_url_content
        self.last_checked = 0

        self.last_checked = datetime.datetime.utcnow()

url = str(input('URL: '))

rss = RSSFeed(url)

data = '\n' + json.dumps({'url': rss.url, 'send_url_content': rss.send_url_content, 'last_checked': rss.last_checked.timestamp()})

f = open('feeds.txt', 'a+')

f.write(data)


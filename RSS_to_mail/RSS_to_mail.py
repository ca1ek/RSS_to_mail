import pickle, feedparser, json, pprint, datetime, time, requests, re

feed_file = 'feeds.txt'
f = open(feed_file, 'r')
not_done = True

class URLOrDataIncorrect(Exception):
    pass

def get_new_entries(feed_data):                 # takes dict loaded from JSON in file, throws out text
    d = feedparser.parse(feed_data['url'])      # {'last_checked': UNIX TIME(float/int), 'url': addres of RSS(string) ...}
    if d['bozo']:
        raise URLOrDataIncorrect

    list = []
    for ii in d['entries']:
        if time.mktime(ii['updated_parsed']) > feed_data['last_checked']:
            url = ii['content'][0]['base']
            r = requests.get(url)
            txt = r.text.split('<div class="entry">')[1]
            txt = txt.split('</div></p><p>')[1]
            exp = p = re.compile(r'<.*?>') # regex to strip HTML tags
            return exp.sub('', txt.split('<h4>Przeczytaj także:</h4>')[0])

def update_last_checked_time(feed_data): # REMEMBER TO MANUALLY SAVE WHATS RETURNED.
    feed_data['last_checked'] = datetime.datetime.utcnow().timestamp()
    return feed_data

while not_done:
    try:
        if not 'begin_pos' in locals():
            begin_pos = f.tell()                                                     
        feeds_list = json.loads(f.readline())           # Read the data from file
        pprint.pprint(feeds_list)

        end_pos = f.tell()                         
        entry_str = get_new_entries(feeds_list)
        #print('BEGIN:' + str(begin_pos) + ' END:' + str(end_pos))
        f.close()
        f = open(feed_file, 'w+')                       # Open up the file for writing
        f.seek(begin_pos)                               # Go to position of that one line

        updated_feeds = json.dumps(update_last_checked_time(feeds_list)) # Update feeds check time
        f.write(updated_feeds)                          # Write it down

        #print('END: ' + str(f.tell()))
        print(entry_str)
        
    except ValueError:
        not_done = False
    except URLOrDataIncorrect:
        pass
    
f.close()
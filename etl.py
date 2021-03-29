import requests
import json
import time
import pandas as pd

def getAllSubmissions(url, subreddit):
    response = requests.get(url, params = {'subreddit':subreddit, 'size':'500', 'fields':['author','created_utc','full_link','id','link_flair_text','title','selftext']})
    data = json.loads(response.text)
    data = pd.json_normalize(data['data'])
    before = data['created_utc'].min()
    print(before)
    data = data[['author','created_utc','full_link','id','link_flair_text','title','selftext']]
    with open('teachers.csv', 'w') as f:
        data.to_csv(f, index=False)
    time.sleep(2.01)
    while before > 1420092000: # This is 01/01/2015 12am Central Time
        response = requests.get(url, params = {'subreddit':subreddit, 'size':'500', 'before':before, 'fields':['author','created_utc','full_link','id','link_flair_text','title','selftext']})
        data = json.loads(response.text)
        data = pd.json_normalize(data['data'])
        before = data['created_utc'].min()
        print(before)
        try:
            data = data[['author','created_utc','full_link','id','link_flair_text','title','selftext']]
            with open('teachers.csv', 'a') as f:
                data.to_csv(f, index=False, header=False)
        except Exception as e:
            print('skipping', before, e)
            before -= 3600
        time.sleep(2.01)
    print('complete')

if __name__ == '__main__':
    getAllSubmissions(url = 'https://api.pushshift.io/reddit/search/submission/', subreddit = 'teachers')
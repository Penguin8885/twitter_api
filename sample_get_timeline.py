from requests_oauthlib import OAuth1Session
import json

if __name__ == '__main__':
    CK = 'XXXXXXXXXXXXXXXXXXXXXX'                             # Consumer Key
    CS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Consumer Secret
    AT = 'XXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Access Token
    AS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Accesss Token Secert

    # タイムライン取得用のURL
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

    # とくにパラメータは無い
    params = {}

    # OAuth で GET method
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.get(url, params = params)

    # レスポンスを確認
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:
            print(tweet["text"])
    else:
        print ("Error: %d" % req.status_code)
from requests_oauthlib import OAuth1Session
import datetime

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
        limit = req.headers['x-rate-limit-remaining']   # API残り
        reset = req.headers['x-rate-limit-reset']       # API制限の更新時刻 (UNIX time)
        reset_time = str(datetime.datetime.fromtimestamp(int(reset)))
        print ("API remain: " + limit)
        print ("API reset: " + reset_time)
    else:
        print ("Error: %d" % req.status_code)
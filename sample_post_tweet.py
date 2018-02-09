from requests_oauthlib import OAuth1Session

if __name__ == '__main__':
    CK = 'XXXXXXXXXXXXXXXXXXXXXX'                             # Consumer Key
    CS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Consumer Secret
    AT = 'XXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Access Token
    AS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Accesss Token Secert

    # ツイート投降用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

    # ツイート本文
    params = {"status": "Hello, World!"}

    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(url, params=params)

    # レスポンスを確認
    if req.status_code == 200:
        print ("OK")
    else:
        print ("Error: %d" % req.status_code)





from requests_oauthlib import OAuth1Session
import json
from datetime import datetime
from time import sleep

def get_saved_tweet_max_id(json_path):
    try:
        with open(json_path, 'rb') as f:
            data = json.load(f)
    except FileNotFoundError:
        return -1                   # 最新ツイートから取得

    if len(data) > 0:
        return data[-1]['id'] - 1   # 保存済みのツイートの次のものから取得
    else:
        return -1                   # 最新ツイートから取得

def append_json(json_path, data):
    with open(json_path, 'ab+') as f:
        f.seek(0, 2)                                            # ファイルの末尾（2）に移動（フォフセット0）
        if f.tell() == 0:                                       # ファイルが空かチェック
            dump = json.dumps([data[0]], ensure_ascii=False)    # JSON 形式にダンプ
            f.write(dump.encode("utf-8"))                       # 空の場合は先頭のみ書き込む
            data = data[1:]                                     # 使用した先頭をリストから取り除く

        f.seek(-1, 2)                                           # ファイルの末尾（2）から -1 文字移動
        f.truncate()                                            # JSON 配列を開ける（最後の]の削除）
        for datum in data:
            f.write(','.encode("utf-8"))                        # 配列のセパレーターを書き込む
            dump = json.dumps(datum, ensure_ascii=False)        # JSON 形式にダンプ
            f.write(dump.encode("utf-8"))                       # 書き込み
        f.write(']'.encode("utf-8"))                            # JSON 配列を閉じる（最後に]の挿入）



if __name__ == '__main__':
    json_path = './tweet.json'

    CK = 'XXXXXXXX' # Consumer Key
    CS = 'XXXXXXXX' # Consumer Secret
    AT = 'XXXXXXXX' # Access Token
    AS = 'XXXXXXXX' # Accesss Token Secert

    # タイムライン取得用のURL
    url = "https://api.twitter.com/1.1/search/tweets.json"
    keyword = '#AppleEvent'

    max_id = get_saved_tweet_max_id(json_path) # 取得するtweetの最初のIDを取得


    params = {
        'q' : keyword + ' lang:ja -filter:media -filter:replies -filter:retweets -filter:links',  # 画像, 動画を除外
        'count' : 100,              # 取得数は100件(最大)
        'max_id' : max_id,          # 保存していないツイートから取得
        'tweet_mode':'extended',    # テキストを省略せずに取得
    }

    # OAuthセッションの開始
    twitter = OAuth1Session(CK, CS, AT, AS)

    total = 0 # ツイート取得数
    while(True):
        # リクエスト(GET)
        req = twitter.get(url, params=params)

        # レスポンスを確認
        if req.status_code == 200:

            # tweetの取得と書き込み
            search_timeline = json.loads(req.text)                  # 結果の取得
            append_json(json_path, search_timeline['statuses'])     # jsonに追加書き込み
            num = len(search_timeline['statuses'])
            total += num
            limit = req.headers['x-rate-limit-remaining']
            print(datetime.now(), total, limit)

            # 取得ができなくなった, 取得数が一定値を超えたら終了
            if num == 0 or total >= 1000000:
                break

            # 次回取得位置の更新
            max_id = search_timeline['statuses'][-1]['id']
            params['max_id']  = max_id - 1


        # 正しく取得できなかった場合
        else:
            print("Error: status_code=%d" % req.status_code)

            # API制限の情報の表示
            limit = req.headers['x-rate-limit-remaining']           # API制限の残り取得回数
            reset = req.headers['x-rate-limit-reset']               # API制限の更新時刻 (UNIX time)
            reset_time = str(datetime.fromtimestamp(int(reset)))    # UNIX timeからdatetime形式に変換
            print("API remaining: " + limit)
            print("API reset: " + reset_time)

            # 待機処理
            print("wait 15 min")
            sleep(15*60)
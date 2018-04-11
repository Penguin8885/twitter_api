from requests_oauthlib import OAuth1Session
import json
import datetime


class ReplyBot:
    userstream_url = "https://userstream.twitter.com/1.1/user.json"
    post_url = "https://api.twitter.com/1.1/statuses/update.json"

    def __init__(self, CK, CS, AT, AS, botID):
        self.CK = CK
        self.CS = CS
        self.AT = AT
        self.AS = AS
        self.bot_screen_name = botID[1:] # @を削除


    # botの作業を開始するメソッド
    def start(self):
        # OAuthでTwitterに接続
        twitter = OAuth1Session(self.CK, self.CS, self.AT, self.AS)
        req = twitter.post(self.userstream_url, params={}, stream=True)

        # 接続エラー
        if req.status_code != 200:
            print ('Error: %d' % req.status_code)

        # 接続成功
        else:
            # ストリームの接続状態を表示
            print(req.headers)

            # ストリームを監視
            for stream in req.iter_lines(chunk_size=1, decode_unicode=True):
                stream_js = self.__get_stream_js(stream) # jsonを取得

                if stream_js is not None:
                    # ストリームの内容を表示
                    print('======== ' + str(datetime.datetime.now()) + ' ========')
                    if 'created_at' in stream_js:
                        print(stream_js['user']['name'])
                        print(stream_js['text'])
                        print('url', stream_js['entities']['urls'])
                    else:
                        for key in stream_js:
                            print(key, ':', stream_js)

                    # リプライ
                    if self.__is_reply_to_me(stream_js):
                        reply = self.__create_reply(stream_js)  # リプを作成
                        self.__post_reply(stream_js, reply)     # リプをポスト


    # ストリームをjson形式で取得
    def __get_stream_js(self, stream):
        if stream == b'':   # 更新情報なし(空文字)
            return None
        else:               # 更新情報あり
            return json.loads(stream)


    # botへのリプライであるかを確認
    def __is_reply_to_me(self, stream_js):
        if 'in_reply_to_screen_name' in stream_js:
            if stream_js['in_reply_to_screen_name'] == self.bot_screen_name:
                return True
        return False


    # リプライを作成
    def __create_reply(self, stream_js):
        text = stream_js['text']
        splited = text.split(' ')
        for token in splited[:]:
            if token[0] == '@':
                splited.remove(token)

        # トリガー設定
        if splited[0] == 'test':
            return 'success'
        elif splited[0] == 'Q':
            return 'A'
        else:
            return None


    # リプライを送信
    def __post_reply(self, stream_js, tweet):
        if tweet is None:
            return  # なにもせずに終了

        # Twitterに接続してPOST
        print('######## ' + str(datetime.datetime.now()) + ' ########')
        twitter = OAuth1Session(self.CK, self.CS, self.AT, self.AS)
        params = {'status': tweet, 'in_reply_to_status_id': stream_js['id']}
        req = twitter.post(self.post_url, params=params)

        if req.status_code == 200:
            print('Success:', params)
            print(req.headers)
        else:
            print('Error: %d' % req.status_code)




if __name__ == '__main__':
    CK = 'XXXXXXXXXXXXXXXXXXXXXX'                             # Consumer Key
    CS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Consumer Secret
    AT = 'XXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # Access Token
    AS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'         # Accesss Token Secert

    bot = ReplyBot(CK, CS, AT, AS, '@___________')
    bot.start()

import psycopg2
import psycopg2.extras
import requests
from dotenv import load_dotenv
import os

# .env ファイルをロードして環境変数へ反映
load_dotenv()

# 環境変数を参照
HOST = os.getenv('DB_HOST')
PORT = '5432'
DB_NAME = os.getenv('DB_NAME')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASS')


# DBへ接続
print(HOST)
conn = psycopg2.connect("host=" + HOST + 
                        " port=" + PORT + 
                        " dbname=" + DB_NAME + 
                        " user=" + USER + 
                        " password=" + PASSWORD
                        )

#SQL
sql = "SELECT * FROM account"

#URL
url = "https://www.mydns.jp/directip.html"

# DBの接続確認
#if not conn.is_connected():
#    raise Exception("DBへの接続に失敗しました")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # 取得結果を辞書型で扱う設定


query__for_fetching = sql
cur.execute(query__for_fetching)


for fetched_line in cur.fetchall():
    mydns_id = fetched_line['mydns_id']
    mydns_pass = fetched_line['mydns_pass']
    ipv4 = fetched_line['ipv4']
    ipv6 = fetched_line['ipv6']

    response = requests.get(url+"?MID="+mydns_id+"&PWD="+mydns_pass+"&IPV4ADDR="+ipv4+"&IPV6ADDR="+ipv6)

    print(response.status_code)    # HTTPのステータスコード取得
    #print(response.text)    # レスポンスのHTMLを文字列で取得

cur.close()
conn.close()

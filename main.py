import mysql.connector
import requests
from dotenv import load_dotenv
import os

# .env ファイルをロードして環境変数へ反映
load_dotenv()

# 環境変数を参照
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASS')
MYSQL_TABL = os.getenv('MYSQL_TABL')


# DBへ接続
conn = mysql.connector.connect(
    user=MYSQL_USER,
    password=MYSQL_PASS,
    host=MYSQL_HOST,
    database=MYSQL_TABL
)

#SQL
sql = "SELECT * FROM account"

#URL
url = "https://www.mydns.jp/directip.html"

# DBの接続確認
if not conn.is_connected():
    raise Exception("MySQLサーバへの接続に失敗しました")

cur = conn.cursor(dictionary=True)  # 取得結果を辞書型で扱う設定

query__for_fetching = sql
cur.execute(query__for_fetching)

for fetched_line in cur.fetchall():
    mydns_id = fetched_line['mydns_id']
    mydns_pass = fetched_line['mydns_pass']
    ipv4 = fetched_line['ipv4']
    ipv6 = fetched_line['ipv6']

    response = requests.get(url+"?MID="+mydns_id+"&PWD="+mydns_pass+"&IPV4ADDR="+ipv4+"&IPV6ADDR="+ipv6)

    print(response.status_code)    # HTTPのステータスコード取得
    ##print(response.text)    # レスポンスのHTMLを文字列で取得

import pandas as pd
import requests
from bs4 import BeautifulSoup

# 指定されたURL
url = "https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0045&ek=004506820&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&po2=99&pc=100"

# リクエストを送信してページの内容を取得
response = requests.get(url)
html = response.text
response.encoding = response.apparent_encoding  # 文字エンコーディングを設定

# BeautifulSoupを使用してHTMLを解析
soup = BeautifulSoup(response.text, "html.parser")

# 物件情報を格納するリスト
properties = []

# 物件名を取得
property_names = [
    a.text.strip() for a in soup.find_all("a", class_="js-cassetLinkHref")
]

# 各物件の物件情報を取得
tables = pd.read_html(html)

for i, table in enumerate(tables):
    if i < len(property_names):
        property_name = property_names[i]
    else:
        property_name = "物件名不明"

    # 物件情報をリストに追加
    property_data = table
    property_data["物件名"] = property_name
    properties.append(property_data)

# すべての物件情報を1つのDataFrameに結合
all_properties_df = pd.concat(properties, ignore_index=True)

# CSVファイルに出力
all_properties_df.to_csv("properties.csv", index=False, encoding="utf-8-sig")

print("データをproperties.csvに保存しました。")

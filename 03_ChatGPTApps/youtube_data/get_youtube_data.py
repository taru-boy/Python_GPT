import pandas as pd
from googleapiclient.discovery import build

# YouTube Data APIキーを設定
api_key = 'AIzaSyB84J5-WMPRdLnxl_hVebHgTy4siYhEoL4'

# YouTube Data APIのクライアントを作成
youtube = build('youtube', 'v3', developerKey=api_key)

# キーワードで動画を検索
search_response = youtube.search().list(
    q='ChatGPT',
    type='video',
    maxResults=30,
    part='id'
).execute()

# 動画の詳細情報を取得
video_details = []
for search_result in search_response.get('items', []):
    video_id = search_result['id']['videoId']
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet,statistics'
    ).execute()
    video_info = video_response['items'][0]
    video_title = video_info['snippet']['title']
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    video_views = video_info['statistics']['viewCount']
    video_likes = video_info['statistics']['likeCount']
    video_details.append([video_title, video_url, video_views, video_likes])

# データをDataFrameに格納
df = pd.DataFrame(video_details, columns=['タイトル', 'URL', '再生回数', 'いいね数'])

# 再生回数でソート
df['再生回数'] = df['再生回数'].astype(int)
df = df.sort_values(by='再生回数', ascending=False)

# CSVファイルに出力
df.to_csv('ChatGPT_videos_sorted.csv', index=False)

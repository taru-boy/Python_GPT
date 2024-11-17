import pandas as pd
from googleapiclient.discovery import build

# YouTube Data APIクライアントを設定
API_KEY = "AIzaSyB84J5-WMPRdLnxl_hVebHgTy4siYhEoL4"  # ご自身のYouTube APIキーに置き換えてください
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# YouTube APIクライアントを初期化
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


# 「Streamlit」に関連する動画を取得する関数
def get_youtube_videos(keyword, max_results=30):
    # YouTubeで「Streamlit」キーワードに関連する動画を検索
    search_response = (
        youtube.search()
        .list(q=keyword, type="video", part="id,snippet", maxResults=max_results)
        .execute()
    )

    # 動画データを格納するリスト
    video_data = []

    # 検索結果をループし、動画の詳細を取得
    for search_result in search_response.get("items", []):
        video_id = search_result["id"]["videoId"]
        title = search_result["snippet"]["title"]
        channel_title = search_result["snippet"]["channelTitle"]  # チャンネル名
        url = f"https://www.youtube.com/watch?v={video_id}"

        # 動画の統計情報（再生回数、いいね数）を取得
        video_response = youtube.videos().list(part="statistics", id=video_id).execute()

        for video in video_response.get("items", []):
            view_count = int(video["statistics"].get("viewCount", 0))
            like_count = int(video["statistics"].get("likeCount", 0))

            # 動画の詳細をリストに追加
            video_data.append(
                {
                    "Title": title,
                    "Channel Name": channel_title,  # チャンネル名
                    "URL": url,
                    "View Count": view_count,
                    "Like Count": like_count,
                }
            )

    return video_data


# keywordに関連するトップ30の動画を取得
keyword = "streamlit"
videos = get_youtube_videos(keyword, max_results=30)

# データをDataFrameに変換
df = pd.DataFrame(videos)

# 再生回数で降順にソート
df_sorted = df.sort_values(by="View Count", ascending=False)

# CSVファイルとして保存
directory_path = "03_ChatGPTApps/youtube_data"
file_name = f"{keyword}_videos.csv"
df_sorted.to_csv("/".join([directory_path, file_name]), index=False)

print(
    f"'{file_name}' が作成されました。"
)
import streamlit as st
import sqlite3
import pandas as pd
import os

# データベースファイルのパス
DB_FILE = "02_sql_app/sql_learning_app.db"

# データベースの初期設定
def init_db():
    # データベースファイルが存在しない場合、作成して初期化
    is_new_db = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)  # ディレクトリ内にDBファイルを作成
    cursor = conn.cursor()

    if is_new_db:
        # メインテーブル作成
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                city TEXT NOT NULL
            )
        """)
        # 補助テーブル作成
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product TEXT NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        # 初期データ挿入
        cursor.executemany("""
            INSERT INTO users (name, age, city) VALUES (?, ?, ?)
        """, [
            ("Alice", 25, "New York"),
            ("Bob", 30, "Los Angeles"),
            ("Charlie", 35, "Chicago"),
        ])
        cursor.executemany("""
            INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)
        """, [
            (1, "Laptop", 1200),
            (2, "Phone", 800),
            (1, "Tablet", 500),
            (3, "Monitor", 300),
        ])
        conn.commit()
    return conn

# データを表示する関数
def display_table(conn, table_name="users"):
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        st.write(f"### テーブル `{table_name}` の内容:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"テーブルの表示中にエラーが発生しました: {e}")

# Streamlitアプリケーション
def main():
    # カスタムCSSを適用
    st.markdown("""
        <style>
        /* サイドバーの横幅を2倍に設定 */
        [data-testid="stSidebar"] {
            width: 40rem;
        }
        /* タイトルのフォントサイズを0.5倍に設定 */
        h1 {
            font-size: 0.5em !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("SQL学習アプリ")
    st.markdown("SQLiteを使用して基本的なSQLコードを実行し、結果を確認できます。")

    # データベースの初期化
    conn = init_db()
    
    # サイドバーに基本的なSQL例の表示
    st.sidebar.title("SQLコードの例")
    st.sidebar.markdown("""
    ### 基本的なSQL構文:
    - **テーブルの作成**:  
      ```sql
      CREATE TABLE users (
          id INTEGER PRIMARY KEY,
          name TEXT,
          age INTEGER,
          city TEXT
      );
      ```
    - **データの挿入**:  
      ```sql
      INSERT INTO users (name, age, city) VALUES ('David', 40, 'Miami');
      ```
    - **データの取得**:  
      ```sql
      SELECT * FROM users;
      ```
    - **データの更新**:  
      ```sql
      UPDATE users SET age = 26 WHERE name = 'Alice';
      ```
    - **データの削除**:  
      ```sql
      DELETE FROM users WHERE name = 'Alice';
      ```
    - **JOINの使用例**:  
      ```sql
      SELECT u.name, o.product, o.amount
      FROM users u
      JOIN orders o
      ON u.id = o.user_id;
      ```
      このクエリはユーザー名とその注文内容を結合して表示します。
    """)

    # JOIN用テーブルの内容も表示
    st.sidebar.markdown("#### テーブル情報")
    st.sidebar.markdown("- **users**: ユーザー情報を格納")
    st.sidebar.markdown("- **orders**: 注文情報を格納")

    # ユーザーがSQLコードを入力
    st.subheader("SQLコードを入力")
    sql_code = st.text_area("SQLコードを入力してください:", value="SELECT * FROM users;")

    if st.button("実行"):
        try:
            cursor = conn.cursor()
            cursor.execute(sql_code)
            conn.commit()

            # 結果の取得と表示
            if sql_code.strip().lower().startswith("select"):
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                st.write("### 実行結果:")
                st.dataframe(df)
            else:
                st.success("SQLコードが正常に実行されました！")
                display_table(conn)  # テーブルの内容を再表示
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

    st.info("SQLコードを実行すると、上記の結果がリアルタイムで反映されます。")

    # アプリの終了時にデータベースをクローズ
    conn.close()

if __name__ == "__main__":
    main()

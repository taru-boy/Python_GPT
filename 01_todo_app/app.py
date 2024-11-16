import sqlite3
import streamlit as st

# データベースのセットアップ
DB_FILE = "01_todo_app/tasks.db"


def init_db():
    """データベースを初期化する"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


def add_task(task):
    """新しいタスクをデータベースに追加する"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()


def get_tasks():
    """データベースからタスクを取得する"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # 未完了のタスクを先に、完了したタスクを後に表示
    cursor.execute("SELECT id, task, completed FROM tasks ORDER BY completed, id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task_status(task_id, completed):
    """タスクの状態を更新する"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()


# チェックボックスの状態が変更されたときに呼ばれる関数
def on_checkbox_change(task_id, is_checked):
    update_task_status(task_id, is_checked)
    st.session_state["rerun"] = not st.session_state.get(
        "rerun", False
    )  # 再レンダリングをトリガー


# データベースの初期化
init_db()

# タスクの追加
new_task = st.text_input("新しいタスクを入力してください", key="new_task")
if st.button("追加"):
    if new_task:
        add_task(new_task)
        # セッション状態のフラグを切り替えて再レンダリングをトリガー
        st.session_state["rerun"] = not st.session_state.get("rerun", False)
    else:
        st.warning("タスクを入力してください。")


tasks = get_tasks()  # タスク取得関数
if tasks:
    for task_id, task, completed in tasks:
        col1, col2 = st.columns([4, 1])

        # 完了したタスクには横線を引く
        task_text = f"<s>{task}</s>" if completed else task

        # チェックボックスでタスク状態を表示・更新
        is_checked = col2.checkbox(
            "完了",
            value=bool(completed),
            key=f"checkbox_{task_id}",
            on_change=on_checkbox_change,
            args=(task_id, not completed),
        )

        # タスク名の表示（完了した場合に横線）
        col1.markdown(task_text, unsafe_allow_html=True)
else:
    st.info("現在、タスクはありません。")

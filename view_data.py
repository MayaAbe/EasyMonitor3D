import sqlite3

def view_data():
    # データベースに接続
    conn = sqlite3.connect('udp_data.db')
    cursor = conn.cursor()

    # データベース内のすべてのデータを取得
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("データベースにデータがありません。")
    else:
        # データを表示
        print("データベースに保存されたデータ:")
        print("ID | 数値1 | 数値2 | 数値3 | 数値4 | 数値5 | 数値6 | タイムスタンプ")
        print("----------------------------------------------------------")

        # 各行のデータを表示
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]}")

    # 接続を終了
    conn.close()

if __name__ == "__main__":
    view_data()

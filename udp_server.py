import socket
import sqlite3
import json
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect('udp_data.db')
    cursor = conn.cursor()
    # テーブル構造を変更して、6つの数値を1行に保存
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number1 INTEGER,
            number2 INTEGER,
            number3 INTEGER,
            number4 INTEGER,
            number5 INTEGER,
            number6 INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    return conn

def store_data(conn, numbers, timestamp):
    cursor = conn.cursor()
    # 6つの数値とタイムスタンプを1行に挿入
    cursor.execute('''
        INSERT INTO data (number1, number2, number3, number4, number5, number6, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (*numbers, timestamp))
    conn.commit()

def udp_server():
    server_address = ('localhost', 12345)  # 自分のIPアドレスとポート番号
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    # データベースを初期化
    conn = initialize_db()

    print(f"UDPサーバが {server_address} で起動しました...")

    try:
        while True:
            data, address = sock.recvfrom(4096)  # データを受信
            json_data = data.decode()

            try:
                # JSONデータをパース
                received_data = json.loads(json_data)
                numbers = received_data.get("numbers", [])

                # 数値が6つ存在するか確認
                if len(numbers) == 6:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # 受信した数値を表示
                    print(f"{address} から受信したデータ: {numbers} at {current_time}")

                    # データベースに蓄積
                    store_data(conn, numbers, current_time)
                else:
                    print("受信データの数が6つではありません。")
            except json.JSONDecodeError:
                print("受信データの解析に失敗しました。")
    finally:
        sock.close()
        conn.close()

if __name__ == "__main__":
    udp_server()

import socket
import time
import random
import json
import pandas as pd
import time

# CSVファイルを読み込む
data = pd.read_csv('.\dummydata\dummy_attitude.csv')

# 表示したい行数を指定
num_lines_to_print = 1000  # 例：1000行

# 指定した行数分だけ1秒ごとに表示
for index in range(num_lines_to_print):
    # ソケットを作成する（UDPを使用）
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    row = data.iloc[index]  # 行を取得
    print(f"Pitch: {row['pitch']}, Yaw: {row['yaw']}, Roll: {row['roll']}")
    # JSON形式に変換
    json_data = json.dumps({"numbers": [row['pitch'], row['yaw'], row['roll']]})
    sock.sendto(json_data.encode(), ('localhost', 12345))

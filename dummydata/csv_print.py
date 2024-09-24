import pandas as pd
import time

# CSVファイルを読み込む
data = pd.read_csv('dummy_attitude.csv')

# 表示したい行数を指定
num_lines_to_print = 1000  # 例：1000行

# 指定した行数分だけ1秒ごとに表示
for index in range(num_lines_to_print):
    row = data.iloc[index]  # 行を取得
    print(f"Pitch: {row['pitch']}, Yaw: {row['yaw']}, Roll: {row['roll']}")
    time.sleep(1)  # 1秒待機

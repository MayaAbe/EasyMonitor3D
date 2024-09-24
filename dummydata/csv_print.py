import pandas as pd
import time
from pathlib import Path

# スクリプトのディレクトリを取得
try:
    current_dir = Path(__file__).resolve().parent
except NameError:
    # __file__ が定義されていない場合（例: Jupyter Notebook）
    current_dir = Path.cwd()

# CSVファイルのパスを生成
csv_file_path = current_dir / 'dummy_attitude.csv'

# CSVファイルを読み込む
data = pd.read_csv(csv_file_path)

# 表示したい行数を指定
num_lines_to_print = 1000  # 例：1000行

# 指定した行数分だけ1秒ごとに表示
for index in range(num_lines_to_print):
    row = data.iloc[index]  # 行を取得
    print(f"Pitch: {row['pitch']}, Yaw: {row['yaw']}, Roll: {row['roll']}")
    time.sleep(1)  # 1秒待機

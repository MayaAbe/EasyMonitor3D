import pandas as pd
import numpy as np

# 各列の上限値
pitch_max = 720
yaw_max = 1080
roll_max = 1440

# 行数
num_rows = 1000

# ステップの計算
pitch_step = pitch_max / (num_rows - 1)
yaw_step = yaw_max / (num_rows - 1)
roll_step = roll_max / (num_rows - 1)

# データの生成
pitch = np.arange(0, pitch_max + pitch_step, pitch_step)
yaw = np.arange(0, yaw_max + yaw_step, yaw_step)
roll = np.arange(0, roll_max + roll_step, roll_step)

# DataFrameの作成
data = pd.DataFrame({
    'pitch': pitch,
    'yaw': yaw,
    'roll': roll
})

# CSVファイルとして保存
data.to_csv('dummy_attitude.csv', index=False)

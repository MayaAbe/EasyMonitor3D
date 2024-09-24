import socket
import time
import random
import json

def send_random_numbers(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            # 0～9のランダムな数値を6つ生成
            numbers = [random.randint(0, 9) for _ in range(6)]
            # JSON形式に変換
            json_data = json.dumps({"numbers": numbers})
            sock.sendto(json_data.encode(), server_address)
            print(f"送信したJSONデータ: {json_data}")
            time.sleep(1)  # 1秒間隔で送信
    finally:
        sock.close()

if __name__ == "__main__":
    server_address = ('localhost', 12345)  # 受信側のIPアドレスとポート番号
    send_random_numbers(server_address)

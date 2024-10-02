import subprocess
import time
import os

# 仮想環境のPythonのパスを指定
venv_python = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'python')  # Windowsの場合
# venv_python = os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'python')  # macOS/Linuxの場合

# rotate_texture_udp.py を先に実行
print("Starting rotate_texture_udp.py...")
rotate_process = subprocess.Popen([venv_python, "rotate_texture_udp.py"])

# 少し待ってから attuitude_client.py を実行
time.sleep(5)
print("Starting attuitude_client.py...")
attitude_process = subprocess.Popen([venv_python, "attuitude_client.py"])

# attuitude_client.py の終了を待機
attitude_process.wait()

# attuitude_client.py が終了したら rotate_texture_udp.py を終了
print("attuitude_client.py has completed. Terminating rotate_texture_udp.py...")
time.sleep(10)
rotate_process.terminate()

# rotate_texture_udp.py の終了を待機
rotate_process.wait()

print("Both processes have completed.")

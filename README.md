# Network
姿勢ビューアを通して，UDPネットワークで送られてくる情報を可視化するリポジトリ．

## ファイル構成
|パス|役割|
|----|----|
||メインのプログラムがある．`attitude_client.py`と`rotate_texture_udp.py`が対応している．`rotate_texture_test.py`は単体で使える．|
|`./dummydata`|姿勢を表示する際のダミーデータを格納している．|
|`./images`|オブジェクトのテクスチャや背景に用いる画像を格納している．|
|`./objects`|3Dモデルのオブジェクトを格納している．|
|`./test`|試験的に開発しているコードが入っている．(あまり人に読ませる気はない．)|

## 動作原理
`rotate_texture_udp.py`はUDPサーバとして動作しており，受け取った姿勢データに基づいてオブジェクトを表示する．現在は姿勢データは60fpsで表示される設定になっている．
姿勢データは3つのデータが`[(patch), (roll), (yaw)]`の順番で格納された.json形式で送信されることを想定している．

`attitude_client`が姿勢データを送信している．現在は`./dummydata/dummy_attitude.csv`に格納されている姿勢データを読み取って1行ずつ`.json`に格納して送信している．
リアルタイムでIMUやシミュレータ等が吐き出したデータでも，`json`形式で`rotate_texture_udp.py`のポート番号を指定して送信すれば`rotate_texture_udp.py`は姿勢を表示してくれる．

## 推奨動作環境
インタプリタはPython3.9を使用してください．

## 環境構築

1. リポジトリのクローン
    ```bash
    git clone https://github.com/MayaAbe/Network
    cd Network
    ```
2. Python 3.9 のインストール（必要に応じて）
3. 仮想環境の作成

   ```bash
   python3.9 -m venv venv
   ```


4. 仮想環境の有効化
* Windows:

    ```bash
    venv\Scripts\activate
    ```

* Mac/Linux:
    ```bash
    source venv/bin/activate
    ```
5. 必要なパッケージのインストール
    ```bash
    pip install -r requirements.txt
6. サーバ(3Dビューア)の起動

    `rotate_texture_udp.py`を実行します．
    始めは黒い画面しか映りませんが，データを受信し始めたら3Dビューアが動作し始めます．
7. データ送信プログラムの実行

   `rotate_texture_udp.py`を実行したまま`attitide_client.py`を実行する．
   一つのターミナルではプログラム実行中に他のプログラムを実行することができないので，他のターミナルを立ち上げて実行する．

   ここで，`atitude_client.py`は仮想環境内で実行する必要はない．(本来は仮想環境の外部から送信されるデータを模しているため)

   `atitude_cloent.py`ではダミーの姿勢データが格納されたcsvファイルから姿勢データをUDP通信で送信する．
   本ファイルの関数をコピーして任意のプログラムに組み込めば姿勢ビューアがうまく使える．
# start.py
import os
import sys
import subprocess

def setup_project():
    """プロジェクトのセットアップと起動"""
    print("オセロゲームをセットアップします...")

    # requirements.txtのインストール
    if os.path.exists("requirements.txt"):
        print("パッケージをインストール中...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("requirements.txt が見つかりません")
        return

    # サーバー起動
    print("サーバーを起動中...")
    os.chdir("backend")
    subprocess.run([sys.executable, "othello.py"])

if __name__ == "__main__":
    setup_project()
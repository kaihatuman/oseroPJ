# start.py
import os
import sys
import subprocess

def setup_project():
    """プロジェクトのセットアップと起動"""
    print("オセロゲームをセットアップします...")
    
    # プロジェクトのルートディレクトリをPythonパスに追加
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.environ["PYTHONPATH"] = project_root
    
    # requirements.txtのインストール
    if os.path.exists("requirements.txt"):
        print("パッケージをインストール中...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("requirements.txt が見つかりません")
        return

    # サーバー起動
    print("サーバーを起動中...")
    try:
        import uvicorn
        from backend.othello import app
        uvicorn.run(app, host="localhost", port=8000)
    except Exception as e:
        print(f"サーバーの起動に失敗しました: {e}")

if __name__ == "__main__":
    setup_project()
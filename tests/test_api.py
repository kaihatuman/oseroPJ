from fastapi.testclient import TestClient
from backend.othello import app  # server.py ではなく othello.py から直接インポート
import pytest

client = TestClient(app)

def test_get_initial_board():
    """初期盤面の取得テスト"""
    response = client.get("/board")
    assert response.status_code == 200
    data = response.json()
    assert "board" in data
    assert "current_player" in data
    assert data["current_player"] == "X"

def test_make_valid_move():
    """有効な手のテスト"""
    # まずゲームをリスタート
    client.post("/restart")
    
    response = client.post("/move", json={"row": 2, "col": 3})
    assert response.status_code == 200
    data = response.json()
    assert data["board"][2][3] == "X"

def test_make_invalid_move():
    """無効な手のテスト"""
    response = client.post("/move", json={"row": 0, "col": 0})
    assert response.status_code == 400
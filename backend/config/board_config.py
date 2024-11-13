
TEST_BOARDS = {
    "initial": """
    --------
    --------
    --------
    ---OX---
    ---XO---
    --------
    --------
    --------
    """,
    "mid_game": """
    --------
    --OX----
    --XO----
    --XO----
    --OX----
    --------
    --------
    --------
    """,
    "end_game": """
    XXXXXXOO
    XXXXXXOO
    XXXXXXOO
    XXXXXXOO
    XXXXXXOO
    XXXXXXOO
    XXXXXXO-
    XXXXXXOO
    """,
    "corner_case": """
    X-------
    -O------
    --X-----
    ---O----
    ----X---
    -----O--
    ------X-
    -------O
    """
}

BOARD_DESCRIPTIONS = {
    "initial": "初期配置：中央に4つの石が配置された状態",
    "mid_game": "中盤の一例：垂直方向に石が並んだ状態",
    "end_game": "終盤の一例：ほぼ全ての石が埋まった状態",
    "corner_case": "特殊な配置：対角線上に石が並んだ状態"
}
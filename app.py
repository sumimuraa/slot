import streamlit as st
import random
import time

# ページの基本設定
st.set_page_config(page_title="ストップスロット", page_icon="🎰")

# --- アプリケーションのUIとロジック ---
st.title("🎰 スロットマシン")

# 使用する絵文字のリスト
SYMBOLS = ["🍒", "🍉", "🍋", "🔔", "⭐", "７"]

# --- 状態の初期化 ---
# st.session_stateに各値がなければ初期値を設定
if 'reels' not in st.session_state:
    st.session_state.reels = ["❓", "❓", "❓"]
if 'spinning' not in st.session_state:
    st.session_state.spinning = [False, False, False]
if 'game_over' not in st.session_state:
    st.session_state.game_over = True # 最初はゲームオーバー状態（待機中）

# --- UIの定義 ---
# リールとストップボタンを配置する列
cols = st.columns(3)
placeholders = []

for i, col in enumerate(cols):
    with col:
        # リール表示用のプレースホルダー
        placeholders.append(st.empty())

        # ストップボタン
        # 対応するリールが回転中(spinning[i] is True)の時だけボタンを有効化
        if st.button(f"ストップ", key=f"stop_{i}", disabled=not st.session_state.spinning[i]):
            st.session_state.spinning[i] = False
            # 全てのリールが止まったかチェック
            if not any(st.session_state.spinning):
                st.session_state.game_over = True
            st.rerun()


# --- ゲーム進行のメインコントロール ---

# ゲームオーバー状態（待機中 or 結果表示中）の時の処理
if st.session_state.game_over:
    # 待機中ではなく、結果表示中の場合
    if st.session_state.reels != ["❓", "❓", "❓"]:
        # 当たり判定
        if len(set(st.session_state.reels)) == 1:
            st.success("🎉🎉🎉 大当たり！おめでとうございます！ 🎉🎉🎉")
            st.balloons()
        else:
            st.info("残念！もう一度挑戦してみよう。")

    # 「スピン！」または「もう一度！」ボタン
    if st.button("スピン！", use_container_width=True):
        st.session_state.reels = [random.choice(SYMBOLS) for _ in range(3)]
        st.session_state.spinning = [True, True, True]
        st.session_state.game_over = False
        st.rerun() # 状態を更新して再実行

# --- リールのアニメーションと表示 ---

# 回転中のリールがある場合、アニメーションを実行
needs_rerun = False
for i in range(3):
    if st.session_state.spinning[i]:
        # 回転中のリールの絵文字をランダムに変更
        st.session_state.reels[i] = random.choice(SYMBOLS)
        needs_rerun = True

    # プレースホルダーに現在の絵文字を表示
    placeholders[i].markdown(
        f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.reels[i]}</h1>",
        unsafe_allow_html=True
    )

# 1つでも回転中のリールがあれば、ページを再実行してアニメーションに見せる
if needs_rerun:
    time.sleep(0.1) # アニメーションの速度調整
    st.rerun()

st.markdown("---")
st.info("「スピン！」で開始し、各リールの下の「ストップ」ボタンで止めよう！")

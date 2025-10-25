import streamlit as st
import random

st.title("🎲 グループ分けBOT")

# メンバー入力欄
members_input = st.text_area("メンバーを入力してください（カンマ、全角スペース、半角スペース区切りOK）", "")

# 区切りを統一して分割
def parse_members(text):
    # 全角スペース → 半角スペース、カンマ → スペースに統一
    text = text.replace("　", " ").replace(",", " ")
    # スペースで分割して空白除去
    members = [m.strip() for m in text.split() if m.strip()]
    return members

# 半角数字を全角に変換
def to_zenkaku(num):
    table = str.maketrans({
        "0": "０", "1": "１", "2": "２", "3": "３", "4": "４",
        "5": "５", "6": "６", "7": "７", "8": "８", "9": "９"
    })
    return str(num).translate(table)

# グループサイズを指定
group_size = st.number_input("1グループの人数", min_value=2, max_value=4, value=4, step=1)

# グループ分け処理
if st.button("🎯 グループ分けする") or st.button("🔁 振り分け直す"):
    members = parse_members(members_input)

    if not members:
        st.warning("⚠ メンバーを入力してください。")
    else:
        random.shuffle(members)
        groups = [members[i:i + group_size] for i in range(0, len(members), group_size)]

        for i, group in enumerate(groups, start=1):
            group_text = ", ".join(group)
            zenkaku_num = to_zenkaku(i)
            st.markdown(f"### #パーティー{zenkaku_num}テキスト\n{group_text}")

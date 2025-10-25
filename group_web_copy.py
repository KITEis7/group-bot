import streamlit as st
import random

st.title("わけわけ")

members_input = st.text_area(
    "メンバーを入力してください（カンマ、半角スペース、全角スペース区切りOK）", ""
)

def parse_members(text):
    text = text.replace("　", " ").replace(",", " ")
    return [m.strip() for m in text.split() if m.strip()]

def to_zenkaku(num):
    table = str.maketrans({
        "0":"０","1":"１","2":"２","3":"３","4":"４",
        "5":"５","6":"６","7":"７","8":"８","9":"９"
    })
    return str(num).translate(table)

def make_groups(members):
    total = len(members)
    random.shuffle(members)
    best_groups = []
    for n_groups in range(1, total + 1):
        size = total // n_groups
        if size < 2 or size > 4:
            continue
        remainder = total % n_groups
        groups, idx = [], 0
        for i in range(n_groups):
            gsize = size + (1 if i < remainder else 0)
            groups.append(members[idx:idx + gsize])
            idx += gsize
        best_groups = groups
        break
    return best_groups

# グループ分けボタン
if st.button("🎯 グループ分けする"):
    members = parse_members(members_input)
    if not members:
        st.warning("⚠ メンバーを入力してください。")
    elif len(members) < 2:
        st.warning("⚠ 2人以上必要です。")
    else:
        groups = make_groups(members)
        lines = []
        for i, group in enumerate(groups, start=1):
            znum = to_zenkaku(i)
            lines.append(f"#パーティー{znum}テキスト " + ", ".join(group))
        result_text = "\n".join(lines)

        # 結果表示（Ctrl+Cで確実にコピー）
        st.text_area("結果（Ctrl+Cでコピーしてください）", value=result_text, height=250)

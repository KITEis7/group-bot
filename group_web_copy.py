import streamlit as st
import random

st.title("わけわけボット")

# セッションステートでメンバーと結果を保持
if 'members' not in st.session_state:
    st.session_state.members = []
if 'result_text' not in st.session_state:
    st.session_state.result_text = ""

# メンバー入力
members_input = st.text_area("メンバーをカンマ区切りで入力してください", ",".join(st.session_state.members))

# メンバーリスト更新
if members_input.strip() != "":
    st.session_state.members = [m.strip() for m in members_input.split(",") if m.strip()]

def make_groups(members):
    members = members[:]
    random.shuffle(members)
    groups = []
    while len(members) > 0:
        if len(members) >= 4:
            group_size = 4
        elif len(members) == 3:
            group_size = 3
        elif len(members) == 2:
            group_size = 2
        else:  # 残り1人
            groups[-1].append(members.pop(0))
            break
        group = [members.pop(0) for _ in range(group_size)]
        groups.append(group)
    return groups

def generate_result():
    groups = make_groups(st.session_state.members)
    result_text = ""
    for i, g in enumerate(groups, 1):
        result_text += f"#パーティー{i} " + ", ".join(g) + "\n"
    st.session_state.result_text = result_text

# ボタン
col1, col2 = st.columns(2)
if col1.button("グループ分け"):
    generate_result()
if col2.button("振り分け直し"):
    generate_result()

# 結果表示
st.text_area("結果", st.session_state.result_text, height=200)

# クリップボードコピー（ブラウザ依存）
if st.button("コピー"):
    st.experimental_set_query_params(copy=st.session_state.result_text)
    st.success("クリップボードにコピーされました（ブラウザ依存）")

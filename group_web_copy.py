import streamlit as st
import random
import html

st.title("わけわけBOT")

members_input = st.text_area(
    "メンバーを入力してください（カンマ、全角スペース、半角スペース区切りOK）", ""
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
    best_groups = None
    min_diff = float("inf")
    for n_groups in range(1, total+1):
        size = total // n_groups
        if size < 2 or size > 4:
            continue
        remainder = total % n_groups
        groups = []
        idx = 0
        for i in range(n_groups):
            gsize = size + (1 if i < remainder else 0)
            groups.append(members[idx:idx+gsize])
            idx += gsize
        diff = max(len(g) for g in groups) - min(len(g) for g in groups)
        if diff < min_diff:
            min_diff = diff
            best_groups = groups
    return best_groups

if st.button("🎯 グループ分けする") or st.button("🔁 振り分け直す"):
    members = parse_members(members_input)
    if not members:
        st.warning("⚠ メンバーを入力してください。")
    elif len(members) < 2:
        st.warning("⚠ 2人以上必要です。")
    else:
        groups = make_groups(members)
        all_text_lines = []
        for i, group in enumerate(groups, start=1):
            zenkaku_num = to_zenkaku(i)
            line = f"#パーティー{zenkaku_num}テキスト " + ", ".join(group)
            all_text_lines.append(line)
        all_text = "\n".join(all_text_lines)

        # 表示用
        st.text_area("結果", value=all_text, height=200)

        # コピー用 HTML + JS
        escaped_text = html.escape(all_text)
        st.markdown(f"""
        <textarea id="copy_area" style="display:none;">{escaped_text}</textarea>
        <button onclick="
        const ta = document.getElementById('copy_area');
        ta.style.display='block';
        ta.select();
        document.execCommand('copy');
        ta.style.display='none';
        alert('✅ コピーしました！');
        ">📋 まとめてコピー</button>
        """, unsafe_allow_html=True)

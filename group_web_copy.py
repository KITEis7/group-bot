import streamlit as st
import random
import streamlit.components.v1 as components

# --- グループ分け関数 ---
def make_groups(names, min_size=2, max_size=4):
    random.shuffle(names)
    n = len(names)
    group_count = max(1, round(n / ((min_size + max_size) / 2)))
    base_size = n // group_count
    remainder = n % group_count

    groups = []
    start = 0
    for i in range(group_count):
        size = base_size + (1 if i < remainder else 0)
        groups.append(names[start:start+size])
        start += size
    return groups

# --- Streamlit GUI ---
st.title("グループ分けBot（コピーボタン付き）")

names_input = st.text_area("名前をカンマ区切りで入力：", height=100)

if st.button("グループ分け実行"):
    if not names_input.strip():
        st.warning("名前を入力してください")
    else:
        names = [n.strip() for n in names_input.split(",") if n.strip()]
        groups = make_groups(names)

        # 結果を作成
        result_text = ""
        for i, g in enumerate(groups, 1):
            full_width_num = str(i).translate(str.maketrans("0123456789", "０１２３４５６７８９"))
            line = f"#パーティー{full_width_num}テキスト\n{', '.join(g)}"
            result_text += line + "\n\n"

        # テキスト表示
        st.text_area("結果", value=result_text, height=200, key="result_area")

        # コピー用HTMLボタン
        copy_button_html = f"""
        <input type="button" value="コピー" onclick="navigator.clipboard.writeText(`{result_text}`)" />
        <p>コピー後はCtrl+Vで貼り付け可能です。</p>
        """
        components.html(copy_button_html, height=60)

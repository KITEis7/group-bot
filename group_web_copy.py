import streamlit as st
import random

st.title("わけわけBOT")

# メンバー入力欄
members_input = st.text_area(
    "メンバーを入力してください（カンマ、全角スペース、半角スペース区切りOK）", ""
)

# 区切りを統一して分割
def parse_members(text):
    text = text.replace("　", " ").replace(",", " ")
    members = [m.strip() for m in text.split() if m.strip()]
    return members

# 半角数字を全角に変換
def to_zenkaku(num):
    table = str.maketrans({
        "0": "０","1":"１","2":"２","3":"３","4":"４",
        "5":"５","6":"６","7":"７","8":"８","9":"９"
    })
    return str(num).translate(table)

# 2〜4人で均等に分ける関数
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
        group_sizes = [len(g) for g in groups]
        diff = max(group_sizes) - min(group_sizes)
        if diff < min_diff:
            min_diff = diff
            best_groups = groups
    return best_groups

# JSコピー関数
st.markdown("""
<script>
function copyToClipboard(text) {
  navigator.clipboard.writeText(text);
  alert("✅ コピーしました！");
}
</script>
""", unsafe_allow_html=True)

# グループ分けボタン
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
        st.text_area("結果", value=all_text, height=200)

        # まとめコピー
        js_text_all = all_text.replace("`", "'").replace("\n", "\\n")
        st.markdown(
            f'<button onclick="copyToClipboard(`{js_text_all}`)" style="margin-top:10px;">📋 まとめてコピー</button>',
            unsafe_allow_html=True
        )

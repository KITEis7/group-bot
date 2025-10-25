import streamlit as st
import random
import html

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
        "0": "０", "1": "１", "2": "２", "3": "３", "4": "４",

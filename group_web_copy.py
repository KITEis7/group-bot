import os

# 入力フォルダと出力フォルダを指定
input_folder = "input_txt"
output_folder = "output_txt"

# 出力フォルダが存在しない場合は作成
os.makedirs(output_folder, exist_ok=True)

# ファイルを処理
for i, filename in enumerate(sorted(os.listdir(input_folder)), start=1):
    if filename.endswith(".txt"):
        # 入力ファイルを読み込み
        input_path = os.path.join(input_folder, filename)
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # 区切り文字を統一して分割（カンマ、全角スペース、半角スペース対応）
        members = [m.strip() for m in content.replace("　", " ").replace(",", " ").split() if m.strip()]

        # 出力内容を作成（全角数字ではなく半角数字を使用）
        output_text = f"#パーティー{i}テキスト\n" + ", ".join(members) + "\n"

        # 出力ファイルに書き込み
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_text)

print("✅ 変換完了しました！")

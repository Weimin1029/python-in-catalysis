def convert_to_utf8(input_file, output_file):
    # 尝试用常见编码打开文件
    encodings = ["utf-8", "gbk", "latin-1"]
    for encoding in encodings:
        try:
            with open(input_file, "r", encoding=encoding) as file:
                content = file.read()
            # 以 UTF-8 编码保存文件
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"文件已成功转换为 UTF-8 编码并保存为 {output_file}")
            return
        except UnicodeDecodeError:
            continue
    print("无法识别文件编码，请手动检查文件编码。")

# 示例文件路径
input_file = "alloy_alkaline.txt"
output_file = "alloy_alkaline_utf8.txt"

# 转换文件编码
convert_to_utf8(input_file, output_file)
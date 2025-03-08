import chardet
import csv
import matplotlib.pyplot as plt
import numpy as np

def count_metals_in_file(file_path, metals):
    try:
        # 尝试用 UTF-8 打开文件
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        try:
            # 如果 UTF-8 失败，尝试用 GBK 打开文件
            with open(file_path, "r", encoding="gbk") as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            # 如果 GBK 也失败，使用 chardet 检测编码
            with open(file_path, "rb") as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                file_encoding = result["encoding"]
            with open(file_path, "r", encoding=file_encoding) as file:
                lines = file.readlines()

    # 记录每一行中每个金属元素出现的次数
    results = []
    # 全局统计每个金属元素出现的总次数
    total_counts = {metal: 0 for metal in metals}

    for line in lines:
        line = line.strip()  # 去除换行符和空格
        metal_count = {}
        i = 0
        while i < len(line):
            # 检查单个字符的元素（如 C, O）
            if i + 1 <= len(line) and line[i] in metals:
                element = line[i]
                metal_count[element] = metal_count.get(element, 0) + 1
                total_counts[element] += 1
                i += 1
            # 检查两个字符的元素（如 Pt, Co）
            elif i + 2 <= len(line) and line[i:i+2] in metals:
                element = line[i:i+2]
                metal_count[element] = metal_count.get(element, 0) + 1
                total_counts[element] += 1
                i += 2
            else:
                i += 1
        results.append(metal_count)

    return results, total_counts

def save_to_csv(data, output_file):
    """
    将数据保存为 CSV 文件
    :param data: 字典形式的数据，键为元素，值为出现次数
    :param output_file: 输出文件路径
    """
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(["Element", "Count"])
        # 写入数据
        for element, count in data:
            writer.writerow([element, count])

def plot_bar_chart(data, output_image):
    """
    绘制柱状图并保存为 PNG 文件
    :param data: 排序后的金属元素及其出现次数
    :param output_image: 输出图片文件路径
    """
    # 过滤出现次数大于等于 1 的元素
    filtered_data = [(element, count) for element, count in data if count >= 1]
    elements = [item[0] for item in filtered_data]  # 元素名称
    counts = [item[1] for item in filtered_data]    # 出现次数

    # 如果没有数据，直接返回
    if not elements:
        print("没有出现次数大于等于 1 的金属元素。")
        return

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    bars = plt.bar(elements, counts, color=plt.cm.tab20.colors[:len(elements)])

    # 在每个柱上方标注元素名称
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # x 坐标
            height + 0.1,                       # y 坐标
            bar.get_height(),                   # 标注的值
            ha="center",                       # 水平居中
            va="bottom"                        # 垂直对齐
        )

    # 设置图表标题和标签
    plt.title("Metal Element Counts (Count >= 1)")
    plt.xlabel("Element")
    plt.ylabel("Count")
    plt.xticks(rotation=45)  # 旋转 x 轴标签
    plt.tight_layout()       # 自动调整布局

    # 保存图表为 PNG 文件
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    print(f"柱状图已保存为 {output_image}")

    # 显示图表
    plt.show()

# 示例文件路径
file_path = "alloy_alkaline_utf8.txt"
output_csv = "metal_counts1.csv"
output_image = "metal_counts1.png"
metals = [
    "Mg", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh",
    "Fl", "Mc", "Lv", "Ts", "Og", "Al", "Ga", "In", "Sn", "Tl", "Pb", "Bi", "Po", "La", "Ce", "Pr", "Nd", "Pm", "Sm",
    "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf",
    "Es", "Fm", "Md", "No", "Lr"
]

# 统计金属元素出现的次数
metal_counts, total_counts = count_metals_in_file(file_path, metals)

# 输出每一行的统计结果
for i, counts in enumerate(metal_counts):
    print(f"第 {i + 1} 行中金属元素出现的次数: {counts}")

# 按出现的总次数排序
sorted_total_counts = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)

# 输出全局统计结果（按出现次数从高到低排序）
print("\n全局统计结果（按出现次数从高到低排序）:")
for metal, count in sorted_total_counts:
    if count > 0:
        print(f"{metal}: {count}")

# 将结果保存为 CSV 文件
save_to_csv(sorted_total_counts, output_csv)
print(f"\n结果已保存到 {output_csv}")

# 绘制柱状图并保存为 PNG 文件
plot_bar_chart(sorted_total_counts, output_image)
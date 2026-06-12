import pandas as pd
import sys
import io

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取示例Excel
df = pd.read_excel('example/2026年1月媒体摘录.xlsx', header=1)

print(f"总行数: {len(df)}\n")
print("前40行中的图文链接（非tv.cctv.com）：\n")

for i, row in df.head(40).iterrows():
    link = str(row['链接'])
    if pd.notna(row['链接']) and 'tv.cctv.com' not in link:
        print(f"第{i+1}行: {row['媒体名称']} - {link}")

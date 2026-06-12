import pandas as pd
import sys
import io

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取示例Excel，跳过第一行标题
df = pd.read_excel('example/2026年1月媒体摘录.xlsx', header=1)

print("第31行数据:")
row = df.iloc[30]  # 第31行（索引从0开始）
for col in df.columns:
    value = row[col]
    if pd.notna(value):
        print(f"{col}: {value}")

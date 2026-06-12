import pandas as pd
import sys
import io

# 设置UTF-8编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取示例Excel，跳过第一行标题
df = pd.read_excel('example/2026年1月媒体摘录.xlsx', header=1)

print("Excel列名:")
print(df.columns.tolist())
print("\n数据行数:", len(df))
print("\n前5行数据预览:")
for idx, row in df.head(5).iterrows():
    print(f"\n=== 行 {idx} ===")
    for col in df.columns:
        value = row[col]
        if pd.notna(value):
            print(f"{col}: {value}")

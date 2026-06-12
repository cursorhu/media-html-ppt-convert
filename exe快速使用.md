# exe快速使用指南

## 🚀 使用方法

### 方法1：使用默认路径

1. 在exe所在目录创建 `input` 文件夹
2. 将Excel文件放入input文件夹，命名为 `媒体摘录.xlsx`
3. 运行exe

```bash
媒体摘要PPT生成器.exe
```

### 方法2：指定Excel文件路径（推荐）

直接指定Excel文件路径，不需要创建input文件夹：

```bash
# 使用相对路径
媒体摘要PPT生成器.exe --excel "example\2026年1月媒体摘录.xlsx"

# 使用绝对路径
媒体摘要PPT生成器.exe --excel "D:\data\我的媒体摘录.xlsx"

# 测试模式
媒体摘要PPT生成器.exe --excel "example\2026年1月媒体摘录.xlsx" --test
```

## 📁 文件结构

### 最简结构（使用--excel参数）
```
媒体摘要PPT生成器.exe
你的Excel文件.xlsx
```

运行：
```bash
媒体摘要PPT生成器.exe --excel "你的Excel文件.xlsx"
```

### 标准结构（使用默认路径）
```
媒体摘要PPT生成器.exe
input/
  └── 媒体摘录.xlsx
output/           # 自动创建
  └── 媒体摘录.pptx
```

运行：
```bash
媒体摘要PPT生成器.exe
```

## 💡 常用命令

```bash
# 1. 处理指定Excel文件
媒体摘要PPT生成器.exe --excel "D:\data\新闻摘录.xlsx"

# 2. 测试模式（处理前5条）
媒体摘要PPT生成器.exe --excel "test.xlsx" --test

# 3. 处理指定行数
媒体摘要PPT生成器.exe --excel "data.xlsx" --limit 20

# 4. 使用默认路径
媒体摘要PPT生成器.exe
```

## ❓ 常见问题

### Q1: 提示"Excel文件不存在"

**解决方法**：
1. 检查文件路径是否正确
2. 使用绝对路径：`--excel "D:\完整\路径\文件.xlsx"`
3. 路径包含空格要加引号

### Q2: 不想创建input文件夹

**解决方法**：
使用 `--excel` 参数直接指定文件路径

```bash
媒体摘要PPT生成器.exe --excel "你的文件.xlsx"
```

### Q3: Excel文件名不是"媒体摘录.xlsx"

**解决方法**：
使用 `--excel` 参数指定任意文件名

```bash
媒体摘要PPT生成器.exe --excel "我的新闻摘录2026.xlsx"
```

## 📝 完整示例

假设你的Excel文件在桌面：

```bash
cd Desktop
媒体摘要PPT生成器.exe --excel "新闻摘录.xlsx"
```

输出：
- `output/媒体摘录.pptx` - 生成的PPT
- `process.log` - 处理日志

## ⚙️ 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--excel` | 指定Excel文件路径 | `--excel "data.xlsx"` |
| `--test` | 测试模式（3视频+2图文） | `--test` |
| `--limit` | 限制处理行数 | `--limit 10` |

## ✅ 推荐使用方式

**最简单**：
```bash
媒体摘要PPT生成器.exe --excel "你的文件.xlsx"
```

**先测试**：
```bash
媒体摘要PPT生成器.exe --excel "你的文件.xlsx" --test
```

**正式处理**：
```bash
媒体摘要PPT生成器.exe --excel "你的文件.xlsx"
```

---

**提示**：首次使用建议先用 `--test` 模式验证效果！

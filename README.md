# 媒体摘要PPT生成器

将Excel中的媒体摘录数据自动转化为PPT演示文稿。

## 功能特性

- 📊 从Excel读取媒体摘录数据
- 🎬 自动识别视频链接，截取关键画面
- 📄 自动识别图文链接，截图并提取摘要
- 📑 生成排版美观的PPT文件
- 🔄 失败重试机制，保证稳健性
- 📝 详细日志记录

## 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：需要安装Chrome浏览器和ChromeDriver。

### ChromeDriver安装

1. 检查Chrome版本：打开Chrome浏览器 -> 设置 -> 关于Chrome
2. 下载对应版本的ChromeDriver：https://chromedriver.chromium.org/downloads
3. 将chromedriver.exe放到系统PATH目录或项目根目录

## 使用方法

### 测试模式（处理前5行）

```bash
python main.py --test
```

### 处理所有数据

```bash
python main.py
```

### 处理指定行数

```bash
python main.py --limit 10
```

## 项目结构

```
html-to-ppt/
├── main.py                 # 主程序
├── config.py              # 配置文件
├── utils.py               # 工具函数
├── excel_reader.py        # Excel读取模块
├── content_analyzer.py    # 内容类型识别
├── webpage_scraper.py     # 网页抓取模块
├── ppt_generator.py       # PPT生成模块
├── requirements.txt       # 依赖库
├── example/              # 示例文件
│   ├── 2026年1月媒体摘录.xlsx
│   └── 2026年1月媒体摘录.pptx
├── output/               # 输出目录
├── temp/                 # 临时文件目录
└── process.log          # 日志文件
```

## 配置说明

可在 `config.py` 中修改：

- `REQUEST_TIMEOUT`: 网络请求超时时间（秒）
- `MAX_RETRIES`: 失败重试次数
- `PAGE_LOAD_WAIT`: 页面加载等待时间（秒）
- `SUMMARY_MAX_LENGTH`: 摘要最大字符数
- `IMAGE_MAX_WIDTH/HEIGHT`: 图片最大尺寸（英寸）

## 工作原理

1. **读取Excel**：从Excel文件读取媒体名称、标题、发布时间、链接等信息
2. **内容识别**：判断链接是视频还是图文类型
3. **网页抓取**：
   - 视频：截取视频播放器画面
   - 图文：截取页面并提取文本摘要
4. **生成PPT**：将文字信息和视觉内容组合成PPT页面
5. **保存输出**：生成完整的PPT文件

## 注意事项

- 需要稳定的网络连接
- 某些网站可能有反爬虫机制，导致抓取失败
- 视频网站可能需要额外的等待时间才能截取到画面
- 建议先使用测试模式验证效果

## 常见问题

### 1. ChromeDriver版本不匹配

**错误信息**：`This version of ChromeDriver only supports Chrome version XX`

**解决方法**：下载与Chrome浏览器版本匹配的ChromeDriver

### 2. 页面截图为空白

**原因**：页面加载时间不足

**解决方法**：增加 `config.py` 中的 `PAGE_LOAD_WAIT` 值

### 3. 部分页面抓取失败

**原因**：网站反爬虫或网络问题

**解决方法**：程序会继续处理其他数据，失败的条目会记录在日志中

## 许可证

MIT License

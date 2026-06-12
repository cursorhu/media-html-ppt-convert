# 配置文件
import os
import sys

# 文件路径配置
# 打包后使用exe所在目录，开发时使用脚本目录
if getattr(sys, 'frozen', False):
    # 打包后的exe环境
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 开发环境
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 目录配置
INPUT_DIR = os.path.join(BASE_DIR, 'input')
EXAMPLE_DIR = os.path.join(BASE_DIR, 'example')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# 默认Excel路径（用于向后兼容，实际使用时会自动扫描input目录）
EXCEL_PATH = os.path.join(INPUT_DIR, '媒体摘录.xlsx')
OUTPUT_PPT = os.path.join(OUTPUT_DIR, '媒体摘录.pptx')

# 网络请求配置
REQUEST_TIMEOUT = 30  # 秒
MAX_RETRIES = 3
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# 内容抓取配置
PAGE_LOAD_WAIT = 3  # 页面加载等待时间（秒）
VIDEO_AD_WAIT = 30  # 视频广告等待时间（秒）
SCREENSHOT_WIDTH = 1920
SCREENSHOT_HEIGHT = 1080

# 摘要配置
SUMMARY_MAX_LENGTH = 300  # 摘要最大字符数

# PPT配置
PPT_SLIDE_WIDTH = 10  # 英寸
PPT_SLIDE_HEIGHT = 7.5
IMAGE_MAX_WIDTH = 8  # 图片最大宽度（英寸）
IMAGE_MAX_HEIGHT = 5  # 图片最大高度（英寸）

# 日志配置
LOG_FILE = os.path.join(BASE_DIR, 'process.log')
LOG_LEVEL = 'INFO'

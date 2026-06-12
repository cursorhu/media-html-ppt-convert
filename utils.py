import logging
import time
import os
from functools import wraps
from config import LOG_FILE, LOG_LEVEL, MAX_RETRIES, TEMP_DIR

# 设置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def retry_on_failure(max_retries=MAX_RETRIES, delay=2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"{func.__name__} 第{attempt + 1}次尝试失败: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            logger.error(f"{func.__name__} 失败，已重试{max_retries}次")
            raise last_exception
        return wrapper
    return decorator

def ensure_dir(directory):
    """确保目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"创建目录: {directory}")

def cleanup_temp_files():
    """清理临时文件"""
    if os.path.exists(TEMP_DIR):
        for file in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.warning(f"清理临时文件失败: {file_path}, 错误: {e}")

# 初始化必要的目录
ensure_dir(os.path.dirname(LOG_FILE))
ensure_dir(TEMP_DIR)
ensure_dir(os.path.dirname(os.path.join(os.path.dirname(__file__), 'output', 'temp')))

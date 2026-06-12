import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils import logger, retry_on_failure
from config import (
    REQUEST_TIMEOUT, PAGE_LOAD_WAIT, VIDEO_AD_WAIT, SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT, USER_AGENT, TEMP_DIR, SUMMARY_MAX_LENGTH
)

class WebpageScraper:
    """网页抓取器"""

    def __init__(self):
        self.driver = None

    def _init_driver(self):
        """初始化Selenium浏览器"""
        if self.driver:
            return

        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f'--window-size={SCREENSHOT_WIDTH},{SCREENSHOT_HEIGHT}')
            chrome_options.add_argument(f'user-agent={USER_AGENT}')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(REQUEST_TIMEOUT)
            logger.info("Selenium浏览器初始化成功")
        except Exception as e:
            logger.error(f"初始化浏览器失败: {e}")
            raise

    @retry_on_failure(max_retries=2)
    def scrape_webpage(self, url, content_type='article'):
        """
        抓取网页内容

        Args:
            url: 网页链接
            content_type: 内容类型 ('video' 或 'article')

        Returns:
            dict: {
                'screenshot': 截图文件路径,
                'summary': 文本摘要 (仅图文)
            }
        """
        self._init_driver()
        result = {'screenshot': None, 'summary': ''}

        try:
            logger.info(f"开始抓取网页: {url}")
            self.driver.get(url)

            # 等待页面加载
            time.sleep(PAGE_LOAD_WAIT)

            # 对于视频页面，等待让广告播放完毕
            if content_type == 'video':
                logger.info(f"视频页面，等待{VIDEO_AD_WAIT}秒让广告播放完毕")
                time.sleep(VIDEO_AD_WAIT)

            # 截图
            timestamp = int(time.time() * 1000)
            screenshot_path = os.path.join(TEMP_DIR, f'screenshot_{timestamp}.png')

            if content_type == 'video':
                # 视频页面：尝试截取视频播放器区域
                result['screenshot'] = self._capture_video_frame(screenshot_path)
            else:
                # 图文页面：截取整个页面
                self.driver.save_screenshot(screenshot_path)
                result['screenshot'] = screenshot_path
                logger.info(f"页面截图保存: {screenshot_path}")

                # 提取文本摘要
                result['summary'] = self._extract_summary()

            return result

        except Exception as e:
            logger.error(f"抓取网页失败: {url}, 错误: {e}")
            raise

    def _capture_video_frame(self, screenshot_path):
        """截取视频播放器画面"""
        try:
            # 尝试关闭广告/弹窗
            try:
                # 常见的关闭按钮选择器
                close_selectors = [
                    '.close', '.closeBtn', '.ad-close',
                    '[class*="close"]', '[class*="Close"]',
                    'button[title*="关闭"]', 'button[aria-label*="关闭"]'
                ]
                for selector in close_selectors:
                    try:
                        close_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if close_btn.is_displayed():
                            close_btn.click()
                            logger.info(f"关闭了广告/弹窗: {selector}")
                            time.sleep(1)
                            break
                    except:
                        continue
            except Exception as e:
                logger.debug(f"尝试关闭广告时出错: {e}")

            # 尝试找到视频播放器元素
            video_selectors = [
                'video',
                '.video-player',
                '#video',
                '.player',
                'iframe[src*="player"]',
            ]

            video_element = None
            for selector in video_selectors:
                try:
                    video_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if video_element:
                        break
                except:
                    continue

            if video_element:
                # 截取视频元素
                video_element.screenshot(screenshot_path)
                logger.info(f"视频播放器截图保存: {screenshot_path}")
            else:
                # 降级方案：截取整个页面
                logger.warning("未找到视频播放器元素，使用整页截图")
                self.driver.save_screenshot(screenshot_path)

            return screenshot_path

        except Exception as e:
            logger.warning(f"视频截图失败，使用整页截图: {e}")
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path

    def _extract_summary(self):
        """提取页面文本摘要"""
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            # 移除干扰元素
            for element in soup(['script', 'style', 'nav', 'footer', 'header',
                                'aside', 'iframe', 'noscript', 'button']):
                element.decompose()

            # 移除常见的导航、侧边栏、评论区等元素（通过class/id特征）
            noise_patterns = [
                'nav', 'menu', 'sidebar', 'side-bar', 'comment',
                'footer', 'header', 'toolbar', 'breadcrumb',
                'social', 'share', 'related', 'recommend', 'hot',
                'ad', 'advertisement', 'banner', 'popup'
            ]

            for pattern in noise_patterns:
                for element in soup.find_all(class_=lambda x: x and pattern in x.lower()):
                    element.decompose()
                for element in soup.find_all(id=lambda x: x and pattern in x.lower()):
                    element.decompose()

            # 优先尝试提取正文内容
            content_selectors = [
                'article',
                '.article-content',
                '.article_content',
                '.article-body',
                '.content-body',
                '#artibody',  # 新浪等
                '.left_zw',   # 中国新闻网
                '.cnt_bd',    # 腾讯
                'main article',
                '.post-content',
                '#content',
            ]

            text = ''
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    # 提取文本前再次清理内部的干扰元素
                    for noise in element.find_all(class_=lambda x: x and any(p in x.lower() for p in ['share', 'related', 'comment', 'editor'])):
                        noise.decompose()

                    text = element.get_text(separator='\n', strip=True)
                    if len(text) > 100:  # 确保提取到足够的文本
                        logger.info(f"使用选择器 '{selector}' 提取到内容")
                        break

            # 如果没找到，尝试找最长的p标签集合
            if not text or len(text) < 100:
                paragraphs = soup.find_all('p')
                # 过滤掉太短的段落（可能是导航或页脚）
                valid_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
                if valid_paragraphs:
                    text = '\n'.join(valid_paragraphs)
                    logger.info(f"使用p标签集合提取到 {len(valid_paragraphs)} 个段落")

            # 清理文本
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            # 过滤掉过短的行（可能是导航链接）和重复行
            filtered_lines = []
            seen = set()
            for line in lines:
                if len(line) > 10 and line not in seen:  # 至少10个字符
                    filtered_lines.append(line)
                    seen.add(line)

            text = '\n'.join(filtered_lines)

            # 截取摘要
            if len(text) > SUMMARY_MAX_LENGTH:
                text = text[:SUMMARY_MAX_LENGTH] + '...'

            logger.info(f"提取文本摘要，长度: {len(text)}")
            return text

        except Exception as e:
            logger.warning(f"提取文本摘要失败: {e}")
            return ''

    def close(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("浏览器已关闭")
            except:
                pass
            self.driver = None

    def __del__(self):
        """析构函数"""
        self.close()

if __name__ == '__main__':
    # 测试代码
    scraper = WebpageScraper()
    try:
        result = scraper.scrape_webpage(
            'https://tv.cctv.com/2025/12/31/VIDEoaGQNS9CZPXgHufwOnUe251231.shtml',
            content_type='video'
        )
        print(result)
    finally:
        scraper.close()

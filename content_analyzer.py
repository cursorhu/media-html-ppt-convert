from urllib.parse import urlparse
from utils import logger

class ContentAnalyzer:
    """内容类型分析器"""

    @staticmethod
    def is_video_link(url):
        """
        判断是否为视频链接

        Args:
            url: 链接地址

        Returns:
            bool: True表示视频链接
        """
        if not url:
            return False

        # CCTV视频特征
        if 'tv.cctv.com' in url:
            return True

        # 其他视频网站特征
        video_domains = [
            'youku.com',
            'bilibili.com',
            'iqiyi.com',
            'qq.com/video',
            'v.qq.com',
            'youtube.com',
            'video',  # 通用video关键词
        ]

        url_lower = url.lower()
        for domain in video_domains:
            if domain in url_lower:
                return True

        return False

    @staticmethod
    def get_content_type(url):
        """
        获取内容类型

        Args:
            url: 链接地址

        Returns:
            str: 'video' 或 'article'
        """
        if ContentAnalyzer.is_video_link(url):
            logger.info(f"识别为视频链接: {url}")
            return 'video'
        else:
            logger.info(f"识别为图文链接: {url}")
            return 'article'

if __name__ == '__main__':
    # 测试代码
    test_urls = [
        'https://tv.cctv.com/2025/12/31/VIDEoaGQNS9CZPXgHufwOnUe251231.shtml',
        'https://www.example.com/news/article.html',
        'https://www.bilibili.com/video/BV1xx411c7XD',
    ]

    for url in test_urls:
        content_type = ContentAnalyzer.get_content_type(url)
        print(f"{url} -> {content_type}")

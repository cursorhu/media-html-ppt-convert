#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：测试图文和视频两种类型
"""

import sys
import os
from excel_reader import ExcelReader
from content_analyzer import ContentAnalyzer
from webpage_scraper import WebpageScraper
from ppt_generator import PPTGenerator
from utils import logger, cleanup_temp_files
from tqdm import tqdm

def test_mixed_content():
    """测试视频和图文混合内容"""

    logger.info("=" * 50)
    logger.info("测试模式：视频+图文")
    logger.info("=" * 50)

    scraper = None

    try:
        # 1. 读取Excel
        reader = ExcelReader()
        all_rows = reader.get_rows()

        # 选择测试数据：前3条视频 + 2条图文
        # 第29行是中国新闻网的图文链接
        video_rows = all_rows[0:3]  # 前3条视频
        article_rows = [all_rows[23], all_rows[28]]  # 第24行(人民日报)和第29行(中国新闻网)
        test_rows = video_rows + article_rows

        print(f"\n选择了 {len(test_rows)} 条测试数据：")
        for i, row in enumerate(test_rows, 1):
            content_type = ContentAnalyzer.get_content_type(row['link'])
            print(f"{i}. [{content_type}] {row['media_name']} - {row['title'][:30]}...")

        # 2. 初始化
        ppt_gen = PPTGenerator('output/测试_视频图文混合.pptx')
        scraper = WebpageScraper()

        # 3. 处理数据
        print("\n开始处理...\n")
        for idx, row in enumerate(tqdm(test_rows, desc="处理进度"), 1):
            try:
                logger.info(f"\n处理第 {idx}/{len(test_rows)} 行")
                logger.info(f"标题: {row.get('title', '')}")
                logger.info(f"链接: {row.get('link', '')}")

                # 分析内容类型
                url = row.get('link', '')
                content_type = ContentAnalyzer.get_content_type(url)

                # 抓取网页内容
                scrape_result = {'screenshot': None, 'summary': ''}
                try:
                    scrape_result = scraper.scrape_webpage(url, content_type)
                except Exception as e:
                    logger.error(f"抓取网页失败: {e}")

                # 准备幻灯片数据
                slide_data = {
                    'media_name': row.get('media_name', ''),
                    'title': row.get('title', ''),
                    'publish_time': row.get('publish_time', ''),
                    'link': url,
                    'screenshot': scrape_result.get('screenshot'),
                    'summary': scrape_result.get('summary', row.get('remark', ''))
                }

                # 添加到PPT
                ppt_gen.add_slide(slide_data)
                logger.info(f"第 {idx} 行处理成功")

            except Exception as e:
                logger.error(f"第 {idx} 行处理失败: {e}")
                continue

        # 4. 保存PPT
        output_path = ppt_gen.save()

        # 5. 清理
        cleanup_temp_files()

        print(f"\n测试完成！")
        print(f"输出文件: {output_path}")

    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        print(f"\n测试失败: {e}")
        sys.exit(1)

    finally:
        if scraper:
            scraper.close()

if __name__ == '__main__':
    test_mixed_content()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
媒体摘要PPT生成器 - 主程序

功能：将Excel中的媒体摘录数据转化为PPT
"""

import sys
import os
from tqdm import tqdm
from excel_reader import ExcelReader
from content_analyzer import ContentAnalyzer
from webpage_scraper import WebpageScraper
from ppt_generator import PPTGenerator
from utils import logger, cleanup_temp_files
from config import OUTPUT_PPT

def main(limit=None, test_mode=False, args=None):
    """
    主流程

    Args:
        limit: 限制处理的行数，None表示处理所有行
        test_mode: 测试模式，选择包含视频和图文的混合数据
        args: 命令行参数
    """
    logger.info("=" * 50)
    logger.info("媒体摘要PPT生成器启动")
    logger.info("=" * 50)

    scraper = None
    success_count = 0
    fail_count = 0

    try:
        # 1. 读取Excel
        logger.info("步骤1: 读取Excel文件")

        # 如果用户通过--excel指定了路径，使用指定路径
        if args.excel:
            reader = ExcelReader(excel_path=args.excel)
        else:
            # 否则自动扫描input目录
            reader = ExcelReader()

        if test_mode:
            # 测试模式：选择视频和图文混合数据
            all_rows = reader.get_rows()
            # 前3条视频 + 2条图文（第24行人民日报，第29行中国新闻网）
            rows = all_rows[0:3] + [all_rows[23], all_rows[28]]
            logger.info("测试模式：选择了3条视频 + 2条图文")
        else:
            rows = reader.get_rows(limit=limit)

        total = len(rows)
        logger.info(f"共读取 {total} 行数据")

        if total == 0:
            logger.warning("没有数据需要处理")
            return

        # 2. 初始化PPT生成器
        logger.info("步骤2: 初始化PPT生成器")
        output_file = 'output/测试_媒体摘录.pptx' if test_mode else OUTPUT_PPT
        ppt_gen = PPTGenerator(output_file)

        # 3. 初始化网页抓取器
        logger.info("步骤3: 初始化网页抓取器")
        scraper = WebpageScraper()

        # 4. 处理每一行数据
        logger.info("步骤4: 开始处理数据并生成PPT")

        for idx, row in enumerate(tqdm(rows, desc="处理进度"), 1):
            try:
                logger.info(f"\n处理第 {idx}/{total} 行")
                logger.info(f"标题: {row.get('title', '')[:50]}")
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
                    # 继续处理，使用空的抓取结果

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
                success_count += 1
                logger.info(f"✓ 第 {idx} 行处理成功")

            except Exception as e:
                fail_count += 1
                logger.error(f"✗ 第 {idx} 行处理失败: {e}")
                # 继续处理下一行
                continue

        # 5. 保存PPT
        logger.info("\n步骤5: 保存PPT文件")
        output_path = ppt_gen.save()

        # 6. 清理临时文件
        logger.info("步骤6: 清理临时文件")
        cleanup_temp_files()

        # 7. 输出统计信息
        logger.info("\n" + "=" * 50)
        logger.info("处理完成！")
        logger.info(f"成功: {success_count} 行")
        logger.info(f"失败: {fail_count} 行")
        logger.info(f"输出文件: {output_path}")
        logger.info("=" * 50)

        print(f"\nPPT生成成功！")
        print(f"  输出文件: {output_path}")
        print(f"  成功: {success_count}/{total} 行")
        if fail_count > 0:
            print(f"  失败: {fail_count} 行（请查看日志）")

    except Exception as e:
        logger.error(f"程序执行失败: {e}", exc_info=True)
        print(f"\n程序执行失败: {e}")
        sys.exit(1)

    finally:
        # 确保关闭浏览器
        if scraper:
            scraper.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='媒体摘要PPT生成器')
    parser.add_argument('--excel', type=str, default=None,
                      help='指定Excel文件路径（可选），如：--excel "D:/data/媒体摘录.xlsx"。不指定则自动扫描input目录')
    parser.add_argument('--limit', type=int, default=None,
                      help='限制处理的行数（测试用），不指定则处理所有行')
    parser.add_argument('--test', action='store_true',
                      help='测试模式，处理3条视频+2条图文（包含视频和图文两种类型）')

    args = parser.parse_args()

    if args.test:
        print(f"测试模式：处理3条视频 + 2条图文数据")
        main(test_mode=True, args=args)
    else:
        if args.limit:
            print(f"限制模式：只处理前 {args.limit} 行数据")
        main(limit=args.limit, args=args)

# -*- coding: utf-8 -*-
"""
PyInstaller打包脚本
"""

import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',                          # 主程序入口
    '--name=media_ppt_converter',       # 生成的exe名称（改为英文）
    '--onefile',                        # 打包成单个exe文件
    '--console',                        # 显示控制台窗口
    '--icon=NONE',                      # 图标（如果有的话）
    # 不再打包example，改为input目录（用户自己创建）
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=pptx',
    '--hidden-import=selenium',
    '--hidden-import=bs4',
    '--hidden-import=PIL',
    '--hidden-import=cv2',
    '--hidden-import=lxml',
    '--hidden-import=tqdm',
    '--collect-all=selenium',
    '--collect-all=pptx',
    f'--distpath={os.path.join(current_dir, "dist")}',
    f'--workpath={os.path.join(current_dir, "build")}',
    f'--specpath={current_dir}',
])

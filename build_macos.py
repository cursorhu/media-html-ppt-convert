# -*- coding: utf-8 -*-
"""
macOS PyInstaller打包脚本
必须在 macOS 系统上运行（或通过 GitHub Actions）
"""

import PyInstaller.__main__
import os
import sys

if sys.platform != 'darwin':
    print(f"警告：此脚本设计为在 macOS 上运行，当前平台：{sys.platform}")
    print("在 GitHub Actions 中，此脚本将在 macos-latest runner 上执行")

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',                          # 主程序入口
    '--name=media_ppt_converter',       # 生成的可执行文件名称（改为英文）
    '--onefile',                        # 打包成单个可执行文件
    '--console',                        # 显示控制台窗口（CLI工具）
    '--icon=NONE',                      # 图标（如果有的话）
    # 隐式导入（确保依赖被打包）
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=pptx',
    '--hidden-import=selenium',
    '--hidden-import=bs4',
    '--hidden-import=PIL',
    '--hidden-import=cv2',
    '--hidden-import=lxml',
    '--hidden-import=tqdm',
    # 收集所有相关数据文件
    '--collect-all=selenium',
    '--collect-all=pptx',
    # 输出路径
    f'--distpath={os.path.join(current_dir, "dist")}',
    f'--workpath={os.path.join(current_dir, "build")}',
    f'--specpath={current_dir}',
])

print("\n=== macOS 构建完成 ===")
print(f"可执行文件位置：{os.path.join(current_dir, 'dist', 'media_ppt_converter')}")
print("\n使用方法：")
print("  ./dist/media_ppt_converter --excel input/your_file.xlsx")

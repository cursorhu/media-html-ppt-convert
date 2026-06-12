import pandas as pd
import os
import glob
from utils import logger
from config import EXCEL_PATH, INPUT_DIR

class ExcelReader:
    """Excel读取器"""

    def __init__(self, excel_path=None):
        """
        初始化Excel读取器

        Args:
            excel_path: Excel文件路径，如果为None则自动查找input目录下的Excel文件
        """
        if excel_path:
            self.excel_path = excel_path
        else:
            # 自动查找input目录下的Excel文件
            self.excel_path = self._find_excel_file()

        self.df = None

    def _find_excel_file(self):
        """自动查找input目录下的Excel文件"""
        # 检查input目录是否存在
        if not os.path.exists(INPUT_DIR):
            logger.warning(f"input目录不存在，尝试创建: {INPUT_DIR}")
            try:
                os.makedirs(INPUT_DIR)
                logger.info(f"已创建input目录: {INPUT_DIR}")
            except:
                pass

        # 查找所有Excel文件
        excel_patterns = [
            os.path.join(INPUT_DIR, '*.xlsx'),
            os.path.join(INPUT_DIR, '*.xls')
        ]

        excel_files = []
        for pattern in excel_patterns:
            excel_files.extend(glob.glob(pattern))

        if not excel_files:
            # 如果input目录没有，尝试example目录
            from config import EXAMPLE_DIR
            if os.path.exists(EXAMPLE_DIR):
                example_pattern = os.path.join(EXAMPLE_DIR, '*.xlsx')
                excel_files = glob.glob(example_pattern)
                if excel_files:
                    logger.info(f"在example目录找到Excel文件: {excel_files[0]}")
                    return excel_files[0]

            # 都没找到，返回默认路径并提示
            logger.error("未找到Excel文件！")
            logger.error(f"请将Excel文件（.xlsx或.xls）放入: {INPUT_DIR}")
            logger.error("或使用 --excel 参数指定文件路径")
            raise FileNotFoundError(f"未在 {INPUT_DIR} 目录找到Excel文件")

        # 如果找到多个文件，使用第一个
        selected_file = excel_files[0]
        if len(excel_files) > 1:
            logger.warning(f"找到多个Excel文件，使用: {os.path.basename(selected_file)}")
            logger.warning(f"其他文件将被忽略: {[os.path.basename(f) for f in excel_files[1:]]}")
        else:
            logger.info(f"自动找到Excel文件: {os.path.basename(selected_file)}")

        return selected_file

    def read(self):
        """读取Excel文件"""
        try:
            # 检查文件是否存在
            if not os.path.exists(self.excel_path):
                logger.error(f"Excel文件不存在: {self.excel_path}")
                logger.error("请确保：")
                logger.error("1. 创建了 input 文件夹")
                logger.error("2. 将Excel文件放入 input 文件夹")
                logger.error("3. 或使用 --excel 参数指定文件路径")
                raise FileNotFoundError(f"Excel文件不存在: {self.excel_path}")

            # 跳过第一行标题，从第二行开始读取
            self.df = pd.read_excel(self.excel_path, header=1)
            logger.info(f"成功读取Excel文件: {self.excel_path}")
            logger.info(f"数据行数: {len(self.df)}")
            logger.info(f"列名: {self.df.columns.tolist()}")
            return self.df
        except Exception as e:
            logger.error(f"读取Excel文件失败: {e}")
            raise

    def get_rows(self, limit=None):
        """
        获取数据行

        Args:
            limit: 限制返回的行数，None表示返回所有行

        Returns:
            list of dict: 每行数据的字典列表
        """
        if self.df is None:
            self.read()

        # 选择需要的列
        columns_map = {
            '序号': 'index',
            '媒体名称': 'media_name',
            '发布时间': 'publish_time',
            '标题': 'title',
            '链接': 'link',
            '备注': 'remark'
        }

        rows = []
        df_subset = self.df.head(limit) if limit else self.df

        for idx, row in df_subset.iterrows():
            row_data = {}
            for col_name, key in columns_map.items():
                if col_name in self.df.columns:
                    value = row[col_name]
                    # 处理NaN值
                    if pd.isna(value):
                        value = ''
                    elif col_name == '发布时间':
                        # 格式化日期
                        try:
                            value = pd.to_datetime(value).strftime('%Y-%m-%d')
                        except:
                            value = str(value)
                    else:
                        value = str(value)
                    row_data[key] = value

            # 只添加有链接的行
            if row_data.get('link'):
                rows.append(row_data)

        logger.info(f"提取了{len(rows)}行有效数据")
        return rows

if __name__ == '__main__':
    # 测试代码
    reader = ExcelReader()
    rows = reader.get_rows(limit=5)
    for i, row in enumerate(rows, 1):
        print(f"\n=== 第{i}行 ===")
        for key, value in row.items():
            print(f"{key}: {value}")

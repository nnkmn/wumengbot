import pandas as pd
import numpy as np
from loguru import logger
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os

from wumeng_crawler.config.config import BASE_DIR

class DataProcessor:
    """
    数据处理器，用于清洗、整合和格式化爬取到的数据
    """
    
    def __init__(self):
        """
        初始化数据处理器
        """
        self.logger = logger
        self.logger.info("初始化数据处理器")
        
        # 创建数据处理目录
        self.processed_data_dir = os.path.join(BASE_DIR, "processed_data")
        os.makedirs(self.processed_data_dir, exist_ok=True)
        
    def clean_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        清洗数据
        
        Args:
            data: 爬取到的数据列表
            
        Returns:
            清洗后的数据列表
        """
        self.logger.info(f"开始清洗数据，共 {len(data)} 条")
        
        cleaned_data = []
        
        for item in data:
            # 移除空值
            cleaned_item = {k: v for k, v in item.items() if v is not None}
            
            # 去除字符串两端的空格
            for k, v in cleaned_item.items():
                if isinstance(v, str):
                    cleaned_item[k] = v.strip()
                elif isinstance(v, list):
                    # 清洗列表中的字符串
                    cleaned_item[k] = [
                        (item.strip() if isinstance(item, str) else item)
                        for item in v
                    ]
            
            # 标准化日期时间格式
            if "crawl_time" in cleaned_item:
                try:
                    if isinstance(cleaned_item["crawl_time"], str):
                        # 尝试解析日期时间字符串
                        cleaned_item["crawl_time"] = datetime.strptime(
                            cleaned_item["crawl_time"], "%Y-%m-%d %H:%M:%S"
                        )
                except ValueError as e:
                    self.logger.warning(f"解析日期时间失败: {e}")
            
            cleaned_data.append(cleaned_item)
        
        # 去重
        cleaned_data = self._remove_duplicates(cleaned_data)
        
        self.logger.info(f"数据清洗完成，共清洗 {len(cleaned_data)} 条数据")
        return cleaned_data
    
    def _remove_duplicates(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        移除重复数据
        
        Args:
            data: 数据列表
            
        Returns:
            去重后的数据列表
        """
        if not data:
            return data
        
        # 使用pandas去重
        df = pd.DataFrame(data)
        
        # 选择合适的列作为去重依据
        # 这里可以根据实际情况调整
        if "site" in df.columns and "domain" in df.columns and "title" in df.columns:
            df.drop_duplicates(subset=["site", "domain", "title"], keep="last", inplace=True)
        
        return df.to_dict(orient="records")
    
    def integrate_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        整合数据
        
        Args:
            data: 清洗后的数据列表
            
        Returns:
            整合后的数据字典
        """
        self.logger.info("开始整合数据")
        
        # 将数据转换为DataFrame
        df = pd.DataFrame(data)
        
        # 按站点分组
        grouped_data = {}
        
        if "site" in df.columns:
            for site, group in df.groupby("site"):
                grouped_data[site] = group.to_dict(orient="records")
        else:
            grouped_data["all"] = data
        
        self.logger.info(f"数据整合完成，共整合 {len(grouped_data)} 个站点的数据")
        return grouped_data
    
    def format_data(self, data: Dict[str, Any], format_type: str = "json") -> Any:
        """
        格式化数据
        
        Args:
            data: 整合后的数据字典
            format_type: 格式化类型，可选值：json、csv、excel
            
        Returns:
            格式化后的数据
        """
        self.logger.info(f"开始格式化数据，格式类型: {format_type}")
        
        if format_type == "json":
            return self._format_to_json(data)
        elif format_type == "csv":
            return self._format_to_csv(data)
        elif format_type == "excel":
            return self._format_to_excel(data)
        else:
            self.logger.error(f"不支持的格式化类型: {format_type}")
            return None
    
    def _format_to_json(self, data: Dict[str, Any]) -> str:
        """
        格式化为JSON字符串
        
        Args:
            data: 整合后的数据字典
            
        Returns:
            JSON字符串
        """
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)
    
    def _format_to_csv(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        格式化为CSV字符串
        
        Args:
            data: 整合后的数据字典
            
        Returns:
            站点名称到CSV字符串的映射字典
        """
        csv_data = {}
        
        for site, items in data.items():
            if items:
                df = pd.DataFrame(items)
                csv_data[site] = df.to_csv(index=False, encoding="utf-8")
        
        return csv_data
    
    def _format_to_excel(self, data: Dict[str, Any]) -> bytes:
        """
        格式化为Excel文件
        
        Args:
            data: 整合后的数据字典
            
        Returns:
            Excel文件的字节流
        """
        import io
        
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            for site, items in data.items():
                if items:
                    df = pd.DataFrame(items)
                    df.to_excel(writer, sheet_name=site[:31], index=False)  # Excel工作表名称最多31个字符
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def save_processed_data(self, data: Any, format_type: str = "json", filename: Optional[str] = None) -> str:
        """
        保存处理后的数据
        
        Args:
            data: 处理后的数据
            format_type: 格式化类型
            filename: 文件名，不包含扩展名
            
        Returns:
            保存的文件路径
        """
        self.logger.info(f"开始保存处理后的数据，格式类型: {format_type}")
        
        # 生成文件名
        if filename is None:
            filename = f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 根据格式类型保存文件
        if format_type == "json":
            file_path = os.path.join(self.processed_data_dir, f"{filename}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)
        elif format_type == "csv":
            # 保存多个CSV文件
            for site, csv_content in data.items():
                file_path = os.path.join(self.processed_data_dir, f"{filename}_{site}.csv")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(csv_content)
        elif format_type == "excel":
            file_path = os.path.join(self.processed_data_dir, f"{filename}.xlsx")
            with open(file_path, "wb") as f:
                f.write(data)
        else:
            self.logger.error(f"不支持的格式化类型: {format_type}")
            return ""
        
        self.logger.info(f"处理后的数据保存成功，保存路径: {file_path}")
        return file_path
    
    def load_data(self, file_path: str) -> Any:
        """
        加载数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            加载的数据
        """
        self.logger.info(f"开始加载数据，文件路径: {file_path}")
        
        # 根据文件扩展名选择加载方式
        _, ext = os.path.splitext(file_path)
        
        if ext.lower() == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif ext.lower() == ".csv":
            data = pd.read_csv(file_path).to_dict(orient="records")
        elif ext.lower() in [".xlsx", ".xls"]:
            data = pd.read_excel(file_path).to_dict(orient="records")
        else:
            self.logger.error(f"不支持的文件类型: {ext}")
            return None
        
        self.logger.info(f"数据加载成功，共 {len(data)} 条")
        return data
    
    def process(self, data: List[Dict[str, Any]], format_type: str = "json", save: bool = False) -> Any:
        """
        完整的数据处理流程
        
        Args:
            data: 爬取到的数据列表
            format_type: 格式化类型
            save: 是否保存处理后的数据
            
        Returns:
            处理后的数据
        """
        self.logger.info("开始完整的数据处理流程")
        
        # 清洗数据
        cleaned_data = self.clean_data(data)
        
        # 整合数据
        integrated_data = self.integrate_data(cleaned_data)
        
        # 格式化数据
        formatted_data = self.format_data(integrated_data, format_type)
        
        # 保存数据
        if save:
            self.save_processed_data(formatted_data, format_type)
        
        self.logger.info("数据处理流程完成")
        return formatted_data

# 单例模式
_data_processor_instance = None

def get_data_processor() -> DataProcessor:
    """
    获取数据处理器实例
    
    Returns:
        数据处理器实例
    """
    global _data_processor_instance
    if _data_processor_instance is None:
        _data_processor_instance = DataProcessor()
    return _data_processor_instance
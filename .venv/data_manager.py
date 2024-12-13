import csv
import logging
import os
from datetime import datetime

class DataManager:
    def __init__(self, base_dir='.venv'):
        """初始化数据管理器"""
        # 设置基础目录
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, 'data')
        self.log_dir = os.path.join(base_dir, 'logs')
        
        # 确保必要的目录存在
        self._ensure_directories()
        
        # 设置日志文件路径
        self.log_file = os.path.join(self.log_dir, 'printer_assistant.log')
        self.data_file = os.path.join(self.data_dir, 'print_records.csv')
        
        # 初始化日志系统
        self._setup_logging()
        
        # CSV文件的列名
        self.csv_headers = ['timestamp', 'user_name', 'project_name', 'email', 'status']
        
        # 确保CSV文件存在并包含表头
        self._ensure_csv_file()
    
    def _ensure_directories(self):
        """确保所需的目录结构存在"""
        for dir_path in [self.data_dir, self.log_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logging.info(f"创建目录: {dir_path}")
    
    def _setup_logging(self):
        """配置日志系统"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()  # 同时输出到控制台
            ]
        )
    
    def _ensure_csv_file(self):
        """确保CSV文件存在并包含正确的表头"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.csv_headers)
                logging.info(f"创建数据文件: {self.data_file}")
    
    def save_print_record(self, user_name, project_name, email, status="开始打印"):
        """保存打印记录到CSV文件"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            record = [timestamp, user_name, project_name, email, status]
            
            with open(self.data_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(record)
            
            logging.info(f"保存打印记录 - 用户: {user_name}, 项目: {project_name}")
            return True
        except Exception as e:
            logging.error(f"保存记录失败: {str(e)}")
            return False
    
    def get_user_history(self, email=None):
        """获取用户的打印历史记录"""
        try:
            records = []
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if email is None or row['email'] == email:
                        records.append(row)
            return records
        except Exception as e:
            logging.error(f"读取历史记录失败: {str(e)}")
            return []
    
    def get_recent_records(self, limit=10):
        """获取最近的打印记录"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = list(csv.DictReader(file))
                return reader[-limit:] if reader else []
        except Exception as e:
            logging.error(f"读取最近记录失败: {str(e)}")
            return []
    
    def update_print_status(self, user_name, project_name, email, new_status):
        """更新打印状态"""
        try:
            self.save_print_record(user_name, project_name, email, new_status)
            logging.info(f"更新打印状态 - 用户: {user_name}, 项目: {project_name}, 状态: {new_status}")
            return True
        except Exception as e:
            logging.error(f"更新状态失败: {str(e)}")
            return False 
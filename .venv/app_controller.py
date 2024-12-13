import subprocess
import psutil
import time
import logging
import os
from typing import Optional
import winreg  # 用于在Windows注册表中搜索应用
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

class AppController:
    """应用程序控制器，用于管理外部应用程序的启动和关闭"""
    
    def __init__(self, app_name: str, app_path: str = None):
        """
        初始化应用程序控制器
        
        Args:
            app_name (str): 应用程序名称（例如：'bamboo.exe'）
            app_path (str, optional): 应用程序的完整路径，如果提供则优先使用
        """
        self.app_name = app_name
        
        # 设置日志
        self._setup_logging()
        
        # 如果提供了路径，验证路径是否有效
        if app_path and os.path.exists(app_path):
            self.app_path = app_path
            self.logger.info(f"使用指定路径: {self.app_path}")
        else:
            # 如果路径无效或未提供，尝试搜索
            if app_path:
                self.logger.warning(f"指定的路径无效: {app_path}，将尝试自动搜索")
            self.app_path = self._find_app_path(app_name)
            
            if self.app_path:
                self.logger.info(f"找到应用程序路径: {self.app_path}")
            else:
                self.logger.warning(f"未找到应用程序: {app_name}")
        
        self.process: Optional[subprocess.Popen] = None
        self.start_time: Optional[float] = None
    
    def _find_app_path(self, app_name: str) -> Optional[str]:
        """
        在系统中搜索应用程序的完整路径
        
        Args:
            app_name (str): 应用程序名称
            
        Returns:
            Optional[str]: 应用程序的完整路径，如果未找到则返回None
        """
        try:
            # 常见的应用程序安装路径
            common_paths = [
                os.environ.get('ProgramFiles', 'C:/Program Files'),
                os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)'),
                os.environ.get('LOCALAPPDATA', ''),
                os.environ.get('APPDATA', ''),
                "D:/",  # 添加其他可能的安装路径
                "E:/"
            ]
            
            # 在常见路径中搜索
            for base_path in common_paths:
                if not base_path or not os.path.exists(base_path):
                    continue
                    
                self.logger.debug(f"搜索目录: {base_path}")
                for root, _, files in os.walk(base_path):
                    # 检查是否包含关键字（不区分大小写）
                    for file in files:
                        if app_name.lower() in file.lower():
                            found_path = os.path.join(root, file)
                            self.logger.info(f"找到匹配的应用程序: {found_path}")
                            return found_path
            
            # 在系统PATH中搜索
            if 'PATH' in os.environ:
                for path in os.environ['PATH'].split(os.pathsep):
                    if not os.path.exists(path):
                        continue
                        
                    for file in os.listdir(path):
                        if app_name.lower() in file.lower():
                            found_path = os.path.join(path, file)
                            if os.path.exists(found_path):
                                self.logger.info(f"在PATH中找到应用程序: {found_path}")
                                return found_path
            
            self.logger.warning(f"未找到应用程序: {app_name}")
            return None
            
        except Exception as e:
            self.logger.error(f"搜索应用程序时发生错误: {str(e)}")
            return None
    
    def _setup_logging(self):
        """配置日志系统"""
        self.logger = logging.getLogger('AppController')
        self.logger.setLevel(logging.INFO)
        
        # 确保日志目录存在
        log_dir = '.venv/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # 如果logger没有处理器，添加一个
        if not self.logger.handlers:
            log_path = os.path.join(log_dir, 'app_controller.log')
            handler = logging.FileHandler(log_path, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def start_app(self, app_path: str = None) -> bool:
        """
        启动应用程序
        
        Args:
            app_path (str, optional): 应用程序路径，如果不提供则使用初始化时的路径
            
        Returns:
            bool: 启动成功返回True，否则返回False
        """
        try:
            # 检查应用是否已经在运行
            if self.is_running(self.app_name):
                self.logger.info(f"应用程序已在运行: {self.app_name}")
                return True  # 直接返回True，不显示提示
            
            # 首先尝试使用指定路径启动
            path_to_use = app_path or self.app_path
            if path_to_use and os.path.exists(path_to_use):
                self.process = subprocess.Popen(path_to_use)
                self.start_time = time.time()
                self.logger.info(f"应用程序已启动: {path_to_use}")
                
                # 启动定时关闭功能
                self._start_auto_close_timer()
                
                return True
            
            # 如果指定路径无效，尝试搜索并启动
            self.logger.warning(f"指定路径无效: {path_to_use}，尝试搜索应用程序")
            found_path = self._find_app_path(self.app_name)
            
            if found_path:
                self.app_path = found_path  # 更新找到的路径
                self.process = subprocess.Popen(found_path)
                self.start_time = time.time()
                self.logger.info(f"通过搜索找到并启动应用程序: {found_path}")
                
                # 启动定时关闭功能
                self._start_auto_close_timer()
                
                return True
            
            # 如果都失败了，记录错误并返回
            self.logger.error("无法找到或启动应用程序")
            return False
            
        except Exception as e:
            self.logger.error(f"启动应用程序失败: {str(e)}")
            return False
    
    def _start_auto_close_timer(self):
        """启动定时关闭功能"""
        if hasattr(self, 'auto_close_minutes') and self.auto_close_minutes > 0:
            timer = threading.Timer(self.auto_close_minutes * 60, self._close_app)
            timer.start()
            self.logger.info(f"应用程序将在 {self.auto_close_minutes} 分钟后自动关闭")

    def _close_app(self):
        """关闭应用程序"""
        if self.process:
            self.process.terminate()
            self.logger.info("应用程序已自动关闭")
    
    def close_app(self, process_name: str = None) -> bool:
        """
        关闭应用程序
        
        Args:
            process_name (str, optional): 进程名称，如果不提供则使用启动的进程
            
        Returns:
            bool: 关闭成功返回True，否则返回False
        """
        try:
            if process_name:
                # 通过进程名关闭
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] == process_name:
                        proc.terminate()
                        proc.wait(timeout=5)
                        self.logger.info(f"已关闭进程: {process_name}")
                return True
            
            elif self.process:
                # 关闭启动的进程
                self.process.terminate()
                self.process.wait(timeout=5)
                self.logger.info("已关闭启动的应用程序")
                return True
            
            else:
                raise ValueError("没有可关闭的应用程序")
            
        except Exception as e:
            self.logger.error(f"关闭应用程序失败: {str(e)}")
            return False
    
    def is_running(self, process_name: str = None) -> bool:
        """
        检查应用程序是否在运行
        
        Args:
            process_name (str, optional): 进程名称，如果不提供则检查启动的进程
            
        Returns:
            bool: 如果程序在运行返回True，否则返回False
        """
        try:
            if process_name:
                # 通过进程名检查
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] == process_name:
                        return True
                return False
            
            elif self.process:
                # 检查启动的进程
                return self.process.poll() is None
            
            return False
            
        except Exception as e:
            self.logger.error(f"检查应用程序状态失败: {str(e)}")
            return False
    
    def get_running_time(self) -> Optional[float]:
        """
        获取应用程序运行时间（秒）
        
        Returns:
            float or None: 运行时间（秒），如果程序未运行则返回None
        """
        if self.start_time and self.is_running():
            return time.time() - self.start_time
        return None
    
    def auto_close_after(self, minutes: int, process_name: str = None):
        """
        设置定时关闭
        
        Args:
            minutes (int): 多少分钟后关闭
            process_name (str, optional): 要关闭的进程名称
        """
        def delayed_close():
            time.sleep(minutes * 60)
            self.close_app(process_name)
        
        # 在新线程中执行延迟关闭
        import threading
        thread = threading.Thread(target=delayed_close)
        thread.daemon = True  # 设置为守护线程，这样主程序退出时线程也会退出
        thread.start() 
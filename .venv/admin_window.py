import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import hashlib
import json
import os
import csv

class AdminWindow:
    """管理员窗口类"""
    def __init__(self, app_controller=None):
        self.login_window = None
        self.admin_panel = None
        self.password_entry = None
        self.app_controller = app_controller
        
        # 加载管理员密码
        self.admin_password = self._load_admin_password()
    
    def show_login(self):
        """显示登录窗口"""
        # 如果已经有登录窗口，就先关闭
        if self.login_window:
            self.login_window.destroy()
        
        # 创建新的登录窗口
        self.login_window = tk.Toplevel()
        self.login_window.title('管理员登录')
        self.login_window.geometry('400x200')
        
        # 设置窗口居中
        self._center_window(self.login_window)
        
        # 创建登录界面
        self._create_login_widgets()
    
    def _center_window(self, window):
        """将窗口居中显示"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_login_widgets(self):
        """创建登录界面组件"""
        frame = ttk.Frame(self.login_window, padding="20")
        frame.pack(fill='both', expand=True)
        
        # 密码输入框
        ttk.Label(frame, text="请输入管理员密码:", font=('Arial', 12)).pack(pady=(0, 10))
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 20))
        
        # 登录按钮
        ttk.Button(frame, text="登录", command=self._verify_password).pack()
        
        # 绑定回车键
        self.password_entry.bind('<Return>', lambda e: self._verify_password())
    
    def _load_admin_password(self):
        """加载管理员密码"""
        try:
            if os.path.exists('admin_config.json'):
                with open('admin_config.json', 'r') as f:
                    config = json.load(f)
                    return config.get('password_hash')
            else:
                # 默认密码的哈希值（默认密码：admin123）
                default_hash = hashlib.sha256('admin123'.encode()).hexdigest()
                with open('admin_config.json', 'w') as f:
                    json.dump({'password_hash': default_hash}, f)
                return default_hash
        except Exception as e:
            print(f"加载管理员密码失败: {e}")
            return None
    
    def _verify_password(self):
        """验证密码"""
        entered_password = self.password_entry.get()
        if not entered_password:
            messagebox.showwarning("警告", "请输入密码！")
            return
        
        # 计算输入密码的哈希值
        entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        
        if entered_hash == self.admin_password:
            self.login_window.destroy()
            self._open_admin_panel()
        else:
            messagebox.showerror("错误", "密码错误！")
            self.password_entry.delete(0, tk.END)
    
    def _open_admin_panel(self):
        """打开管理员控制面板"""
        self.admin_panel = tk.Toplevel()
        self.admin_panel.title('管理员控制面板')
        self.admin_panel.geometry('800x600')
        self._center_window(self.admin_panel)
        
        # 创建管理面板界面
        self._create_admin_panel_widgets()
        
        # 显示最新的5条记录
        self._view_records()
    
    def _create_admin_panel_widgets(self):
        """创建管理面板界面组件"""
        main_frame = ttk.Frame(self.admin_panel, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        ttk.Label(
            main_frame, 
            text="3D打印机管理系统", 
            font=('Arial', 16, 'bold')
        ).pack(pady=(0, 20))
        
        # 应用程序路径设置区域
        self.app_frame = ttk.LabelFrame(main_frame, text="应用程序路径设置", padding=10)
        self.app_frame.pack(fill='x', pady=(0, 20))
        
        # 路径输入框
        path_frame = ttk.Frame(self.app_frame)
        path_frame.pack(fill='x', pady=5)
        
        ttk.Label(
            path_frame,
            text="应用程序路径:",
            font=('Arial', 12)
        ).pack(side='left', padx=(0, 10))
        
        self.app_path_entry = ttk.Entry(path_frame, width=50, font=('Arial', 12))
        self.app_path_entry.pack(side='left', padx=(0, 10))
        
        # 加载当前应用程序路径
        self._load_current_app_path()
        
        # 按钮框架
        button_frame = ttk.Frame(self.app_frame)
        button_frame.pack(fill='x', pady=5)
        
        # 打开应用按钮
        ttk.Button(
            button_frame,
            text="打开应用",
            command=self._open_app
        ).pack(side='left', padx=5)
        
        # 保存路径按钮
        ttk.Button(
            button_frame,
            text="保存路径",
            command=self._save_app_path
        ).pack(side='left', padx=5)
        
        # 定时关闭设置
        ttk.Label(
            main_frame,
            text="自动关闭时间（分钟）:",
            font=('Arial', 12)
        ).pack(pady=(10, 0))
        
        self.auto_close_entry = ttk.Entry(main_frame, width=10, font=('Arial', 12))
        self.auto_close_entry.pack(pady=(0, 10))
        
        # 加载当前定时关闭时间
        self._load_auto_close_time()
        
        # 保存定时关闭时间按钮
        ttk.Button(
            main_frame,
            text="保存定时关闭时间",
            command=self._save_auto_close_time
        ).pack(pady=(0, 20))
        
        # 密码修改区域
        self._create_password_change_widgets(main_frame)
        
        # 记录显示区域
        self.record_frame = ttk.LabelFrame(main_frame, text="使用记录", padding=10)
        self.record_frame.pack(fill='both', expand=True, pady=10)
        
        # 记录显示文本框
        self.record_text = tk.Text(self.record_frame, wrap='word', height=15)
        self.record_text.pack(fill='both', expand=True)
    
    def _view_records(self):
        """查看使用记录"""
        try:
            # 清空当前显示
            self.record_text.delete(1.0, tk.END)
            
            # 读取CSV文件中的记录
            with open('.venv/data/print_records.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                records = list(reader)
                
                # 获取最新的5条记录
                latest_records = records[-5:]
                
                # 显示记录
                for record in latest_records:
                    self.record_text.insert(tk.END, ', '.join(record) + '\n')
        
        except Exception as e:
            messagebox.showerror("错误", f"读取记录失败: {str(e)}")
    
    def _load_app_path(self):
        """加载保存的应用程序路径"""
        try:
            if os.path.exists('admin_config.json'):
                with open('admin_config.json', 'r') as f:
                    config = json.load(f)
                    saved_path = config.get('app_path', '')
                    if saved_path:
                        self.app_path_entry.insert(0, saved_path)
        except Exception as e:
            print(f"加载应用程序路径失败: {e}")
    
    def _load_current_app_path(self):
        """加载当前应用程序路径"""
        # 首先尝试从 AppController 获取当前路径
        if self.app_controller and self.app_controller.app_path:
            self.app_path_entry.insert(0, self.app_controller.app_path)
        else:
            # 如果没有当前路径，则尝试从配置文件加载
            self._load_app_path()
    
    def _save_app_path(self):
        """保存应用程序路径"""
        try:
            path = self.app_path_entry.get().strip()
            if not path:
                messagebox.showwarning("警告", "请输入应用程序路径！")
            return
        
            # 验证路径是否存在
            if not os.path.exists(path):
                messagebox.showerror("错误", "指定的路径不存在！")
                return
            
            # 更新 AppController 的路径
            if self.app_controller:
                self.app_controller.app_path = path
            
            # 读取现有配置
            config = {}
            if os.path.exists('admin_config.json'):
                with open('admin_config.json', 'r') as f:
                    config = json.load(f)
            
            # 更新路径
            config['app_path'] = path
            
            # 保存配置
            with open('admin_config.json', 'w') as f:
                json.dump(config, f)
            
            messagebox.showinfo("成功", "应用程序路径已保存！")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存路径失败: {str(e)}")
    
    def _open_app(self):
        """打开应用程序"""
        try:
            path = self.app_path_entry.get().strip()
            if not path:
                messagebox.showwarning("警告", "请输入应用程序路径！")
                return
            
            if not os.path.exists(path):
                messagebox.showerror("错误", "指定的路径不存在！")
                return
            
            # 使用 AppController 启动应用
            if self.app_controller:
                if self.app_controller.start_app(path):
                    messagebox.showinfo("成功", "应用程序已启动！")
                else:
                    messagebox.showerror("错误", "启动应用程序失败！")
            else:
                # 如果没有 AppController，使用直接方式启动
                import subprocess
                subprocess.Popen(path)
                messagebox.showinfo("成功", "应用程序已启动！")
            
        except Exception as e:
            messagebox.showerror("错误", f"启动应用程序失败: {str(e)}")
    
    def _change_password(self):
        """修改管理员密码"""
        new_password = self.new_password_entry.get().strip()
        if not new_password:
            messagebox.showwarning("警告", "请输入新密码！")
            return
        
        # 计算新密码的哈希值
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        try:
            # 读取现有配置
            config = {}
            if os.path.exists('admin_config.json'):
                with open('admin_config.json', 'r') as f:
                    config = json.load(f)
            
            # 更新密码哈希
            config['password_hash'] = new_password_hash
            
            # 保存配置
            with open('admin_config.json', 'w') as f:
                json.dump(config, f)
            
            # 更新当前密码
            self.admin_password = new_password_hash
            
            messagebox.showinfo("成功", "管理员密码已更新！")
            
        except Exception as e:
            messagebox.showerror("错误", f"更新密码失败: {str(e)}")
    
    def _load_auto_close_time(self):
        """加载当前定时关闭时间"""
        try:
            if os.path.exists('admin_config.json'):
                with open('admin_config.json', 'r') as f:
                    config = json.load(f)
                    auto_close_time = config.get('auto_close_minutes', 0)
                    self.auto_close_entry.insert(0, str(auto_close_time))
        except Exception as e:
            print(f"加载定时关闭时间失败: {e}")

    def _save_auto_close_time(self):
        """保存定时关闭时间"""
        try:
            auto_close_time = int(self.auto_close_entry.get().strip())
            if auto_close_time < 0:
                messagebox.showwarning("警告", "请输入有效的时间！")
                return
            
            # 更新 AppController 的定时关闭时间
            if self.app_controller:
                self.app_controller.auto_close_minutes = auto_close_time
            
            # 读取现有配置
            config = {}
            if os.path.exists('admin_config.json'):
                with open('admin_config.json', 'r') as f:
                    config = json.load(f)
            
            # 更新定时关闭时间
            config['auto_close_minutes'] = auto_close_time
            
            # 保存配置
            with open('admin_config.json', 'w') as f:
                json.dump(config, f)
            
            messagebox.showinfo("成功", "定时关闭时间已保存！")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数！")
        except Exception as e:
            messagebox.showerror("错误", f"保存定时关闭时间失败: {str(e)}")

    def _create_password_change_widgets(self, parent_frame):
        """创建密码修改界面组件"""
        password_frame = ttk.LabelFrame(parent_frame, text="修改管理员密码", padding=10)
        password_frame.pack(fill='x', pady=(10, 20))
        
        ttk.Label(password_frame, text="新密码:", font=('Arial', 12)).pack(side='left', padx=(0, 10))
        self.new_password_entry = ttk.Entry(password_frame, show="*", width=30, font=('Arial', 12))
        self.new_password_entry.pack(side='left', padx=(0, 10))
        
        ttk.Button(
            password_frame,
            text="保存新密码",
            command=self._change_password
        ).pack(side='left', padx=5)
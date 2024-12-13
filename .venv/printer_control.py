import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PrinterControlWindow:
    """打印控制窗口"""
    def __init__(self, user_info, on_close_callback):
        # 创建新窗口
        self.window = tk.Toplevel()
        self.window.title('3D打印机控制面板')
        
        # 禁用窗口右上角的关闭按钮
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # 设置窗口大小和位置
        self.window_width = 1280
        self.window_height = 720
        self._center_window()
        
        # 保存用户信息和回调函数
        self.user_info = user_info
        self.on_close_callback = on_close_callback
        
        # 创建UI组件
        self._create_widgets()
        
    def _center_window(self):
        """将窗口居中显示"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        center_x = int(screen_width/2 - self.window_width/2)
        center_y = int(screen_height/2 - self.window_height/2)
        
        self.window.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
    
    def _create_widgets(self):
        """创建控制面板的UI组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(pady=30, padx=40, fill='both', expand=True)
        
        # 用户信息显示
        self.info_frame = ttk.LabelFrame(self.main_frame, text='当前用户信息', padding=15)
        self.info_frame.pack(fill='x', pady=(0, 20))
        
        info_text = f"""
        使用者：{self.user_info['user_name']}
        项目名称：{self.user_info['project_name']}
        学号：{self.user_info['student_id']}
        """
        
        self.info_label = ttk.Label(
            self.info_frame,
            text=info_text,
            font=('Arial', 12),
            justify='left'
        )
        self.info_label.pack(padx=10, pady=5)
        
        # 打印时间和邮箱输入区域
        self.input_frame = ttk.LabelFrame(self.main_frame, text='打印信息登记', padding=15)
        self.input_frame.pack(fill='x', pady=(0, 20))
        
        # 打印时长输入
        self.time_frame = ttk.Frame(self.input_frame)
        self.time_frame.pack(fill='x', padx=20, pady=10)
        
        self.time_label = ttk.Label(
            self.time_frame, 
            text='预计打印时长(小时):', 
            font=('Arial', 12)
        )
        self.time_label.pack(side='left', padx=(0, 15))
        
        self.time_entry = ttk.Entry(self.time_frame, width=20, font=('Arial', 12))
        self.time_entry.pack(side='left')
        
        # 邮箱输入
        self.email_frame = ttk.Frame(self.input_frame)
        self.email_frame.pack(fill='x', padx=20, pady=10)
        
        self.email_label = ttk.Label(
            self.email_frame, 
            text='邮箱地址:', 
            font=('Arial', 12)
        )
        self.email_label.pack(side='left', padx=(0, 15))
        
        self.email_entry = ttk.Entry(self.email_frame, width=40, font=('Arial', 12))
        self.email_entry.pack(side='left')
        
        # 按钮框架
        self.button_frame = ttk.Frame(self.input_frame)
        self.button_frame.pack(pady=10)
        
        # 提交按钮
        self.submit_btn = ttk.Button(
            self.button_frame,
            text='提交信息',
            command=self._submit_info,
            style='Accent.TButton'
        )
        self.submit_btn.pack(side='left', padx=10)
        
        # 退出按钮
        self.exit_btn = ttk.Button(
            self.button_frame,
            text='退出',
            command=self._on_exit
        )
        self.exit_btn.pack(side='left', padx=10)
        
        # 说明区域
        self.instruction_frame = ttk.LabelFrame(self.main_frame, text='使用说明', padding=15)
        self.instruction_frame.pack(fill='both', expand=True)
        
        instruction_text = """
        说明：
        
        你可以输入你的打印时长和邮箱地址，系统将在打印完成后通过邮件通知你。
        如果你觉得麻烦也可以不输入，直接点退出就行了。
        
        点击退出按钮，会回到登记页面。
        如果你没有关闭Bamboo Studio，系统会在30分钟后自动关闭Bamboo Studio。
        """
        
        self.instruction_label = ttk.Label(
            self.instruction_frame,
            text=instruction_text,
            font=('Arial', 12),
            justify='left',
            wraplength=self.window_width - 150
        )
        self.instruction_label.pack(padx=10, pady=5)
    
    def _submit_info(self):
        """提交打印信息"""
        time = self.time_entry.get()
        email = self.email_entry.get()
        
        # 验证输入
        if not time or not email:
            messagebox.showwarning("提示", "请填写完整的打印时长和邮箱地址！")
            return
        
        # 验证时间格式
        try:
            hours = float(time)
            if hours <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("提示", "请输入有效的打印时长！")
            return
        
        # 验证邮箱格式
        if '@' not in email or '.' not in email:
            messagebox.showwarning("提示", "请输入有效的邮箱地址！")
            return
        
        # TODO: 在这里添加保存信息的逻辑
        
        messagebox.showinfo(
            "成功", 
            f"信息已提交！\n打印时长：{time}小时\n通知邮箱：{email}\n"
            "系统将在打印完成后通过邮件通知您。"
        ) 
    
    def _on_exit(self):
        """退出"""
        self.on_close_callback(self.window)
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from data_manager import DataManager
from printer_control import PrinterControlWindow
from admin_window import AdminWindow

class PrinterAssistantGUI:
    def __init__(self, window_width=1280, window_height=720, app_controller=None, admin_window=None):
        # 初始化主窗口
        self.root = tk.Tk()
        self.root.title('3D打印机使用登记助手')
        
        # 保存窗口尺寸和控制器
        self.window_width = window_width
        self.window_height = window_height
        self.app_controller = app_controller
        self.admin_window = admin_window
        
        # 设置窗口位置和大小
        self._center_window()
        
        # 创建UI组件
        self._create_widgets()
        
        # 初始化数据管理器
        self.data_manager = DataManager()
    
    def _center_window(self):
        """将窗口居中显示"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int(screen_width/2 - self.window_width/2)
        center_y = int(screen_height/2 - self.window_height/2)
        
        self.root.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
    
    def _create_widgets(self):
        """创建所有UI组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=30, padx=40)
        
        # 欢迎文本
        self.welcome_label = ttk.Label(
            self.main_frame, 
            text='欢迎使用3D打印机登记助手!',
            font=('Arial', 24, 'bold')
        )
        self.welcome_label.pack(pady=(0, 30))
        
        # 用户信息框架
        self.info_frame = ttk.LabelFrame(self.main_frame, text='用户信息', padding=15)
        self.info_frame.pack(fill='x', pady=(0, 30))
        
        # 使用者姓名输入
        self.name_frame = ttk.Frame(self.info_frame)
        self.name_frame.pack(fill='x', padx=20, pady=10)
        
        self.name_label = ttk.Label(self.name_frame, text='使用者姓名:', font=('Arial', 12))
        self.name_label.pack(side='left', padx=(0, 15))
        
        self.name_entry = ttk.Entry(self.name_frame, width=40, font=('Arial', 12))
        self.name_entry.pack(side='left')
        
        # 项目名称输入
        self.project_frame = ttk.Frame(self.info_frame)
        self.project_frame.pack(fill='x', padx=20, pady=10)
        
        self.project_label = ttk.Label(self.project_frame, text='项目名称:  ', font=('Arial', 12))
        self.project_label.pack(side='left', padx=(0, 15))
        
        self.project_entry = ttk.Entry(self.project_frame, width=40, font=('Arial', 12))
        self.project_entry.pack(side='left')
        
        # 将邮箱输入框改为学号输入框
        self.student_id_frame = ttk.Frame(self.info_frame)
        self.student_id_frame.pack(fill='x', padx=20, pady=10)
        
        self.student_id_label = ttk.Label(self.student_id_frame, text='学号:      ', font=('Arial', 12))
        self.student_id_label.pack(side='left', padx=(0, 15))
        
        self.student_id_entry = ttk.Entry(self.student_id_frame, width=40, font=('Arial', 12))
        self.student_id_entry.pack(side='left')
        
        # 操作按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=20)
        
        # 启动按钮
        self.start_button = ttk.Button(
            self.button_frame,
            text='启动软件',
            command=self.on_start,
            style='Accent.TButton'
        )
        self.start_button.pack(side='left', padx=10)
        
        
        # 添加管理员按钮
        self.admin_button = ttk.Button(
            self.button_frame,
            text='管理员',
            command=self._open_admin_window
        )
        self.admin_button.pack(side='left', padx=10)
        
        # 退出按钮
        self.exit_button = ttk.Button(
            self.button_frame, 
            text='退出',
            command=self.on_exit
        )
        self.exit_button.pack(side='left', padx=10)
        
        # 添加说明区域
        self.instruction_frame = ttk.LabelFrame(self.main_frame, text='使用说明', padding=15)
        self.instruction_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        instruction_text = """
        3D打印机使用步骤说明：
        
        1. 填写使用者姓名和项目名称
        2. 输入你的学号
        3. 输入完成后点击“启动软件”即可打开切片软件开始打印
        """
        
        self.instruction_label = ttk.Label(
            self.instruction_frame,
            text=instruction_text,
            font=('Arial', 12),
            justify='left',
            wraplength=self.window_width - 150  # 自动换行宽度
        )
        self.instruction_label.pack(padx=20, pady=10)
        
        # 创建自定义样式
        self._create_styles()
    
    def _create_styles(self):
        """创建自定义按钮样式"""
        style = ttk.Style()
        # 创建突出显示的按钮样式
        style.configure('Accent.TButton', font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TLabelframe.Label', font=('Arial', 12, 'bold'))
    
    def on_start(self):
        """启动按钮的回调函数"""
        user_name = self.name_entry.get()
        project_name = self.project_entry.get()
        student_id = self.student_id_entry.get()
        
        # 验证输入
        if not user_name or not project_name or not student_id:
            messagebox.showwarning(
                "提示", 
                "请填写完整的使用者姓名、项目名称和学号！"
            )
            return
        
        # 学号格式验证（假设学号为8位数字）
        if not student_id.isdigit() or len(student_id) != 8:
            messagebox.showwarning(
                "提示", 
                "请输入正确的8位学号！"
            )
            return
        
        # 保存打印作业记录并打开控制面板
        if self._save_print_job(user_name, project_name, student_id):
            print(f"启动软件 - 使用者：{user_name}，项目：{project_name}，学号：{student_id}")
    
    def on_exit(self):
        """退出程序"""
        self.root.quit()
    
    def run(self):
        """启动主循环"""
        self.root.mainloop()
    
    def _save_print_job(self, user_name, project_name, student_id):
        """保存打印作业记录并打开控制面板"""
        try:
            # 保存打印记录
            if not self.data_manager.save_print_record(user_name, project_name, student_id):
                raise Exception("数据保存失败")
            
            # 启动外部应用（如果有配置应用控制器）
            if self.app_controller:
                if not self.app_controller.start_app():
                    messagebox.showwarning(
                        "警告",
                        "无法启动切片软件，请检查软件是否正确安装。"
                    )
                    return False  # 软件启动失败时直接返回
                
                # 显示应用启动成功的提示信息
                messagebox.showinfo(
                    "成功",
                    "切片软件已成功启动！"
                )
            
            # 记录成功后清空输入框
            self.name_entry.delete(0, tk.END)
            self.project_entry.delete(0, tk.END)
            self.student_id_entry.delete(0, tk.END)
            
            # 显示成功消息
            messagebox.showinfo(
                "成功", 
                f"登记信息已提交！\n用户：{user_name}\n项目：{project_name}\n学号：{student_id}"
            )
            
            # 注释掉打开控制面板窗口的功能
            # user_info = {
            #     'user_name': user_name,
            #     'project_name': project_name,
            #     'student_id': student_id
            # }
            # control_window = PrinterControlWindow(
            #     user_info,
            #     self._on_control_window_close  # 传递回调函数
            # )
            
            # 不再隐藏主窗口
            # self.root.withdraw()
            
            return True
            
        except Exception as e:
            messagebox.showerror(
                "错误", 
                f"保存记录失败：{str(e)}\n请重试！"
            )
            return False
    
    def _on_control_window_close(self, control_window):
        """处理控制窗口关闭事件"""
        if messagebox.askyesno("确认", "确定要关闭控制面板吗？"):
            control_window.destroy()
            self.root.deiconify()  # 重新显示主窗口
    
    def _open_admin_window(self):
        """打开管理员窗口"""
        if self.admin_window:
            self.admin_window.show_login()
  
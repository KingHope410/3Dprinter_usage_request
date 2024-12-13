from gui import PrinterAssistantGUI
from app_controller import AppController
from admin_window import AdminWindow

# 全局常量定义
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def main():
    # 创建应用控制器
    app_controller = AppController(
        app_name="bambu-studio.exe",
        app_path="D:/Bambu Studio/bambu-studio.exe"
    )
    
    # 创建管理员窗口实例，并传入应用控制器
    admin_window = AdminWindow(app_controller)
    
    # 创建GUI实例，并传入应用控制器和管理员窗口
    app = PrinterAssistantGUI(
        window_width=WINDOW_WIDTH,
        window_height=WINDOW_HEIGHT,
        app_controller=app_controller,
        admin_window=admin_window
    )
    
    # 运行程序
    app.run()

if __name__ == '__main__':
    main()
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=PrinterAssistant',  # 可执行文件的名称
    '--onefile',                # 打包成单个文件
    '--windowed',               # 不显示控制台窗口
    '--add-data=.venv/data/print_records.csv;.venv/data',  # 添加数据文件
    '--add-data=admin_config.json;.',  # 添加配置文件
    '--add-data=.venv/logs;logs',  # 添加日志目录
    '--add-data=.venv/data_manager.py;.',  # 添加数据管理器
    '--add-data=.venv/printer_control.py;.',  # 添加打印控制
    '--add-data=.venv/admin_window.py;.',  # 添加管理员窗口
    '--add-data=.venv/gui.py;.',  # 添加GUI
    '--add-data=.venv/app_controller.py;.',  # 添加应用控制器
    '--hidden-import=tkinter',  # 确保tkinter被正确导入
    '.venv/main.py'  # 主程序入口
]) 
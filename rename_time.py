import os
import time
from datetime import datetime

def is_already_renamed(filename):
    # 检查文件名是否已经包含日期前缀（8位数字+空格+减号）
    parts = filename.split(' - ', 1)
    if len(parts) == 2:
        date_part = parts[0]
        if len(date_part) == 8 and date_part.isdigit():
            return True
    return False

def should_skip_folder(folder_name):
    # 检查是否是需要跳过的文件夹
    skip_folders = ['备份', 'back']
    return folder_name in skip_folders

def rename_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for root, dirs, files in os.walk(current_dir):
        
        # 跳过不需要的部分
        folder_name = os.path.basename(root)
        if should_skip_folder(folder_name):
            continue
            
        for filename in files:
            if filename.endswith('.py'):
                continue
                
            file_path = os.path.join(root, filename)
            
            if is_already_renamed(filename):
                continue
            
            try:
                mtime = os.path.getmtime(file_path)
                dt = datetime.fromtimestamp(mtime)
                date_str = dt.strftime('%Y%m%d')
                
                # 构造新文件名
                new_filename = f"{date_str} - {filename}"
                new_file_path = os.path.join(root, new_filename)
                
                # 重命名文件
                os.rename(file_path, new_file_path)
                print(f"已重命名: {filename} -> {new_filename}")
                
            except Exception as e:
                print(f"重命名文件 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    try:
        rename_files()
        print("文件重命名完成！")
        input("按回车键退出...")
    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        input("按回车键退出...")
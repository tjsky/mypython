import os
import time
from datetime import datetime

def is_already_renamed(filename):
    # 检查文件名是否已经包含日期前缀（8位数字_）
    parts = filename.split('_', 1)
    if len(parts) == 2:
        date_part = parts[0]
        if len(date_part) == 8 and date_part.isdigit():
            return True
    return False

def should_skip_folder(folder_name):
    # 跳过部分文件夹
    skip_folders = ['备份', 'BACK']
    return folder_name in skip_folders

def preview_changes():
    # 预览更改
    current_dir = os.path.dirname(os.path.abspath(__file__))
    changes_found = False
    
    print("\n文件将被重命名：")
    print("-" * 50)
    
    for root, dirs, files in os.walk(current_dir):
        folder_name = os.path.basename(root)
        if should_skip_folder(folder_name):
            continue
            
        for filename in files:
            if filename.endswith('.py'):
                continue
                
            if is_already_renamed(filename):
                continue
            
            file_path = os.path.join(root, filename)
            mtime = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(mtime)
            date_str = dt.strftime('%Y%m%d')
            new_filename = f"{date_str}_{filename}"
            
            print(f"{filename} -> {new_filename}")
            changes_found = True
    
    print("-" * 50)
    if not changes_found:
        print("我没有找到需要重命名的文件。")
    return changes_found

def rename_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 遍历目录及子目录
    for root, dirs, files in os.walk(current_dir):
        
        folder_name = os.path.basename(root)
        if should_skip_folder(folder_name):
            continue
            
        for filename in files:
            # 跳过自身
            if filename.endswith('.py'):
                continue
                

            file_path = os.path.join(root, filename)
            
            # 跳过已经改过的
            if is_already_renamed(filename):
                continue
            
            try:
                mtime = os.path.getmtime(file_path)
                dt = datetime.fromtimestamp(mtime)
                date_str = dt.strftime('%Y%m%d')
                
                # 构建新文件名
                new_filename = f"{date_str}_{filename}"
                new_file_path = os.path.join(root, new_filename)
                
                # 重命名文件
                os.rename(file_path, new_file_path)
                print(f"已重命名: {filename} -> {new_filename}")
                
            except Exception as e:
                print(f"重命名文件 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    try:
        print("文件批量重命名工具")
        print("=" * 50)
        print("此工具将在文件名前添加修改日期前缀")
        print("格式: YYYYMMDD_原文件名")
        print("=" * 50)
        
        # 预览更改
        changes_exist = preview_changes()
        
        if changes_exist:
            while True:
                choice = input("\n是否执行重命名操作？(Y/N): ").strip().upper()
                if choice == 'Y':
                    print("\n开始重命名文件...")
                    rename_files()
                    print("\n文件重命名完成！")
                    break
                elif choice == 'N':
                    print("\n操作已取消。")
                    break
                else:
                    print("你输的是啥啊，请输入 Y 或 N")
        
        input("\n按回车键退出...")
        
    except Exception as e:
        print(f"\n程序执行出错: {str(e)}")
        input("\n按回车键退出...")

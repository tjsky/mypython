import os
import re
import shutil
from pathlib import Path

def organize_folders_by_date(src_dir):
    # 匹配年份和月份
    pattern = re.compile(r"(\d{4})年(\d{1,2})月\d{1,2}日")  
    
    for folder_name in os.listdir(src_dir):
        folder_path = os.path.join(src_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
        
        # 提取年月
        match = pattern.search(folder_name)
        if not match:
            print(f"跳过不含有效日期的文件夹: {folder_name}")
            continue
        
        year, month = match.groups()
        # 格式化月份
        formatted_month = f"{int(month):02d}月"
        
        
        target_dir = Path(src_dir) / f"{year}年" / formatted_month
        
        target_path = target_dir / folder_name
        
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(folder_path, target_path)
            print(f"移动成功: {folder_name} -> {target_path}")
        except Exception as e:
            print(f"移动失败: {folder_name} | 错误: {str(e)}")

# 需要处理的目录
organize_folders_by_date(r"D:\Downloads\")
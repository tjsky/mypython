import os
import sys
import platform
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from datetime import datetime
import jinja2

# 报告的 HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>图片完整性检测</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        .summary { background: #f8f9fa; padding: 20px; border-radius: 5px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        tr:hover { background-color: #f5f5f5; }
        .critical { color: #dc3545; font-weight: bold; }
    </style>
</head>
<body>
    <h1>图片完整性检测</h1>
    <div class="summary">
        <p>扫描时间：{{ scan_time }}</p>
        <p>扫描目录：{{ scan_dir }}</p>
        <p class="critical">损坏文件：{{ corrupted_count }} / {{ total_files }}</p>
        <p>完成耗时：{{ duration }} 秒</p>
    </div>

    <h2>损坏文件详情</h2>
    <table>
        <thead>
            <tr>
                <th>文件路径</th>
                <th>错误信息</th>
            </tr>
        </thead>
        <tbody>
            {% for file in corrupted_files %}
            <tr>
                <td>{{ file.path }}</td>
                <td>{{ file.error }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

# 适配unix与win全平台
def is_hidden_file(path):
    try:
        
        if not os.path.exists(path):
            return False
            
        name = os.path.basename(path)
                
        if name.startswith('.'):
            return True
        
        if platform.system() == 'Windows':
            attrs = os.stat(path).st_file_attributes
            return bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
        return False
    except Exception as e:
        print(f"隐藏检测异常 {path}: {str(e)}")
        return False

# 图片完整性检查
def validate_image_file(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        
        with Image.open(file_path) as img:
            img.load()
        
        return (file_path, None)
    except Exception as e:
        return (file_path, str(e))

# 生成HTML检测报告
def generate_report(output_path, data):
    env = jinja2.Environment()
    template = env.from_string(HTML_TEMPLATE)
    html = template.render(**data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

# 扫描所有图片
def scan_images(directory, max_workers=None):
    
    supported_ext = {'.jpg', '.jpeg', '.png', '.gif', 
                    '.bmp', '.webp', '.tiff', '.heic'}
    
    image_files = []
    for root, dirs, files in os.walk(directory):
        
        dirs[:] = [d for d in dirs if not is_hidden_file(os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            if is_hidden_file(file_path):
                continue
            
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_ext:
                image_files.append(file_path)
    
    # 并行扫描
    corrupted = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(validate_image_file, path): path 
                  for path in image_files}
        
        # 进度条显示
        with tqdm(total=len(image_files), desc="扫描进度", unit="file") as pbar:
            for future in as_completed(futures):
                path, error = future.result()
                if error:
                    corrupted.append({"path": path, "error": error})
                pbar.update(1)
    
    return corrupted, len(image_files)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python img_validator.py <目录路径> [并发数(留空使用CPU全部线程)]")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    max_workers = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count()
    
    start_time = datetime.now()
    corrupted_files, total_files = scan_images(target_dir, max_workers)
    duration = round((datetime.now() - start_time).total_seconds(), 2)
    
    # 生成HTML报告
    report_data = {
        "scan_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "scan_dir": os.path.abspath(target_dir),
        "corrupted_count": len(corrupted_files),
        "total_files": total_files,
        "duration": duration,
        "corrupted_files": corrupted_files
    }
    
    report_path = os.path.join(os.getcwd(), "image_validation_report.html")
    generate_report(report_path, report_data)
    
    # 控制台输出
    print(f"\n扫描完成！耗时 {duration} 秒")
    print(f"检测文件总数: {total_files}")
    print(f"损坏文件数量: {len(corrupted_files)}")
    print(f"报告已生成: file://{report_path}")
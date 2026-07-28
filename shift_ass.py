import os
import re

# 格式需要减去的时间：1小时2分钟3秒 
SHIFT_CS = (1 * 3600 + 2 * 60 + 3) * 100

def shift_timestamp(match):
    h, m, s, cs = map(int, match.groups())
    total_cs = (h * 3600 + m * 60 + s) * 100 + cs
    
    new_cs = total_cs - SHIFT_CS
    if new_cs < 0:
        new_cs = 0
    
    new_h = new_cs // 360000
    new_cs %= 360000
    new_m = new_cs // 6000
    new_cs %= 6000
    new_s = new_cs // 100
    new_cs %= 100
    
    return f"{new_h}:{new_m:02d}:{new_s:02d}.{new_cs:02d}"

def process_ass_files():
    time_pattern = re.compile(r'(\d+):(\d{2}):(\d{2})\.(\d{2})')
    
    files = [f for f in os.listdir('.') if f.endswith('.ass') and not f.endswith('_fixed.ass')]
    if not files:
        print("当前目录下未找到 .ass 文件")
        return

    for filename in files:
        with open(filename, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read()
        
        # 替换时间戳并另存为新文件
        new_content = time_pattern.sub(shift_timestamp, content)
        
        output_filename = filename.replace('.ass', '_fixed.ass')
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"处理完毕: {filename} -> {output_filename}")

if __name__ == '__main__':
    process_ass_files()

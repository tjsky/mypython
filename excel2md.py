# pip install pandas
# pip install tabulate
# pip install openpyxl

import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('表格文件名.xlsx')

# 将 DataFrame 转换为 Markdown 格式
markdown_table = df.to_markdown(index=False)

# 输出 Markdown 表格
print(markdown_table)

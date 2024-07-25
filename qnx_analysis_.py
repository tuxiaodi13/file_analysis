import pandas as pd
from pathlib import Path
import re

def parse_files(directory):
    # 创建一个空 DataFrame 来存储结果
    data = pd.DataFrame(columns=['A', 'B'])

    # 获取当前目录下的所有文件
    files = list(Path(directory).glob('*'))

    for file_path in files:
        if file_path.is_file() and not file_path.name.startswith('.'):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # 初始化变量
                time_A = None
                time_B = None
                
                for line in lines:
                    if '(0x7362)times:1' in line:
                        # 提取时间
                        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', line)
                        if match:
                            time_A = match.group(0)
                    
                    elif time_A is not None and re.search(r'\(0x7510\)times:\d+(?![0])', line):
                        # 提取时间
                        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', line)
                        if match:
                            time_B = match.group(0)
                            break  # 找到 B 时间后跳出循环
                        
                if time_A and time_B:
                    # 将找到的时间添加到 DataFrame
                    data = pd.concat([data, pd.DataFrame({'A': [time_A], 'B': [time_B]})], ignore_index=True)

    return data

def main():
    # 指定要解析的目录
    directory = 'qnx0725'
    
    # 解析文件并获取数据
    parsed_data = parse_files(directory)
    
    # 保存到 Excel 文件
    parsed_data.to_excel('result.xlsx', index=False)
    print("Data has been saved to 'result.xlsx'")

if __name__ == '__main__':
    main()
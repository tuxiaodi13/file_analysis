import pandas as pd
from pathlib import Path
import re

def parse_files(directory):
    # ����һ���� DataFrame ���洢���
    data = pd.DataFrame(columns=['A', 'B'])

    # ��ȡ��ǰĿ¼�µ������ļ�
    files = list(Path(directory).glob('*'))

    for file_path in files:
        if file_path.is_file() and not file_path.name.startswith('.'):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # ��ʼ������
                time_A = None
                time_B = None
                
                for line in lines:
                    if '(0x7362)times:1' in line:
                        # ��ȡʱ��
                        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', line)
                        if match:
                            time_A = match.group(0)
                    
                    elif time_A is not None and re.search(r'\(0x7510\)times:\d+(?![0])', line):
                        # ��ȡʱ��
                        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', line)
                        if match:
                            time_B = match.group(0)
                            break  # �ҵ� B ʱ�������ѭ��
                        
                if time_A and time_B:
                    # ���ҵ���ʱ����ӵ� DataFrame
                    data = pd.concat([data, pd.DataFrame({'A': [time_A], 'B': [time_B]})], ignore_index=True)

    return data

def main():
    # ָ��Ҫ������Ŀ¼
    directory = 'qnx0725'
    
    # �����ļ�����ȡ����
    parsed_data = parse_files(directory)
    
    # ���浽 Excel �ļ�
    parsed_data.to_excel('result.xlsx', index=False)
    print("Data has been saved to 'result.xlsx'")

if __name__ == '__main__':
    main()
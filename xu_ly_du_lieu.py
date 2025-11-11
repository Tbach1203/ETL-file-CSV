import pandas as pd
import numpy as np
import re

df = pd.read_csv('data.csv')

def process_salary(salary):
    if pd.isna(salary):
        return salary
    # Chuyển đổi sang chuỗi nếu chưa phải
    salary_str = str(salary)
    # Kiểm tra và xử lý các trường hợp có chứa "triệu"
    if 'triệu' in salary_str.lower():
        # Tách các phần số và xử lý
        parts = re.split(r' - | tới | trên ', salary_str.lower())
        converted_parts = []
        for part in parts:
            part = part.strip()
            # Tìm tất cả các số trong phần
            numbers = re.findall(r'\d+\.?\d*', part)
            if numbers:
                # Lấy số đầu tiên tìm thấy và nhân với 1,000,000
                number = float(numbers[0])
                converted_number = int(number * 1000000)
                converted_parts.append(str(converted_number))
            else:
                converted_parts.append(part.replace('triệu', '').strip())
        
        # Ghép các phần lại
        if ' - ' in salary_str:
            return ' - '.join(converted_parts)
        elif ' tới ' in salary_str.lower():
            return ' tới '.join(converted_parts)
        elif ' trên ' in salary_str.lower():
            return ' trên '.join(converted_parts)
        else:
            return converted_parts[0] if converted_parts else salary_str
    
    # Giữ nguyên các trường hợp không có "triệu"
    return salary_str

# df['salary'] = df['salary'].apply(process_salary)

def add_column():
    pass 

def process_address():
    pass    

def normalize_job_tile():
    pass 


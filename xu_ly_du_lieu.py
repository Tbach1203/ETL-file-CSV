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
            # Tìm các giá trị số 
            numbers = re.findall(r'\d+\.?\d*', part)
            if numbers:
                number = float(numbers[0])
                converted_number = int(number * 1000000)
                converted_parts.append(str(converted_number))
            else:
                converted_parts.append(part.replace('triệu', '').strip())
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

def add_columns(salary):
    if pd.isna(salary) or str(salary).lower() in ['thoả thuận', 'thỏa thuận']:
        return None, None, None
    salary_str = str(salary)
    # Xác định đơn vị lương
    salary_unit = 'USD' if 'usd' in salary_str.lower() else 'VND'
    # Chuẩn hóa chuỗi lương
    salary_clean = salary_str.lower().replace(',', '').replace(' ', '')
    # Trích xuất các số từ chuỗi
    numbers = re.findall(r'\d+\.?\d*', salary_clean)
    numbers = [float(num) for num in numbers]
    # Xác định min_salary và max_salary dựa trên từ khóa
    if 'tới' in salary_str.lower():
        # Trường hợp "Tới X"
        if numbers:
            return None, numbers[0], salary_unit
        else:
            return None, None, salary_unit
    elif 'trên' in salary_str.lower():
        # Trường hợp "Trên X"
        if numbers:
            return numbers[0], None, salary_unit
        else:
            return None, None, salary_unit
    elif ' - ' in salary_str:
        # Trường hợp "X - Y"
        if len(numbers) >= 2:
            return numbers[0], numbers[1], salary_unit
        elif len(numbers) == 1:
            return numbers[0], numbers[0], salary_unit
        else:
            return None, None, salary_unit
    else:
        # Trường hợp chỉ có một giá trị
        if numbers:
            return numbers[0], numbers[0], salary_unit
        else:
            return None, None, salary_unit

def process_address():
    pass    

def normalize_job_tile():
    pass 

if "__main__" == __name__:
    df['salary'] = df['salary'].apply(process_salary)

    # Trích xuất thông tin lương và tạo các cột mới
    salary_info = df['salary'].apply(add_columns)
    df['min_salary'] = salary_info.apply(lambda x: x[0] if x else None)
    df['max_salary'] = salary_info.apply(lambda x: x[1] if x else None)
    df['salary_unit'] = salary_info.apply(lambda x: x[2] if x else None)
    df['salary'] = df['salary'].apply(lambda x: re.sub(r'\s*USD\s*', '', str(x), flags=re.IGNORECASE) if pd.notna(x) else x)

    cols = df.columns.tolist()
    salary_index = cols.index('salary')

    # Tìm vị trí để chèn các cột mới 
    new_cols = cols[:salary_index+1] + ['salary_unit', 'min_salary', 'max_salary'] + cols[salary_index+1:-3]
    df = df[new_cols]

    df = df.fillna('unknown')
    df.to_csv('data_normalize.csv', index=False)
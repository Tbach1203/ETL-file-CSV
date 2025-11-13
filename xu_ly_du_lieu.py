import pandas as pd
import numpy as np
import re

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

def process_address(address):
    if pd.isna(address):
        return []
    address_str = str(address)
    # Tách các phần bằng dấu ":"
    parts = [part.strip() for part in address_str.split(':')]
    # Tạo danh sách các cặp (city, district)
    pairs = []
    # Nếu chỉ có 1 phần tử
    if len(parts) == 1:
        pairs.append((parts[0], None))
    else:
        # Ghép các phần tử thành các cặp (city, district)
        for i in range(0, len(parts), 2):
            if i + 1 < len(parts):
                pairs.append((parts[i], parts[i+1]))
            else:
                pairs.append((parts[i], None))
    return pairs

def normalize_job_tile(job_title):
    if pd.isna(job_title):
        return "Other"
    
    job_title_lower = job_title.lower()
    
    # Định nghĩa các nhóm và từ khóa tương ứng
    job_groups = {
        "Software Engineer": [
            "software engineer", "software developer", "developer", "programmer", 
            "lập trình viên", "lap trinh vien", "dev", "engineer"
        ],
        "Business Analyst": [
            "business analyst", "ba", "phân tích nghiệp vụ", "phan tich nghiep vu"
        ],
        "Data Scientist/Analyst": [
            "data scientist", "data analyst", "data engineer", "big data", 
            "machine learning", "ai engineer", "artificial intelligence"
        ],
        "Project Manager": [
            "project manager", "pm", "quản lý dự án", "quan ly du an", 
            "scrum master", "product owner"
        ],
        "QA/Tester": [
            "tester", "qa", "quality assurance", "kiểm thử", "kiem thu", 
            "quality control", "qc"
        ],
        "DevOps/System Admin": [
            "devops", "system admin", "sysadmin", "system administrator", 
            "it admin", "network", "infrastructure"
        ],
        "Frontend Developer": [
            "frontend", "front end", "react", "angular", "vue", "javascript"
        ],
        "Backend Developer": [
            "backend", "back end", "java", "python", "node", "php", ".net"
        ],
        "Full Stack Developer": [
            "full stack", "fullstack", "full-stack"
        ],
        "Mobile Developer": [
            "mobile", "ios", "android", "react native", "flutter"
        ],
        "UI/UX Designer": [
            "ui/ux", "ux/ui", "designer", "thiết kế", "thiet ke"
        ],
        "IT Support": [
            "it support", "helpdesk", "hỗ trợ kỹ thuật", "ho tro ky thuat",
            "technical support"
        ],
        "Database Administrator": [
            "database", "dba", "sql", "quản trị cơ sở dữ liệu", "quan tri co so du lieu"
        ],
        "Security": [
            "security", "cyber", "an ninh mạng", "an toan thong tin", "bảo mật", "bao mat"
        ]
    }
    # Kiểm tra từng nhóm
    for group, keywords in job_groups.items():
        for keyword in keywords:
            if keyword in job_title_lower:
                return group
    return "Other"

if  __name__ == "__main__":
    df = pd.read_csv('data.csv')
    df['job_group'] = df['job_title'].apply(normalize_job_tile)
    df['salary'] = df['salary'].apply(process_salary)

    # Trích xuất thông tin lương và tạo các cột mới
    salary_info = df['salary'].apply(add_columns)
    df['min_salary'] = salary_info.apply(lambda x: x[0] if x else None)
    df['max_salary'] = salary_info.apply(lambda x: x[1] if x else None)
    df['salary_unit'] = salary_info.apply(lambda x: x[2] if x else None)
    df['salary'] = df['salary'].apply(lambda x: re.sub(r'\s*USD\s*', '', str(x), flags=re.IGNORECASE) if pd.notna(x) else x)

    new_rows = []
    # Duyệt qua từng dòng trong DataFrame gốc
    for idx, row in df.iterrows():
        address_pairs = process_address(row['address'])
        
        # Nếu không có cặp nào, thêm dòng gốc với city và district là None
        if not address_pairs:
            new_row = row.copy()
            new_row['city'] = None
            new_row['district'] = None
            new_rows.append(new_row)
        else:
            # Thêm một dòng mới cho mỗi cặp (city, district)
            for city, district in address_pairs:
                new_row = row.copy()
                new_row['city'] = city
                new_row['district'] = district
                new_rows.append(new_row)

    # Tạo DataFrame mới từ danh sách các dòng
    new_df = pd.DataFrame(new_rows)
    # Định nghĩa thứ tự các cột mong muốn
    desired_order = [
        'created_date', 'job_title', 'job_group', 'company', 'salary', 
        'min_salary', 'max_salary', 'salary_unit', 'address', 'city', 
        'district', 'time', 'link_description'
    ]

    # Chỉ giữ lại các cột có trong DataFrame
    final_columns = [col for col in desired_order if col in new_df.columns]
    new_df = new_df[final_columns]
    # new_df = new_df.fillna('unknown')
    # Lưu file CSV mới
    new_df.to_csv('data_processed_final.csv', index=False)
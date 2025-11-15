import pandas as pd
import psycopg2
from io import StringIO
import csv
import os

def load_data(df):
    db_params = {
        "database": os.getenv('POSTGRES_DB', 'Mini Project ETL'),
        "user": os.getenv('POSTGRES_USER', 'postgres'),
        "password": os.getenv('POSTGRES_PASSWORD', '123'),
        "host": os.getenv('POSTGRES_HOST', 'host.docker.internal'),
        "port": os.getenv('POSTGRES_PORT', '5432')
    }
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    table_name = 'job'
    cur.execute(f"DROP TABLE IF EXISTS {table_name};")
    conn.commit()

    create_table_query = """
    CREATE TABLE job (
        id SERIAL PRIMARY KEY,
        created_date TEXT,
        job_title TEXT,
        job_group TEXT,
        company TEXT,
        salary TEXT,
        min_salary TEXT,
        max_salary TEXT,
        salary_unit TEXT,
        address TEXT,
        city TEXT,
        district TEXT,
        time TEXT,
        link_description TEXT
    );
    """

    try:
        # Thực thi lệnh tạo bảng
        cur.execute(create_table_query)
        conn.commit()
        print("Bảng đã được tạo thành công!")
    except Exception as e:
        print(f"Lỗi khi tạo bảng: {e}")
        conn.rollback()

    # Thay thế giá trị rỗng hoặc NaN bằng chuỗi "NULL"
    df = df.fillna('NULL')
    for col in df.columns:
        df[col] = df[col].astype(str).replace('nan', 'NULL')
    # Định nghĩa các cột để import (không bao gồm cột id vì nó tự động tăng)
    columns = ['created_date', 'job_title', 'job_group','company','salary','min_salary','max_salary','salary_unit','address','city','district','time','link_description']
    # Tạo buffer và ghi DataFrame dưới dạng CSV với tất cả các trường được đặt trong dấu ngoặc kép
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, header=False, quoting=csv.QUOTE_ALL, sep=',', quotechar='"')
    csv_buffer.seek(0) 
    try:
        copy_sql = f"""
        COPY {table_name} ({', '.join(columns)}) 
        FROM STDIN 
        WITH (
            FORMAT CSV,
            DELIMITER ',',
            QUOTE '"',
            NULL 'NULL'
        )
        """
        cur.copy_expert(copy_sql, csv_buffer)
        conn.commit()
        print("Dữ liệu đã được tải thành công vào PostgreSQL!")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi tải dữ liệu: {e}")
        conn.rollback()

    cur.close()
    conn.close()
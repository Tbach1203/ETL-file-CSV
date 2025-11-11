import pandas as pd
import numpy as np
import re

df = pd.read_csv('data.csv')
print(df['salary'])

def process_salary(salary):
    if pd.isna(salary) or salary == ' ':
        return salary
    salary = str(salary).lower()

    if 'triệu' in salary:
        numbers = re.findall(r'\d+\.?\d*', salary)
        
        if numbers:
            first_number = float(numbers[0])
            return int(first_number * 1000000)
    return salary

# df['salary'] = df['salary'].apply(process_salary)
# print(df['salary'])

def add_column():
    pass 

def process_address():
    pass    

def normalize_job_tile():
    pass 


import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')
print(df['salary'])

def process_salary(salary):
    if salary == 'Thỏa thuận':
        return np.nan


def add_column():
    pass 

def process_address():
    pass    

def normalize_job_tile():
    pass 


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import csv
import sys
import os



sys.path.append(os.path.join(os.path.dirname(__file__), '../plugins'))
from xu_ly_du_lieu import transform
from load_du_lieu import load_data

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'job_etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline for Job Data from CSV to PostgreSQL',
    schedule=timedelta(days=1),
    tags=['etl', 'job', 'postgresql']
)

def extract_data(**kwargs):
    ti = kwargs['ti']
    csv_file_path = '/opt/airflow/data.csv'
    
    try:
        df = pd.read_csv(csv_file_path)
        ti.xcom_push(key='raw_data', value=df.to_json(orient='records'))
        return f"Extracted {len(df)} records"
    except Exception as e:
        print(f"Error in extract_data: {e}")
        raise

def transform_data(**kwargs):
    ti = kwargs['ti']
    # Pull data from previous task
    raw_data_json = ti.xcom_pull(task_ids='extract_task', key='raw_data')
    raw_df = pd.read_json(raw_data_json, orient='records')
    # Call the transformation function
    transformed_df = transform(raw_df)
    print(f"Transformation completed. {len(transformed_df)} records after transformation")
    # Push transformed data to XCom
    ti.xcom_push(key='transformed_data', value=transformed_df.to_json(orient='records'))
    return f"Transformed {len(transformed_df)} records"

def load_data_wrapper(**kwargs):
    """
    Wrapper function để tương thích với hàm load_data hiện có
    """
    ti = kwargs['ti']
    
    # Lấy dữ liệu từ task transform
    transformed_data_json = ti.xcom_pull(task_ids='transform_task', key='transformed_data')
    df = pd.read_json(transformed_data_json, orient='records')
    return load_data(df)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data_wrapper,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract():
    return "Data extracted"

def transform(data):
    return data + " transformed"

def load(data):
    print(data + " loaded")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'simple_etl_dag',
    default_args=default_args,
    description='A simple ETL DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 1),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    t2 = PythonOperator(
        task_id='transform',
        python_callable=transform,
        op_args=["{{ task_instance.xcom_pull(task_ids='extract') }}"],
    )

    t3 = PythonOperator(
        task_id='load',
        python_callable=load,
        op_args=["{{ task_instance.xcom_pull(task_ids='transform') }}"],
    )

    t1 >> t2 >> t3  # Define task dependencies

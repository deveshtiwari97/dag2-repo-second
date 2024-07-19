# dags/test_basic_dag.py
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    'test_basic_dag',
    default_args=default_args,
    description='A basic test DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    start >> end

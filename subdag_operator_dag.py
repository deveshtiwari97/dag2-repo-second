from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator

def subdag(parent_dag_name, child_dag_name, args):
    dag_subdag = DAG(
        dag_id=f'{parent_dag_name}.{child_dag_name}',
        default_args=args,
        schedule_interval=timedelta(days=1),
    )

    start = DummyOperator(
        task_id='start',
        dag=dag_subdag,
    )

    end = DummyOperator(
        task_id='end',
        dag=dag_subdag,
    )

    start >> end
    return dag_subdag

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'subdag_operator_dag',
    default_args=default_args,
    description='A DAG with SubDAG',
    schedule_interval=timedelta(days=1),
)

start = DummyOperator(
    task_id='start',
    dag=dag,
)

subdag_task = SubDagOperator(
    task_id='subdag_task',
    subdag=subdag('subdag_operator_dag', 'subdag_task', default_args),
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    dag=dag,
)

start >> subdag_task >> end

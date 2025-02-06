from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

import pandas as pd
import sqlalchemy as db
from utiles.functions import *

import random
from sklearn.datasets import load_iris

def insert_data():
    data = load_iris()
    df = pd.DataFrame(data.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
    df['y'] = data.target

    data = DataBaseV2(db_name='airflow', db_type='sqlite')
    
    data.create_table('iris_data', 
                    id_columns=db.Integer, 
                    sepal_length=db.Float, 
                    sepal_width=db.Float,
                    petal_length=db.Float,
                    petal_width=db.Float, 
                    y=db.Integer)

    # Injection dans la base de données
    n_lines = random.randint(0, len(df)-10)

    for n in range(n_lines, n_lines+10):
        data_value = df.iloc[n]
        data.insert_row('iris_data',
                        id_columns=n,
                        sepal_length = data_value.sepal_length,
                        sepal_width = data_value.sepal_width,
                        petal_length = data_value.petal_length,
                        petal_width = data_value.petal_width, 
                        y = data_value.y)
        

def read_data():
    data = DataBaseV2(db_name='airflow', db_type='sqlite')
    n_lines = len(data.dataframe('iris_data'))

    if n_lines >10:
        return 'task_train_model'


with DAG(
    "my_training_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval=timedelta(seconds=30)):

    task_insert_data = PythonOperator(
        task_id="task_insert_data",
        python_callable=insert_data,
    )

    task_read_data = BranchPythonOperator(
        task_id="task_read_data",
        python_callable=read_data)
    
    task_train_model = BashOperator(
        task_id="task_train_model",
        bash_command="python /root/airflow/train.py",)
    
    task_insert_data >> task_read_data >> task_train_model
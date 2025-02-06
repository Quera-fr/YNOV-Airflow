from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta

import pandas as pd
from sklearn.datasets import load_iris
import sqlalchemy as db
from utiles.functions import *

def load_data():
    data = load_iris()
    df = pd.DataFrame(data.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])

def insert_data_to_db():
    # Création de la table IRIS DATA
    data = DataBaseV2(db_name='Iris_DATA', db_type='sqlite')
    data.create_table('iris_data', 
                    id_columns=db.Integer, 
                    sepal_length=db.Float, 
                    sepal_width=db.Float,
                    petal_length=db.Float,
                    petal_width=db.Float)


    # Injection dans la base de données
    n_lines = len(data.dataframe('iris_data'))

    for n in range(n_lines, n_lines+5):
        data_value = df.iloc[n]
        data.insert_row('iris_data',
                        id_columns=n,
                        sepal_length = data_value.sepal_length,
                        sepal_width = data_value.sepal_width,
                        petal_length = data_value.petal_length,
                        petal_width = data_value.petal_width)



with DAG(
    "my_training_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@once"):

    task_load_data = PythonOperator(task_id="task_load_data", 
                                    python_callable=load_data)

    task_insert_data_to_db = PythonOperator(task_id="task_insert_data_to_db", 
                                            python_callable=insert_data_to_db)

    task_load_data >> task_insert_data_to_db
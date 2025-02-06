FROM continuumio/miniconda3

WORKDIR /root/airflow

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY utiles/ /root/airflow/dags/plugins/utiles/

COPY Iris_DATA.db Iris_DATA.db

CMD airflow standalone
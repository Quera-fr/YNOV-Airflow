FROM continuumio/miniconda3

WORKDIR /root/airflow

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY dags/ dags/

COPY plugins/ plugins/

COPY train.py .

COPY airflow.db .

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID

ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

RUN echo $AWS_SECRET_ACCESS_KEY

CMD airflow standalone
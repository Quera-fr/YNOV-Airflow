import mlflow, os
from plugins.utiles.functions import DataBaseV2
from sklearn.tree import DecisionTreeClassifier

mlflow.set_tracking_uri("https://quera-server-mlflow-cda209265623.herokuapp.com/")
experiment = mlflow.set_experiment("Airflow-training")

data = DataBaseV2(db_name='/root/airflow/airflow', db_type='sqlite')
df = data.dataframe("iris_data")

with mlflow.start_run(
    experiment_id=experiment.experiment_id
    ):

    print(df.columns)

    X = df.drop(["y"], axis=1)
    y = df.y

    model = DecisionTreeClassifier()
    model.fit(X, y)

    mlflow.log_param('accuracy', model.score(X, y))
    mlflow.sklearn.log_model(model, "model")
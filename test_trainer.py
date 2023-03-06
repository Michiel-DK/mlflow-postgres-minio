# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import mlflow
import mlflow.sklearn
import os


EXPERIMENT_NAME = os.getenv('EXPERIMENT_NAME')
ARTIFACT_ROOT = os.getenv('ARTIFACT_ROOT')
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')


if __name__ == "__main__":
    # os.environ['MLFLOW_TRACKING_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/mlflow_db'
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://127.0.0.1:9100'
    os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'
    try:
        np.random.seed(40)

        # Read the wine-quality csv file from the URL
        csv_url =\
            'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
        data = pd.read_csv(csv_url, sep=';')

        # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data)

        # The predicted column is "quality" which is a scalar from [3, 9]
        train_x = train.drop(["quality"], axis=1)
        test_x = test.drop(["quality"], axis=1)
        train_y = train[["quality"]]
        test_y = test[["quality"]]
        
        try:
            mlflow.create_experiment(EXPERIMENT_NAME, artifact_location=ARTIFACT_ROOT)
            print('created new experiment')
            mlflow.set_experiment(EXPERIMENT_NAME)
        except:
            print('experiment already exists')
            mlflow.set_experiment(EXPERIMENT_NAME)

        with mlflow.start_run() as run:
            
            print("Active run_id: {}".format(run.info.run_id))
            
            model = Sequential()

            model.add(layers.Dense(10))
            model.add(layers.Dense(1, activation='linear'))

            model.compile(loss='mse', metrics='mse')
            
            mse = model.evaluate(test_x, test_y)[-1]

            mlflow.log_metric("mse", mse)
            mlflow.log_param("layers", len(model.layers))
            #mlflow.log_artifact("output.txt")
            mlflow.tensorflow.log_model(model,
                                        artifact_path="model",
                                        registered_model_name='test_model')
    except:
        import ipdb, traceback, sys

        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)

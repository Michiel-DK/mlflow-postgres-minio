CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow_user_pw';
GRANT all privileges ON DATABASE mlflow_db to mlflow_user;
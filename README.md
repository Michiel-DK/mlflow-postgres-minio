# Example structure for minio/docker/mlflow

### setup_mlflowdb.sql
.sql script that runs while building postgres container.
- creates ***mlflow_db***
- creates user: ***mlflow_user*** with password: ***mlflow_user_pw***
- grants all priveleges on the database with that user

### Dockerfile_postgres
Gets a **postgres alpine** image and runs the .sql script

### Dockerfile_mlflow
Installs **mlflow 2.1.1** in a python image and runs the mlflow server

### docker-compose.yml
Creates the different services:
- **postgres**:
    - mapped to 5532 for outside use
    - uses Dockerfile_postgres to build image
- **minio**:
    - maps console port 9000 -> 9900 for outside use
    - maps API port 9001 -> 9100 for outside use
    - runs Minio server on 9000/9001 inside container
- **mlflow**:
    - maps server port 5000 -> 5050 for outside use
    - uses Dockerfile_mlflow to build
    - uses AWS credentials to connect ot minio

### test_trainer.py
Simple tensorfow model to test logging on mlflow and minio

### still to do
- check why all tables saved under db mlflow_user
- script to create S3 bucket in minio for startup --> for now create manually before running a training
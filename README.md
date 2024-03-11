# Home Task - Data Engineer - 1

## Project Overview

This project, developed by [Your Name], encompasses a sophisticated ETL (Extract, Transform, Load) pipeline and a Flask-based REST API. The ETL pipeline efficiently processes CSV files, loading the data into a SQLite database. The API allows users to access the most recently ingested data by retrieving the first 10 lines. The entire solution has been meticulously uploaded and deployed on Kubernetes, ensuring seamless scalability and efficient management.

---

## Installation

To run this project locally, follow these steps:

1. **Clone this repository:**

    ```bash
    git clone git@github.com:chenenaoui/ETL_kubernetes.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

---

## Running the ETL Pipeline and API Locally

Utilizing Docker Compose simplifies the orchestration of your application's containers. 
Docker Compose defines and runs multi-container Docker applications, with configuration specified in a `docker-compose.yml` file. Follow these steps:

1. **Start the Docker containers:**

    ```bash
    docker-compose up -d
    ```

    This command launches the containers in detached mode, enabling them to run in the background.

2. **Check the status of the containers:**

    ```bash
    docker-compose ps
    ```

    This command provides information about the running containers, ensuring they are up and healthy.

    ![Docker Compose](./images/docker-compose.png)

    Access the API at [http://localhost:5000/read/first-chunck](http://127.0.0.1:5000/read/first-chunck)

3. **Stop and remove the containers:**

    ```bash
    docker-compose down
    ```

    This command stops and removes the running containers, freeing up resources. The Docker images used in this project are publicly available, making it easy for anyone to replicate and deploy the application. (The images are hosted on Docker Hub.)

    ![Docker Compose](./images/Screenshot%20from%202024-03-10%2002-43-06.png)

---

## Kubernetes Deployment

1. **Install Minikube and kubectl:**

    Before deploying the application to Kubernetes, ensure that Minikube and kubectl are installed. If not, use the following commands:

    ```bash
    # Install Minikube (Linux)
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
    sudo dpkg -i minikube_latest_amd64.deb
    
    # Install kubectl (Linux)
    sudo apt-get update && sudo apt-get install -y kubectl
    ```

2. **Start Minikube:**

    ```bash
    minikube start
    ```

3. **Deploy the application to Kubernetes:**

    ```bash
    kubectl apply -f kubernetes/api-deployment.yaml
    kubectl apply -f kubernetes/etl-deployment.yaml
    kubectl apply -f kubernetes/api-service.yaml
    kubectl apply -f kubernetes/data-output-pvc.yaml
    kubectl apply -f kubernetes/logs-pvc.yaml
    ```

    These commands deploy the API, ETL, and necessary services along with persistent volume claims for data and logs.

4. **Monitor the deployed resources:**

    ```bash
    kubectl get pods
    kubectl get services
    kubectl get pvc
    ```

    The image shows the status of the deployed pods, services, and persistent volume claims.

    ![Docker Compose](./images/check_services.png)

    You can also open Minikube Dashboard for a visual representation of your cluster:

    ```bash
    minikube dashboard
    ```

    ![Docker Compose](./images/dashboard.png)

5. **Access the API service using Minikube:**

    ```bash
    minikube service api-service --url
    ```

    When you run `minikube service api-service --url`, it will print the corresponding URL. 

    ```bash
    minikube service api-service
    ```

    The `minikube service api-service` command in Minikube is used to expose a Kubernetes service and open it in a default web browser.

    ![Docker Compose](./images/run_web_app.png)

    ![Docker Compose](./images/web_output.png)

6. **To access the pod where the Flask application is running, use:**

    ```bash
    kubectl exec -it <pod_name> -- /bin/sh
    ```

    To access logs from the running pods, use the following commands:

    ```bash
    cd logs
    cat api_logs.log
    cat etl_logs.log
    ```

    ![Docker Compose](./images/check_logs.png)

7. **These commands clean up all deployed resources in the Kubernetes cluster and stop Minikube:**

    ```bash
    kubectl delete all --all
    ```

    ```bash
    minikube stop
    ```

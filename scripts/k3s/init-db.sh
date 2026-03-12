#!/bin/bash

# Check minikube status and capture the exit code
minikube status > /dev/null 2>&1
STATUS_CODE=$?

if [ $STATUS_CODE -eq 0 ]; then
    echo "Minikube is running and all components are healthy."
else
    minikube start --cpus=24 --memory=16384mb --driver=docker
    minikube status
fi

kubectl apply -f database.yaml
kubectl port-forward service/mysql-service 3306:3306
#!/bin/bash
cd pod_creator
docker build -t pod-creator-webservice:latest .
echo "Built pod creator image"
echo "Role binding pod creator image to minikube..."
kubectl apply -f pod-creator-rbac.yaml
# echo "removing old images from minikube..."
# minikube image rm pod-creator-webservice:latest
echo "Loading pod creator image latest into Minikube..."
minikube image load pod-creator-webservice:latest
cd ..
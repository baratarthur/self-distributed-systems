#!/bin/bash
cd pod_creator
docker build -t pod-creator-webservice:v$1 .
echo "Built pod creator image"
echo "Loading pod creator image version $1 into Minikube..."
minikube image load pod-creator-webservice:v$1
cd ..
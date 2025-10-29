#!/bin/bash
echo "Building dana-main image version $1..."
docker build -t dana-main:v$1 -f Dockerfile.main .
echo "Built dana-main image"
echo "Loading dana-main image version $1 into Minikube..."
minikube image load dana-main:v$1
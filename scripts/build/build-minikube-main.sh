#!/bin/bash
echo "Building dana-main image latest..."
docker build -t dana-main:latest -f Dockerfile.main .
echo "Built dana-main image"
# echo "removing old images from minikube..."
# minikube image rm dana-main:latest
echo "Loading dana-main image latest into Minikube..."
minikube image load dana-main:latest
#!/bin/bash
echo "Building dana-remote image..."
docker build -t dana-remote:latest -f Dockerfile.remote .
echo "Built dana-remote image"
echo "removing old images from minikube..."
minikube image rm dana-remote:latest
echo "Loading dana-remote image into Minikube..."
minikube image load dana-remote:latest
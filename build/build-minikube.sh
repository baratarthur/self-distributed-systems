#!/bin/bash
# accepts $1 as version number on tag
# source ./build/build-minikube-pod_creator.sh $1
source ./build/build-minikube-main.sh $1
source ./build/build-minikube-remote.sh $1
echo "Re-deploying Dana in Minikube..."
kubectl delete -f ./dana-kube.yaml
echo "dana deleted."
echo "Re-deploying dana..."
kubectl apply -f ./dana-kube.yaml

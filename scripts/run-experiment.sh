#!/bin/bash
minikube delete
minikube start --cpus=6 --memory=2048mb --driver=docker
# 1-> app version, 2 -> experiment round
kubectl apply -f database.yaml
source ./scripts/build/compile.sh
source ./scripts/build/build-minikube.sh
echo "App version $1 built."
echo "Running experiment for 3m in $1 ..."
sleep 3m
# echo "Experiment round $1 finished."
# source ./data-retreive/copy-result.sh $1 30u
# echo "Copying logs from dana-main"
# source ./scripts/data-retreive/copy-logs.sh dana-main $1
# echo "Copying logs from post-repository-replicate-weak-1"
# source ./scripts/data-retreive/copy-logs.sh post-repository-replicate-weak-1 $1
# echo "running analysis for round $1 ..."
# python3 ./results/analisys.py $1
# echo "Analysis for round $1 done."
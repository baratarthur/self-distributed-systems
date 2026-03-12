#!/bin/bash
# 1-> app version, 2 -> experiment round
kubectl delete -f k6-manifest.yaml
kubectl delete -f k6-manifest-viral.yaml
echo "App version $1 built."
echo "Starting k6 user load..."
kubectl apply -f k6-manifest.yaml
sleep 1m
echo "Starting k6 viral load..."
kubectl apply -f k6-manifest-viral.yaml
sleep 1m
# echo "Experiment round $1 finished."
# source ./data-retreive/copy-result.sh $1 30u
# echo "Copying logs from dana-main"
# source ./scripts/data-retreive/copy-logs.sh dana-main $1
# echo "Copying logs from post-repository-replicate-weak-1"
# source ./scripts/data-retreive/copy-logs.sh post-repository-replicate-weak-1 $1
# echo "running analysis for round $1 ..."
# python3 ./results/analisys.py $1
# echo "Analysis for round $1 done."
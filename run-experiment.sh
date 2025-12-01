#!/bin/bash
# 1-> app version, 2 -> experiment round
source ./build/compile.sh
source ./build/build-minikube.sh
echo "App version $1 built."
echo "Running experiment round $1 ..."
sleep 26s
echo "33% finished ..."
sleep 25s
echo "66% finished ..."
sleep 25s
echo "99% finished ..."
sleep 3s
echo "Experiment round $1 finished."
source ./data-retreive/copy-result.sh $1
echo "Copying logs from dana-main"
source ./data-retreive/copy-logs.sh dana-main $1
echo "Copying logs from post-repository-replicate-weak-1"
source ./data-retreive/copy-logs.sh post-repository-replicate-weak-1 $1
# echo "running analysis for round $2 ..."
# python3 ./results/analisys.py $2
# echo "Analysis for round $2 done."
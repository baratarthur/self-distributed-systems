#!/bin/bash

# 1. Pega o nome
POD_NAME=$(kubectl get pods -l app=$1 -o jsonpath="{.items[0].metadata.name}")

# 2. Copia (O pod precisa estar rodando o comando sleep agora)
echo "Copiando logs do pod: $POD_NAME"
kubectl logs $POD_NAME > ./logs/$1-log-round$2.txt

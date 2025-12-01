#!/bin/bash

# 1. Espera o Pod estar rodando e pronto (opcional, mas bom para automação)
echo "Aguardando o pod iniciar..."
kubectl wait --for=condition=ready pod -l app=$1 --timeout=60s

# 2. Pega o nome
POD_NAME=$(kubectl get pods -l app=$1 -o jsonpath="{.items[0].metadata.name}")

# 3. Copia (O pod precisa estar rodando o comando sleep agora)
echo "Copiando logs do pod: $POD_NAME"
kubectl logs $POD_NAME > ./logs/$1-log-round$2.txt

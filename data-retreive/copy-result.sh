#!/bin/bash

# 1. Espera o Pod estar rodando e pronto (opcional, mas bom para automação)
echo "Aguardando o pod iniciar..."
kubectl wait --for=condition=ready pod -l app=k6-load-tester --timeout=60s

# 2. Pega o nome
POD_NAME=$(kubectl get pods -l app=k6-load-tester -o jsonpath="{.items[0].metadata.name}")

# 3. Copia (O pod precisa estar rodando o comando sleep agora)
echo "Copiando do pod: $POD_NAME"
kubectl cp $POD_NAME:/results/data.csv ./results/results_round$1.csv

# 4. (Opcional) Mata o pod manualmente se não quiser esperar o sleep acabar
kubectl delete pod $POD_NAME
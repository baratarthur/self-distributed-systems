kubectl apply -f database.yaml
kubectl port-forward service/mysql-service 3306:3306
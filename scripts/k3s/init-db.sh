kubectl apply -f database.yaml
kubectl port-forward service/mysql-service 30306:3306
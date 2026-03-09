source ./scripts/k3s/build-publish-main.sh
source ./scripts/k3s/build-publish-remote.sh

echo "Starting dana app in port 8080"
kubectl apply -f ./manifest.yaml

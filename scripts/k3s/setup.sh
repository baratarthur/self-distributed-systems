DIRECTORY="sds-proxy-generator"

if [ ! -d "$DIRECTORY" ]; then
    echo "Directory $DIRECTORY does not exist. Creating it now..."
    git clone https://github.com/baratarthur/sds-proxy-generator.git
    mkdir "$DIRECTORY"
fi

# source ./scripts/build/compile.sh

source ./scripts/k3s/build-publish-main.sh
source ./scripts/k3s/build-publish-remote.sh

echo "Starting dana app in port 8080"
kubectl apply -f ./manifest.yaml

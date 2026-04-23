DIRECTORY_PROXY="sds-proxy-generator"
# DIRECTORY_NATIVE_LIBRARIES="native_libraries"

if [ ! -d "$DIRECTORY_PROXY" ]; then
    echo "Directory $DIRECTORY_PROXY does not exist. Creating it now..."
    git clone https://github.com/baratarthur/sds-proxy-generator.git
    mkdir "$DIRECTORY_PROXY"
fi

# if [ ! -d "$DIRECTORY_NATIVE_LIBRARIES" ]; then
#     echo "Directory $DIRECTORY_NATIVE_LIBRARIES does not exist. Creating it now..."
#     git clone https://github.com/projectdana/native_libraries.git
#     mkdir "$DIRECTORY_NATIVE_LIBRARIES"
# fi

# cp custom/* native_libraries/

source ./scripts/k3s/build-publish-main.sh
source ./scripts/k3s/build-publish-remote.sh

echo "Starting dana app in port 8080"
kubectl apply -f ./manifest.yaml

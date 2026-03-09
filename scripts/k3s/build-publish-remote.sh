echo "Building and publishing the main image to the private registry..."
docker buildx build \
        --platform linux/amd64,linux/arm \
        --provenance=false \
        --sbom=false \
        -t my.private-registry.lan:5000/dana-remote:latest \
        --push \
        -f Dockerfile.remote .

docker tag dana-remote:latest my.private-registry.lan:5000/dana-remote:latest
docker push my.private-registry.lan:5000/dana-remote:latest

echo "Veryfying deploied image..."
curl -X GET http://my.private-registry.lan:5000/v2/_catalog
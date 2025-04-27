#!/bin/bash
set -e

# Print commands for better debugging
set -x

echo "=== Setting up local Kubernetes environment ==="

# 1. Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting."; exit 1; }
command -v minikube >/dev/null 2>&1 || { echo "Minikube is required but not installed. Aborting."; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "kubectl is required but not installed. Aborting."; exit 1; }

# 2. Start Minikube if not running
if ! minikube status | grep -q "Running"; then
    echo "Starting Minikube..."
    minikube start --driver=docker --cpus=2 --memory=4096
fi

# 3. Create data directory for persistent volume
minikube ssh "sudo mkdir -p /mnt/data && sudo chmod 777 /mnt/data"

# 4. Build Docker images
echo "=== Building Docker images ==="

# Build auth service
echo "Building auth-service image..."
cd auth-service
docker build -t auth-service:v1 .
cd ..

# Build data service
echo "Building data-service image..."
cd data-service
docker build -t data-service:v1 .
cd ..

# 5. Load images into Minikube
echo "=== Loading images into Minikube ==="
minikube image load auth-service:v1
minikube image load data-service:v1

# 6. Apply Kubernetes manifests
echo "=== Deploying to Kubernetes ==="

# Create the namespace if it doesn't exist
kubectl create namespace microservices --dry-run=client -o yaml | kubectl apply -f -

# Set the current context to use the namespace
kubectl config set-context --current --namespace=microservices

# Apply the manifests
kubectl apply -f k8s/data-deployment.yaml
kubectl apply -f k8s/auth-deployment.yaml
kubectl apply -f k8s/envoy-config.yaml
kubectl apply -f k8s/envoy-deployment.yaml
kubectl apply -f k8s/network-policies.yaml
kubectl apply -f k8s/horizontal-pod-autoscaler.yaml

# 7. Wait for deployments to be ready
echo "=== Waiting for deployments to be ready ==="
kubectl rollout status deployment/auth-service -n microservices
kubectl rollout status deployment/data-service -n microservices
kubectl rollout status deployment/envoy-proxy -n microservices

# 8. Get service URL
echo "=== Getting service URL ==="
MINIKUBE_IP=$(minikube ip)
echo "Your services are available at:"
echo "Envoy Proxy: http://$MINIKUBE_IP:30080"
echo "Envoy Admin: http://$MINIKUBE_IP:30901"

echo "=== Deployment completed successfully ==="
echo ""
echo "To test your deployment:"
echo "curl -X POST http://$MINIKUBE_IP:30080/auth -H \"Content-Type: application/json\" -d '{\"username\":\"user1\",\"password\":\"password1\"}'"
echo ""
echo "Then use the token in the response to access the data service:"
echo "curl -X POST http://$MINIKUBE_IP:30080/data -H \"Content-Type: application/json\" -H \"Authorization: Bearer YOUR_TOKEN\""

# Check pod status
echo "=== Current pod status ==="
kubectl get pods -n microservices

echo "=== To monitor your cluster, you can use k9s ==="

import os
from flask import Flask, request, jsonify
from kubernetes import client, config

app = Flask(__name__)

# --- Configuração do Cliente Kubernetes ---
# Carrega a configuração de dentro do cluster ou localmente
try:
    config.load_incluster_config()
except config.ConfigException:
    config.load_kube_config()

core_v1_api = client.CoreV1Api()


@app.route('/create-pod', methods=['POST'])
def create_pod_handler():
    data = request.get_json()
    if not data or 'pod_name' not in data or 'image_name' not in data:
        return jsonify({"error": "Requisição inválida. Forneça 'pod_name' e 'image_name'."}), 400

    pod_name = data['pod_name']
    image_name = data['image_name']
    namespace = os.getenv("POD_NAMESPACE", "default")
    
    # --- Criar o Pod no Kubernetes ---
    # O manifesto do pod agora usa diretamente a imagem fornecida
    pod_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": pod_name},
        "spec": {
            "containers": [{
                "name": f"{pod_name}-container",
                "image": image_name,
                "imagePullPolicy": "IfNotPresent"
            }]
        }
    }

    try:
        print(f"Criando o pod '{pod_name}' com a imagem '{image_name}' no namespace '{namespace}'")
        core_v1_api.create_namespaced_pod(
            namespace=namespace,
            body=pod_manifest
        )
    except client.ApiException as e:
        print(f"Erro na API do Kubernetes: {e.body}")
        return jsonify({"error": "Falha ao criar o pod no Kubernetes.", "details": e.body}), 500

    return jsonify({
        "message": "Pod criado com sucesso!",
        "pod_name": pod_name,
        "image_used": image_name
    }), 201

@app.route('/pod/<string:pod_name>', methods=['DELETE'])
def delete_pod_handler(pod_name):
    """Deleta um pod pelo nome."""
    namespace = os.getenv("POD_NAMESPACE", "default")
    
    try:
        print(f"Tentando deletar o pod '{pod_name}' no namespace '{namespace}'")
        core_v1_api.delete_namespaced_pod(
            name=pod_name, 
            namespace=namespace
        )
        return jsonify({"message": f"Pod '{pod_name}' deletado com sucesso."}), 200
        
    except client.ApiException as e:
        # Se o pod não for encontrado (código 404), retorna uma mensagem amigável
        if e.status == 404:
            return jsonify({"error": f"Pod '{pod_name}' não encontrado."}), 404
        
        # Para outros erros da API
        print(f"Erro na API do Kubernetes ao deletar: {e.body}")
        return jsonify({"error": "Falha ao deletar o pod.", "details": e.body}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
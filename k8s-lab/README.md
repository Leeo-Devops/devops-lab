# Kubernetes Lab (K3d)

Este diretório contém os manifestos e experimentos práticos de Kubernetes realizados no laboratório local (K3d - cluster de 4 nós).

## O que foi implementado:
- **Deployment:** Nginx com 2 réplicas para alta disponibilidade.
- **Service:** Exposição interna (ClusterIP) e NodePort.
- **Ingress:** Roteamento de tráfego HTTP pelo domínio `devopero.local`.
- **ConfigMap e Secret:** Separação de configurações e dados sensíveis.
- **Persistência (PVC):** Volume de 1Gi montado no Nginx para sobreviver à morte dos Pods.
- **Troubleshooting:** Simulação de `CrashLoopBackOff` e correção via `kubectl patch`.

## Como aplicar:
```bash
kubectl apply -f nginx-com-pvc.yaml
kubectl apply -f ingress.yaml


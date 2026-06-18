# Local Kubernetes Lab: K3s + Calico + Rancher Setup (Multi-Node Edition)

This repository documents the engineering process of setting up a lightweight, production-ready, multi-node local Kubernetes cluster. The primary goal of this environment is to host a resilient multi-tier application protected by strict internal firewall rules (Network Policies), distributed persistent storage, and a highly available, replicated database.

---

## 🏗️ Architecture Overview

To mirror real-world production constraints on local physical hardware, the cluster is decoupled from cloud provider infrastructure by leveraging a fully open-source bare-metal stack:

* **Orchestrator:** K3s (a lightweight, fully certified Kubernetes distribution) deployed in a Multi-Node topology (1 Control-Plane / Master + 1 Worker / Agent).
* **CNI (Container Network Interface):** Project Calico (deployed via Tigera Operator) providing robust Network Policy support and native compatibility with modern Linux `nftables`.
* **Storage Engine:** Longhorn (distributed block storage) to allow volume replication across distinct physical nodes.
* **Management Plane:** Rancher Manager (deployed via Helm + Cert-Manager) for visual monitoring, logs, and cluster governance.



---

## 🛠️ Step-by-Step Installation Guide

The procedures below were validated on local physical hosts running **Linux Mint (Ubuntu 24.04 Noble LTS base)** and **openSUSE**.

* **Control-Plane (Master Node):** `t14` (IP: `192.168.18.9`)
* **Worker Node (Agent):** `k3s-worker` (IP: `192.168.18.27`)

### 1. Custom K3s Control-Plane Installation (Master)
To allow Calico to manage internal network security natively, K3s must be installed without its default, unisolated networking engine (Flannel):

```bash
curl -sfL [https://get.k3s.io](https://get.k3s.io) | sh -s - --flannel-backend=none --disable-network-policy --data-dir=/home/k3s-root

```


#Configure non-root permissions so your local user can manage the cluster without typing sudo:

mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
export KUBECONFIG=~/.kube/config

# Persist the environment variable
echo "export KUBECONFIG=~/.kube/config" >> ~/.bashrc



2. Deploying Calico CNI (via Tigera Operator)
Using the Operator pattern is critical here; it automatically detects the K3s environment and correctly maps host CNI binary paths, avoiding volume mount conflicts standard manifests encounter on modern Ubuntu/Mint systems.

# Install the Custom Resource Definitions (CRDs) and the Operator
kubectl create -f [https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml](https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml)

# Apply the custom resource definition to initialize the network engine
kubectl create -f [https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/custom-resources.yaml](https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/custom-resources.yaml)

Verify cluster networking health:
kubectl get pods -n calico-system -w
kubectl get nodes



3. Package Management (Helm) & TLS Provisioning

Rancher requires an encrypted control plane. Helm is used to deploy cert-manager to handle internal TLS automated certificate generation.

# Install Helm CLI
curl [https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3](https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3) | bash

# Add official Helm repositories
helm repo add jetstack [https://charts.jetstack.io](https://charts.jetstack.io)
helm repo add rancher-stable [https://releases.rancher.com/server-charts/stable](https://releases.rancher.com/server-charts/stable)
helm repo update

# Install Cert-Manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true


4. Deploying Rancher Manager

Deploy the management dashboard into its own dedicated namespace:

helm install rancher rancher-stable/rancher \
  --namespace cattle-system \
  --create-namespace \
  --set hostname=rancher.local \
  --set bootstrapPassword=***

Monitor the deployment roll out until successful:
kubectl -n cattle-system rollout status deploy/rancher

5. Joining Worker Nodes (Multi-Node Expansion)

To transform the environment into a true multi-node cluster, extract the node token from the Master node:

sudo cat /home/k3s-root/server/node-token

curl -sfL [https://get.k3s.io](https://get.k3s.io) | K3S_URL=[https://master_local_ip:6443](https://master_local_ip:6443) \
  K3S_TOKEN="<YOUR_NODE_TOKEN>" \
  sh -s - agent

Validate that both nodes are working in tandem:
kubectl get nodes

🔍 Critical Troubleshooting & Engineering Notes
🚨 Issue 1: Calico Node IP Autodetection & Mesh Loops

Symptom: Calico pods entering CrashLoopBackOff or worker nodes stuck in NotReady with cni plugin not initialized errors. This happens because Calico might auto-detect a wrong interface (like a virtual bridge or Wi-Fi card) instead of the real physical LAN interface, creating mismatched subnets between nodes (e.g., Master on 192.168.100.X and Worker on 192.168.18.X).

Solution: Force the Tigera Operator to bind exclusively to the correct physical local subnet via a patch:
Bash

kubectl patch installations.operator.tigera.io default --type=merge -p '{"spec": {"calicoNetwork": {"nodeAddressAutodetectionV4": {"cidrs": ["192.168.18.0/24"]}}}}'

After patching, restart the network plane pods to flush the bad routing cache:
Bash

kubectl delete pod -n calico-system -l k8s-app=calico-node

🚨 Issue 2: Local Host Resolution (rancher.local)

Symptom: Browser returning Unable to connect / Connection Refused when accessing https://rancher.local.

Solution: Since the K3s Traefik Ingress controller exposes the ports 80/443 on both nodes dynamically, update your client machine's /etc/hosts file pointing explicitly to the cluster's physical IP instead of 127.0.0.1:
Bash

sudo echo "master_local_ip rancher.local" >> /etc/hosts

🚀 Next Milestone Tasks

    [x] Configure a resilient multi-node cluster topology.

    [x] Deploy Longhorn for distributed persistent storage.

    [ ] Install Gitea as the internal version control hub.

    [ ] Install the CloudNativePG operator to orchestrate a High-Availability PostgreSQL cluster with streaming replication.

    [ ] Implement strict label-based NetworkPolicies to enforce isolation between workloads.


# Local Multi-Node Cluster Topology

This directory tracks the declarative configuration and bare-metal physical architecture of the local laboratory. 

## 🖥️ Hardware & OS Distribution

The cluster operates across two distinct physical/virtual machines bridged via local networking:

| Node Name | Role | Hardware Platform | OS Distribution | Local IP |
| :--- | :--- | :--- | :--- | :--- |
| **t14** | Control-Plane, Master | ThinkPad T14    | Linux Mint 22.2 | `192.168.18.9` |
| **k3s-worker** | Agent, Worker | Virtual Machine (VirtualBox) | Linux Mint / Ubuntu Base | `192.168.18.27` |

## 🌐 Network Plane (Calico CNI Implementation)

To prevent mesh routing loops and ensure the Tigera Operator explicitly binds to the physical interface instead of virtual bridge alternatives (e.g., Docker bridges, local host-only adapters), the following subnet restriction was applied to the installation manifest:

* **Target Subnet:** `192.168.18.0/24`
* **Storage Engine Link:** Longhorn handles multi-node block replication directly through the `enp0s3` and host network cards on this subnet.

### Active Kubernetes Core Nodes
```bash
$ kubectl get nodes -o wide
NAME         STATUS   ROLES           AGE   VERSION        INTERNAL-IP
t14          Ready    control-plane   5h    v1.35.5+k3s1   192.168.18.9
k3s-worker   Ready    <none>          10m   v1.35.5+k3s1   192.168.18.27

**This doc talks about setting up OpenShift metrics based on Hawkular and
Prometheus. After following this document, we will have Hawkular, Prometheus
and Alert Manager accesible via OpenShift Web Console. We will also talk about
setting up kube-ops-view which will help us have a quick view of our OpenShift
cluster**

This document assumes that you have an OpenShift 3.9.0 cluster up and running.
If you don't have it already, take a look at
[cluster-upgrade](cluster-upgrade.md) and [logging-install](logging-install.md)
documents. Former talks about upgrading OpenShift cluster from 3.7.2 to 3.9.0
while latter talk about setting up a fresh 3.9.0 in brief since it's mainly
focussed on setting up logging stacks using EFK.

This doc is split between setting up metrics using Hawkular and then setting up
Prometheus to have a view of the metrics.

### Setup Hawkular

OpenShift metrics uses Cassandra DB to store the metrics. To read about storage
requirement, heapster, hawkular, etc. you can go through the
[documentation](https://docs.openshift.org/3.9/install_config/cluster_metrics.html)
on OKD (formerly Origin) website.

As mentioned in aforementioned docs link and also on official [Cassandra
docs](https://docs.openshift.org/3.9/install_config/cluster_metrics.html), it
is not recommended to use NFS storage with Cassandra. So, we first need to
create a PV that's based on `hostPath` and make it available to the cluster.

In the setup we tried things on, we created a `/logging` directory on master
node and exposed it as PV. Then, we made sure to use the same node for spinning
up OpenShift metrics pods by setting proper labels. Here's the yaml for the PV:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
    name: metrics-pv
spec:
    capacity:
        storage: 30Gi
    accessModes:
        - ReadWriteOnce
    persistentVolumeClaimPolicy: Recycle
    hostPath:
        path: "/logging"
```

We create this PV on master-1 and so we need to make sure that metrics pods
spin up on master-1. This can be done by setting specific label for the node
and specifying `nodeselector` in hosts file. Label can be added/modified by
doing:

```bash
$ oc edit nodes/<master-1>
```

And finally we need to add parameters to hosts file for metrics installation:

```
openshift_metrics_install_metrics=true
openshift_metrics_cassandra_storage_type=pv
openshift_metrics_cassandra_replicas=1
openshift_metrics_cassandra_nodeselector={'node-type': 'metrics'}
openshift_metrics_image_version=v3.9
```

The overall hosts file will look like this:

```bash
# Create an OSEv3 group that contains the masters and nodes groups
[OSEv3:children]
masters
nodes
etcd

# Set variables common for all OSEv3 hosts
[OSEv3:vars]
# SSH user, this user should allow ssh based auth without requiring a password
ansible_ssh_user=root

# If ansible_ssh_user is not root, ansible_become must be set to true
# ansible_become=true
# containerized=true
debug_level=4

openshift_master_api_port=8443
# openshift_master_console_port=8756
openshift_deployment_type=origin
openshift_release=v3.9
os_firewall_use_firewalld=true
openshift_clock_enabled=false
openshift_pkg_version=-3.9.0
openshift_enable_service_catalog=false
openshift_docker_insecure_registries=172.29.33.8:5000
openshift_docker_additional_registries=172.29.33.8:5000
openshift_master_default_subdomain={{ hostvars[groups['masters'][0]].openshift_ip }}.nip.io
openshift_rolling_restart_mode=system

# logging stack
openshift_logging_install_logging=true
openshift_logging_es_cluster_size=1
openshift_logging_es_memory_limit=2G
openshift_logging_elasticsearch_storage_type="hostmount"
openshift_logging_elasticsearch_hostmount_path="/logging"
openshift_logging_elasticsearch_nodeselector={'node-type': 'logging'}

# logging stack for ops
openshift_logging_use_ops=true
openshift_logging_es_ops_cluster_size=1
openshift_logging_es_ops_memory_limit=2G

# metrics stack
openshift_metrics_install_metrics=true
openshift_metrics_cassandra_storage_type=pv
openshift_metrics_cassandra_replicas=1
openshift_metrics_cassandra_nodeselector={'node-type': 'metrics'}
openshift_metrics_image_version=v3.9

# uncomment the following to enable htpasswd authentication; defaults to DenyAllPasswordIdentityProvider
openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider', 'filename': '/etc/origin/master/htpasswd'}]

# default selectors for router and registry services
openshift_router_selector='region=infra'
openshift_registry_selector='region=infra'
openshift_disable_check=docker_storage,memory_availability

# host group for masters
[masters]
os-master-[1:2].lon1.centos.org

# host group for etcd
[etcd]
os-node-[1:2].lon1.centos.org

# host group for nodes, includes region info
[nodes]
os-master-1.lon1.centos.org openshift_node_labels="{'region': 'infra','zone': 'default','purpose':'infra', 'node-type': 'metrics'}" openshift_schedulable=true openshift_ip=172.29.33.36
os-master-2.lon1.centos.org openshift_node_labels="{'region': 'infra','zone': 'default','purpose':'infra', 'node-type': 'logging'}" openshift_schedulable=true openshift_ip=172.29.33.46
os-node-1.lon1.centos.org openshift_node_labels="{'region':'primary','zone': 'default','purpose':'prod', 'node-type': 'logging'}" openshift_schedulable=true openshift_ip=172.29.33.23
os-node-2.lon1.centos.org openshift_node_labels="{'region':'primary','zone': 'default','purpose':'prod', 'node-type': 'logging'}" openshift_schedulable=true openshift_ip=172.29.33.52
```

Now we can start metrics installation by doing:

```bash
$ time ansible-playbook -i openshift-cluster/hosts.39 /usr/share/ansible/openshift-ansible/playbooks/openshift-metrics/config.yml -vvv
```

Once the installation is over, metrics related pods, routes, etc. will show up
under the project `openshift-infra` on the OpenShift Web Console. Hawkular will
have a route exposed which can be used to make API requests. Other than that,
its web interface shows nothing but a static page.

#### Kube-Ops-View

[Kube-Ops-View](https://github.com/hjacobs/kube-ops-view) is a read-only
dashboard for multiple Kubernetes clusters. Kube-ops-view requires OpenShift
Metrics to be successfully setup and running. We have referred [this OpenShift
blog](https://blog.openshift.com/full-cluster-capacity-management-monitoring-openshift/)
to bring up kube-ops-view.

We're going to use it's forked version tailored for use with OpenShift. It's
available on [GitHub](https://github.com/raffaelespazzoli/kube-ops-view/tree/ocp).

Copy the `~/.kube/config` file on master-1 to your laptop. If you need to use
`sshuttle` or any other tool to connect to the remote OpenShift cluster's
network, do that first. With that in place, run below steps to have a kube-ops
dashboard accessible on your laptop at localhost:8080:

```bash
$ oc login -u system:admin --config /path/to/kubeconfig/on/laptop
$ oc proxy --config /path/to/kubeconfig/on/laptop
$ docker run -it --net=host raffaelespazzoli/ocp-ops-view
```

If you didn't face any error(s) in above steps, open the URL
http://localhost:8080 in your browser.

### Setup Prometheus

Prometheus is used for viewing the metrics being collected by heapster and
stored in Cassandra in earlier part of this document.

To read more about seting up Prometheus, read through the [documentation
here](https://docs.okd.io/3.9/install_config/cluster_metrics.html#openshift-prometheus).

For our setup, we will need to bring up three PVs to be used by each of
prometheus, alert-manager and alert-buffer. Unlike seting up OpenShift Metrics,
we can use NFS based PVs here. A sample PV yaml file is given below:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: prometheus
  namespace: cccp
spec:
  capacity:
    storage: 10Gi 
  accessModes:
  - ReadWriteOnce 
  nfs: 
    path: /prometheus
    server: 127.0.0.1
  persistentVolumeReclaimPolicy: Recycle
```
Make sure to use correct IP address above instead of 127.0.0.1. Spin up three
PVs. There's no guarantee that prometheus deployment will grab the prometheus
PV. We are naming it only for our understanding.

With the three extra PVs available in the cluster, let's add below parameters
to hosts file:

```
# prometheus stack
openshift_hosted_prometheus_deploy=false
openshift_prometheus_node_selector={'node-type': 'metrics'}
openshift_prometheus_storage_type=pvc
openshift_prometheus_alertmanager_storage_type=pvc
openshift_prometheus_alertbuffer_storage_type=pvc
```

The hosts file now looks like:

```
# Create an OSEv3 group that contains the masters and nodes groups
[OSEv3:children]
masters
nodes
etcd

# Set variables common for all OSEv3 hosts
[OSEv3:vars]
# SSH user, this user should allow ssh based auth without requiring a password
ansible_ssh_user=root

# If ansible_ssh_user is not root, ansible_become must be set to true
# ansible_become=true
# containerized=true
debug_level=4

openshift_master_api_port=8443
# openshift_master_console_port=8756
openshift_deployment_type=origin
openshift_release=v3.9
os_firewall_use_firewalld=true
openshift_clock_enabled=false
openshift_pkg_version=-3.9.0
openshift_enable_service_catalog=false
openshift_docker_insecure_registries=172.29.33.8:5000
openshift_docker_additional_registries=172.29.33.8:5000
openshift_master_default_subdomain={{ hostvars[groups['masters'][0]].openshift_ip }}.nip.io
openshift_rolling_restart_mode=system

# logging stack
openshift_logging_install_logging=true
openshift_logging_es_cluster_size=1
openshift_logging_es_memory_limit=2G
openshift_logging_elasticsearch_storage_type="hostmount"
openshift_logging_elasticsearch_hostmount_path="/logging"
openshift_logging_elasticsearch_nodeselector={'node-type': 'logging'}

# logging stack for ops
openshift_logging_use_ops=true
openshift_logging_es_ops_cluster_size=1
openshift_logging_es_ops_memory_limit=2G

# metrics stack
openshift_metrics_install_metrics=true
openshift_metrics_cassandra_storage_type=pv
openshift_metrics_cassandra_replicas=1
openshift_metrics_cassandra_nodeselector={'node-type': 'metrics'}
openshift_metrics_image_version=v3.9

# prometheus stack
openshift_hosted_prometheus_deploy=false
openshift_prometheus_node_selector={'node-type': 'metrics'}
openshift_prometheus_storage_type=pvc
openshift_prometheus_alertmanager_storage_type=pvc
openshift_prometheus_alertbuffer_storage_type=pvc

# uncomment the following to enable htpasswd authentication; defaults to DenyAllPasswordIdentityProvider
openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider', 'filename': '/etc/origin/master/htpasswd'}]

# default selectors for router and registry services
openshift_router_selector='region=infra'
openshift_registry_selector='region=infra'
openshift_disable_check=docker_storage,memory_availability

# host group for masters
[masters]
os-master-[1:2].lon1.centos.org

# host group for etcd
[etcd]
os-node-[1:2].lon1.centos.org

# host group for nodes, includes region info
[nodes]
os-master-1.lon1.centos.org openshift_node_labels="{'region': 'infra','zone': 'default','purpose':'infra', 'node-type': 'metrics'}" openshift_schedulable=true openshift_ip=172.29.33.36
os-master-2.lon1.centos.org openshift_node_labels="{'region': 'infra','zone': 'default','purpose':'infra', 'node-type': 'logging'}" openshift_schedulable=true openshift_ip=172.29.33.46
os-node-1.lon1.centos.org openshift_node_labels="{'region':'primary','zone': 'default','purpose':'prod', 'node-type': 'logging'}" openshift_schedulable=true openshift_ip=172.29.33.23
os-node-2.lon1.centos.org openshift_node_labels="{'region':'primary','zone': 'default','purpose':'prod', 'node-type': 'logging'}" openshift_schedulable=true openshift_ip=172.29.33.52
```

Let's install Prometheus:

```bash
$ time ansible-playbook -i openshift-cluster/hosts.39 /usr/share/ansible/openshift-ansible/playbooks/openshift-prometheus/config.yml -vvv
```

If the above command finished without any errors, go to the openshift-metrics
project on OpenShift Web Console and check for the various routes exposed by
Prometheus, Alert Manager and Alert Buffer.

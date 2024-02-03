import logging
import os, yaml
from kubernetes import client, config
from devopschatenginee.constraints.constants import Constants
from datetime import datetime
from typing import List, Dict, Any, Optional, Union

class KubernetesAction:
    
    @staticmethod
    def load_k8s_config(file_path: str) -> Optional[Dict[str, Any]]:
        """Load the k8s config from a file."""
        try:
            with open(file_path, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
        
    @staticmethod
    def get_k8s_cluster_names(config_path=Constants.K8S_CONFIG_PATH) -> Optional[List[str]]:
        if not os.path.exists(config_path):
            print(f"Config path: {config_path} doesn't exist.")
            return

        cluster_names = []

        for file in os.listdir(config_path):
            file_path = os.path.join(config_path, file)

            if os.path.isfile(file_path):
                config = KubernetesAction.load_k8s_config(file_path)

                if 'clusters' in config:
                    for cluster in config['clusters']:
                        if 'name' in cluster:
                            cluster_names.append(cluster['name'])

        return cluster_names

    @staticmethod
    def get_k8s_config(cluster_name, config_path=Constants.K8S_CONFIG_PATH) -> Optional[List[str]]:
        if not os.path.exists(config_path):
            print(f"Config path: {config_path} doesn't exist.")
            return

        for file in os.listdir(config_path):
            file_path = os.path.join(config_path, file)

            if os.path.isfile(file_path):
                config = KubernetesAction.load_k8s_config(file_path)

                if 'clusters' in config:
                    for cluster in config['clusters']:
                        if 'name' in cluster and cluster['name'] == cluster_name:
                            return file_path

        print(f"No config found for cluster: {cluster_name}")
        return None

    @staticmethod
    def get_k8s_namespaces(cluster_name: str) -> Optional[List[str]]:
        # Get the config file for the specified cluster
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            return None

        config.load_kube_config(config_file=config_path)

        v1 = client.CoreV1Api()

        # Get the list of namespaces
        namespaces_list = v1.list_namespace().items

        namespaces = []
        for ns in namespaces_list:
            namespaces.append(ns.metadata.name)

        return namespaces

    @staticmethod
    def get_k8s_resource(resource_type: str, cluster_name: str, namespace: str) -> Optional[List[str]]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)
        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return

        config.load_kube_config(config_file=config_path)
        api_instance = client.AppsV1Api()

        if resource_type.lower() == 'deployment':
            resource_list = api_instance.list_namespaced_deployment(namespace)
        elif resource_type.lower() == 'statefulset':
            resource_list = api_instance.list_namespaced_stateful_set(namespace)
        elif resource_type.lower() == 'daemonset':
            resource_list = api_instance.list_namespaced_daemon_set(namespace)
        else:
            print(f"Unsupported resource type: {resource_type}")
            return

        resources = [res.metadata.name for res in resource_list.items]
        return resources

    @staticmethod
    def restart_k8s_resource(resource_type: str, namespace: str, resource_name: str, cluster_name: str) -> Optional[str]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return

        try:
            config.load_kube_config(config_file=config_path)
            api_instance = client.AppsV1Api()

            # get the resource object based on its type
            if resource_type.lower() == 'deployment':
                resource = api_instance.read_namespaced_deployment(resource_name, namespace)
                update_func = api_instance.replace_namespaced_deployment
            elif resource_type.lower() == 'statefulset':
                resource = api_instance.read_namespaced_stateful_set(resource_name, namespace)
                update_func = api_instance.replace_namespaced_stateful_set
            elif resource_type.lower() == 'daemonset':
                resource = api_instance.read_namespaced_daemon_set(resource_name, namespace)
                update_func = api_instance.replace_namespaced_daemon_set
            else:
                print(f"Unsupported resource type: {resource_type}")
                return

            # check if annotations is None and initialize it if it is
            if resource.spec.template.metadata.annotations is None:
                resource.spec.template.metadata.annotations = {}

            resource.spec.template.metadata.annotations['kubectl.kubernetes.io/restartedAt'] = datetime.now().isoformat()

            # update the resource
            update_func(resource_name, namespace, resource)
        except client.ApiException as e:
            print(f"An exception occurred when trying to restart the {resource_type}: {e}")
            return f"Failed to restart {resource_type} {resource_name} in namespace {namespace} due to: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"Failed to restart {resource_type} due to an unexpected error: {e}"

        return f"{resource_type}.apps/{resource_name} restarted."

    @staticmethod
    def get_k8s_resource_status(resource_type: str, namespace: str, resource_name: str, cluster_name: str) -> List[str]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return []

        try:
            config.load_kube_config(config_file=config_path)
            v1 = client.CoreV1Api()
            api_instance = client.AppsV1Api()

            if resource_type.lower() == 'deployment':
                resource = api_instance.read_namespaced_deployment(resource_name, namespace)
            elif resource_type.lower() == 'statefulset':
                resource = api_instance.read_namespaced_stateful_set(resource_name, namespace)
            elif resource_type.lower() == 'daemonset':
                resource = api_instance.read_namespaced_daemon_set(resource_name, namespace)
            else:
                print(f"Unsupported resource type: {resource_type}")
                return []

            # extract the labels from the resource to form a label selector
            label_selector = ",".join([f"{k}={v}" for k, v in resource.spec.template.metadata.labels.items()])

            # get the list of pods using the label selector
            pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)

            # loop through the pods and collect their status
            pod_statuses = []
            for i in pods.items:
                pod_statuses.append(f"Pod: {i.metadata.name}, Status: {i.status.phase}")

        except client.ApiException as e:
            print(f"An exception occurred when trying to list the pods: {e}")
            return [f"Failed to list pods in namespace {namespace} due to: {e}"]
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return [f"Failed to list pods due to an unexpected error: {e}"]

        return pod_statuses

    @staticmethod
    def get_k8s_pod_names_for_resource(resource_type: str, namespace: str, resource_name: str, cluster_name: str) -> List[str]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return []

        try:
            config.load_kube_config(config_file=config_path)
            v1 = client.CoreV1Api()
            api_instance = client.AppsV1Api()

            if resource_type.lower() == 'deployment':
                resource = api_instance.read_namespaced_deployment(resource_name, namespace)
            elif resource_type.lower() == 'statefulset':
                resource = api_instance.read_namespaced_stateful_set(resource_name, namespace)
            elif resource_type.lower() == 'daemonset':
                resource = api_instance.read_namespaced_daemon_set(resource_name, namespace)
            else:
                print(f"Unsupported resource type: {resource_type}")
                return []

            # extract the labels from the resource to form a label selector
            label_selector = ",".join([f"{k}={v}" for k, v in resource.spec.selector.match_labels.items()])

            # get the list of pods using the label selector
            pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)

            # loop through the pods and collect their names
            pod_names = [pod.metadata.name for pod in pods.items]
        except client.ApiException as e:
            print(f"An exception occurred when trying to list the pods: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

        return pod_names

    @staticmethod
    def get_k8s_pod_logs(resource_type: str, namespace: str, resource_name: str, cluster_name: str, pod_name: Optional[str] = None, tail_lines: int = 10) -> Optional[str]:
        # I've left the resource_type and resource_name parameters in place even though they're not used,
        # as you might want to use them in future.
        
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            logging.error(f"No config found for cluster: {cluster_name}")
            return None

        try:
            config.load_kube_config(config_file=config_path)
            v1 = client.CoreV1Api()

            if pod_name is None:
                pod_name = resource_name

            # Get the last 'tail_lines' lines of logs
            log = v1.read_namespaced_pod_log(pod_name, namespace, tail_lines=tail_lines)

            return log
        except client.ApiException as e:
            logging.error(f"Exception occurred when trying to get the logs for the pod {pod_name}: {e}")
            return f"Failed to get logs for pod {pod_name} in namespace {namespace} due to: {e}"
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return f"Failed to get logs for pod due to an unexpected error: {e}"

    @staticmethod
    def get_k8s_all_rollback_revisions(resource_type: str, namespace: str, resource_name: str, cluster_name: str) -> Optional[List[int]]:
        if resource_type.lower() != "deployment":
            print("The resource type must be a deployment for getting rollback revisions.")
            return None

        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return None

        try:
            config.load_kube_config(config_file=config_path)
            api_instance = client.AppsV1Api()

            # Fetch the deployment
            deployment = api_instance.read_namespaced_deployment(resource_name, namespace)
            # Fetch all ReplicaSets
            rs = api_instance.list_namespaced_replica_set(namespace)
            # Filter ReplicaSets created by the deployment
            related_rs = [r for r in rs.items if r.metadata.owner_references[0].name == resource_name]
            # Get all revisions from the ReplicaSets and sort them
            revisions = sorted([int(rs.metadata.annotations["deployment.kubernetes.io/revision"]) for rs in related_rs])

            return revisions
        except client.ApiException as e:
            print(f"An exception occurred when trying to get the rollback revisions: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def rollback_k8s_resource_to_revision(resource_type: str, namespace: str, resource_name: str, cluster_name: str, revision_number: int) -> Optional[str]:
        if resource_type.lower() != "deployment":
            print("The resource type must be a deployment for rolling back revisions.")
            return None

        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return None

        try:
            config.load_kube_config(config_file=config_path)
            api_instance = client.AppsV1Api()

            # Fetch the target ReplicaSet based on the revision_number
            rs_list = api_instance.list_namespaced_replica_set(namespace)
            target_rs = next((rs for rs in rs_list.items if int(rs.metadata.annotations["deployment.kubernetes.io/revision"]) == revision_number), None)

            if target_rs is None:
                print(f"Revision number {revision_number} does not exist for deployment {resource_name}")
                return None

            # Update the deployment to match the target ReplicaSet's spec
            deployment = api_instance.read_namespaced_deployment(resource_name, namespace)
            deployment.spec.template = target_rs.spec.template

            # Apply the updated deployment
            api_instance.patch_namespaced_deployment(resource_name, namespace, deployment)
        except client.ApiException as e:
            print(f"An exception occurred when trying to rollback the deployment: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

        return f"{resource_type}.apps/{resource_name} rolled back to revision {revision_number}"

    @staticmethod
    def get_k8s_nodes(cluster_name: str) -> Union[List[str], str]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)
        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return None

        config.load_kube_config(config_file=config_path)
        v1 = client.CoreV1Api()

        try:
            nodes = v1.list_node().items
            node_names = [node.metadata.name for node in nodes]
            return node_names
        except client.ApiException as e:
            print(f"An exception occurred when trying to get nodes: {e}")
            return f"Failed to get nodes due to: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"Failed to get nodes due to an unexpected error: {e}"

    @staticmethod
    def get_k8s_nodes_status(cluster_name: str) -> Optional[List[Dict[str, Union[str, int, datetime]]]]:
        # Get the config file for the specified cluster
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            return None

        config.load_kube_config(config_file=config_path)

        v1 = client.CoreV1Api()

        # Get the list of nodes
        nodes_list = v1.list_node().items

        nodes_status = []
        for node in nodes_list:
            # node.status.conditions is a list, and the "Ready" condition is what we usually mean by "status"
            for condition in node.status.conditions:
                if condition.type == "Ready":
                    node_roles = []
                    for key in node.metadata.labels:
                        if 'node-role.kubernetes.io' in key:
                            # The role is defined as the part after the final slash
                            node_roles.append(key.split('/')[-1])
                    node_age = (datetime.now(node.metadata.creation_timestamp.tzinfo) - node.metadata.creation_timestamp).days
                    node_version = node.status.node_info.kubelet_version

                    nodes_status.append({
                        'node': node.metadata.name,
                        'status': condition.status,
                        'roles': ', '.join(node_roles) if node_roles else 'None',
                        'age': f'{node_age} days',
                        'version': node_version,
                        'last_heartbeat_time': condition.last_heartbeat_time
                    })

        return nodes_status

    @staticmethod
    def describe_k8s_node(cluster_name: str, node_name: str) -> Union[Dict[str, Union[str, Dict[str, str], Dict[str, Any]]], str, None]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)
        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return None

        config.load_kube_config(config_file=config_path)
        v1 = client.CoreV1Api()

        try:
            node = v1.read_node(name=node_name)
            node_info = {
                "name": node.metadata.name,
                "labels": node.metadata.labels,
                "annotations": node.metadata.annotations,
                "capacity": node.status.capacity,
                "allocatable": node.status.allocatable,
                "addresses": {a.type: a.address for a in node.status.addresses},
                "nodeInfo": node.status.node_info.to_dict(),
            }
            return node_info
        except client.ApiException as e:
            print(f"An exception occurred when trying to describe the node {node_name}: {e}")
            return f"Failed to describe node {node_name} due to: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"Failed to describe node due to an unexpected error: {e}"

    @staticmethod
    def get_k8s_node_capacity(cluster_name: str) -> Optional[Dict[str, Dict[str, int]]]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return None

        try:
            # Load kube config
            config.load_kube_config(config_file=config_path)
            # Create API client
            api = client.CoreV1Api()

            node_list = api.list_node()

            node_capacity = {}
            for node in node_list.items:
                node_name = node.metadata.name
                cpu_capacity = int(node.status.capacity["cpu"]) * 1000000  # Convert from millicores to 'n'
                memory_capacity = int(node.status.capacity["memory"][:-2])  # Remove 'Ki' and convert to int

                node_capacity[node_name] = {
                    'cpu_capacity': cpu_capacity,
                    'memory_capacity': memory_capacity,
                }

            return node_capacity

        except client.ApiException as e:
            print(f"An exception occurred when trying to get the node capacity: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def get_k8s_node_resources(cluster_name: str) -> Optional[List[Dict[str, Union[str, int]]]]:
        config_path = KubernetesAction.get_k8s_config(cluster_name)

        if config_path is None:
            print(f"No config found for cluster: {cluster_name}")
            return None

        try:
            # Load kube config
            config.load_kube_config(config_file=config_path)
            # Create API client
            api = client.CustomObjectsApi()

            node_metrics = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")

            node_resources = []
            for item in node_metrics['items']:
                node_name = item['metadata']['name']
                cpu_usage = int(item['usage']['cpu'][:-1])  # Remove 'n' and convert to int
                memory_usage = int(item['usage']['memory'][:-2])  # Remove 'Ki' and convert to int

                node_resources.append({
                    'node': node_name,
                    'cpu_usage': cpu_usage,
                    'memory_usage': memory_usage,
                })

            return node_resources
        
        except client.ApiException as e:
            print(f"An exception occurred when trying to get the node resources: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
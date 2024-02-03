
class Constants:
    (
        ACTION_SELECT,
        COMPONENT_PICK,
    ) = map(chr, range(2))

    (
        RETURN_PREV,
        RETURN_START,
        END_SESSION,
    ) = map(chr, range(2, 5))

    (
        K8S_ENV_CHOOSE,
        K8S_RESOURCETYPE_DEFINE,
        K8S_NODE_DEFINE,
        K8S_NODE_LIST_DEFINE,
        K8S_NAMESPACE_DEFINE,
        K8S_RESOURCE_DEFINE,
        K8S_OPERATION_PERFORM,
        K8S_OPERATION_HISTORY,
        K8S_OPERATION_LOG,
    ) = map(chr, range(5, 14))

    (
        COMPONENT_K8S,
        COMPONENT_GITLAB,
        COMPONENT_ES,
        COMPONENT_MINIO,
    ) = map(chr, range(14, 18))

    (
        K8S_POD_RESTART,
        K8S_POD_ROLLBACK_HISTORY,
        K8S_POD_STATUS_CHECK,
        K8S_POD_LOG_VIEW,
    ) = map(chr, range(18, 22))

    (
        K8S_NODE_STATUS,
        K8S_NODE_DESCRIBE,
        K8S_NODE_SHOW_RESOURCE,
    ) = map(chr, range(22, 25))

    K8S_RESOURCE_TYPES = ['node', 'deployment', 'statefulset', 'daemonset']
    K8S_CONFIG_PATH = 'settings/kube_config'

from devopschatenginee.constraints.constants import Constants
from devopschatenginee.managers.chatops_manager import ChatOpsManager
from devopschatenginee.managers.kubernetes_manager import KubernetesManager
from typing import Dict, List
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
)

class ChatStates:
    # ACTION_SELECT: The user is choosing between different actions
    ACTION_SELECT: Dict[str, List[CallbackQueryHandler]] = {
        Constants.ACTION_SELECT: [
            # When the user chooses to pick a component, it will transition to the COMPONENT_PICK state
            CallbackQueryHandler(ChatOpsManager.select_component, pattern="^" + str(Constants.COMPONENT_PICK) + "$"),
            # The "terminate_session" command will end session the conversation
            CallbackQueryHandler(ChatOpsManager.terminate_session, pattern="^" + str(Constants.END_SESSION) + "$"),
        ]
    }
    # COMPONENT_PICK: The user is choosing a component
    COMPONENT_PICK: Dict[str, List[CallbackQueryHandler]] = {
        Constants.COMPONENT_PICK: [
            CallbackQueryHandler(KubernetesManager.k8s_env_choose, pattern="^" + str(Constants.COMPONENT_K8S) + "$"),
            # The "start_return_prev" command will return the conversation to the start state
            CallbackQueryHandler(ChatOpsManager.start_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            ]
    }
    K8S_ENV_CHOOSE: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_ENV_CHOOSE: [
            CallbackQueryHandler(KubernetesManager.k8s_resource_type_define, pattern=f"^(?!({str(Constants.RETURN_PREV)}|{str(Constants.RETURN_START)})).*$"),
            CallbackQueryHandler(ChatOpsManager.select_component_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_RESOURCETYPE_DEFINE: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_RESOURCETYPE_DEFINE: [
            CallbackQueryHandler(KubernetesManager.k8s_node_define, pattern="^" + 'node' + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_namespace_define, pattern="^" + 'deployment' + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_namespace_define, pattern="^" + 'daemonset' + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_namespace_define, pattern="^" + 'statefulset' + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_env_choose_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_NODE_DEFINE: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_NODE_DEFINE: [
            CallbackQueryHandler(KubernetesManager.k8s_node_status, pattern="^" + str(Constants.K8S_NODE_STATUS) + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_node_show_resource, pattern="^" + str(Constants.K8S_NODE_SHOW_RESOURCE) + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_node_list, pattern="^" + str(Constants.K8S_NODE_DESCRIBE) + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_resource_type_define_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_NODE_LIST_DEFINE: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_NODE_LIST_DEFINE: [
            CallbackQueryHandler(KubernetesManager.k8s_node_describe, pattern=f"^(?!({str(Constants.RETURN_PREV)}|{str(Constants.RETURN_START)})).*$"),
            CallbackQueryHandler(KubernetesManager.k8s_node_define_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_NAMESPACE_DEFINE: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_NAMESPACE_DEFINE: [
            CallbackQueryHandler(KubernetesManager.k8s_resource_define, pattern=f"^(?!({str(Constants.RETURN_PREV)}|{str(Constants.RETURN_START)})).*$"),
            CallbackQueryHandler(KubernetesManager.k8s_resource_type_define_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_RESOURCE_DEFINE: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_RESOURCE_DEFINE: [
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform, pattern=f"^(?!({str(Constants.RETURN_PREV)}|{str(Constants.RETURN_START)})).*$"),
            CallbackQueryHandler(KubernetesManager.k8s_namespace_define_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_OPERATION_PERFORM: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_OPERATION_PERFORM: [
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_restart, pattern="^" + str(Constants.K8S_POD_RESTART) + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_status, pattern="^" + str(Constants.K8S_POD_STATUS_CHECK) + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_pod_log, pattern="^" + str(Constants.K8S_POD_LOG_VIEW) + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_rollback_history, pattern="^" + str(Constants.K8S_POD_ROLLBACK_HISTORY) + "$"),
            CallbackQueryHandler(KubernetesManager.k8s_resource_define_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_OPERATION_HISTORY: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_OPERATION_HISTORY: [
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_rollback, pattern=f"^(?!({str(Constants.RETURN_PREV)}|{str(Constants.RETURN_START)})).*$"),
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_rollback_history_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }
    K8S_OPERATION_LOG: Dict[str, List[CallbackQueryHandler]] = {
        Constants.K8S_OPERATION_LOG: [
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_log, pattern=f"^(?!({str(Constants.RETURN_PREV)}|{str(Constants.RETURN_START)})).*$"),
            CallbackQueryHandler(KubernetesManager.k8s_operation_perform_pod_log_return_prev, pattern="^" + str(Constants.RETURN_PREV) + "$"),
            CallbackQueryHandler(ChatOpsManager.return_to_start, pattern="^" + str(Constants.RETURN_START) + "$"),
        ]
    }

    @classmethod
    def get_entry_points(cls):
        return [CommandHandler("start", ChatOpsManager.start_operation)]

    @classmethod
    def get_states(cls):
        return {
            **cls.ACTION_SELECT,
            **cls.COMPONENT_PICK,
            **cls.K8S_ENV_CHOOSE,
            **cls.K8S_RESOURCETYPE_DEFINE,
            **cls.K8S_NODE_DEFINE,
            **cls.K8S_NODE_LIST_DEFINE,
            **cls.K8S_NAMESPACE_DEFINE,
            **cls.K8S_RESOURCE_DEFINE,
            **cls.K8S_OPERATION_PERFORM,
            **cls.K8S_OPERATION_HISTORY,
            **cls.K8S_OPERATION_LOG,
        }

    @classmethod
    def get_fallbacks(cls):
        return [CommandHandler("start", ChatOpsManager.start_operation)]
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from devopschatenginee.constraints.constants import Constants
from devopschatenginee.utils.list_chunker import ListChunker
from devopschatenginee.operations.kubernetes_action import KubernetesAction

class KubernetesManager:

    @staticmethod
    async def k8s_env_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        cluster_names = KubernetesAction.get_k8s_cluster_names()

        keyboard = []

        for cluster_name in cluster_names:
            keyboard.append([InlineKeyboardButton(text=f"🌐 {cluster_name}", callback_data=cluster_name)])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🌍 Let's choose your battlefield! Select the environment.", reply_markup=reply_markup
        )

        return Constants.K8S_ENV_CHOOSE

    @staticmethod
    async def k8s_env_choose_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        cluster_names = KubernetesAction.get_k8s_cluster_names()

        keyboard = []

        for cluster_name in cluster_names:
            keyboard.append([InlineKeyboardButton(text=f"🌐 {cluster_name}", callback_data=cluster_name)])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🔄 Oops! Misstep? No worries. Select the environment again!", reply_markup=reply_markup
        )

        return Constants.K8S_ENV_CHOOSE

    @staticmethod
    async def k8s_resource_type_define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        cluster_name = query.data
        context.user_data['KUBERNETES_CLUSTER_NAME'] = cluster_name
        await query.answer()

        text = f"""
        🌌 You're exploring the universe of:
        - Cluster name: {cluster_name}

        Now, choose a resource type to delve deeper.
        """

        # Create a list of rows to hold the buttons
        keyboard = []
        
        resource_type_chunks = list(ListChunker.chunks(lst=Constants.K8S_RESOURCE_TYPES, n=2))  # Create chunks of size 2
    
        for chunk in resource_type_chunks:
            keyboard.append([InlineKeyboardButton(text=f"🚀 {resource_type.capitalize()}", callback_data=resource_type) for resource_type in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_RESOURCETYPE_DEFINE

    @staticmethod
    async def k8s_resource_type_define_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        🔄 Oops, did you make a wrong turn?
        - Cluster name: {cluster_name}

        No worries! Select the resource type again.
        """

        # Create a list of rows to hold the buttons
        keyboard = []
        
        resource_type_chunks = list(ListChunker.chunks(lst=Constants.K8S_RESOURCE_TYPES, n=2))  # Create chunks of size 2
    
        for chunk in resource_type_chunks:
            keyboard.append([InlineKeyboardButton(text=f"🚀 {resource_type.capitalize()}", callback_data=resource_type) for resource_type in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_RESOURCETYPE_DEFINE

    @staticmethod
    async def k8s_node_define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        resource_type = query.data
        context.user_data['KUBERNETES_RESOURCE_TYPE'] = resource_type
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        🚀 Onwards, Adventurer! You're currently navigating:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        """

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")


        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status Nodes", callback_data=str(Constants.K8S_NODE_STATUS)),
                InlineKeyboardButton(text="📜 Describe nodes", callback_data=str(Constants.K8S_NODE_DESCRIBE)),
            ],
            [
                InlineKeyboardButton(text="🔄 Show Nodes Resource", callback_data=str(Constants.K8S_NODE_SHOW_RESOURCE)),
            ],

        ]

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NODE_DEFINE

    @staticmethod
    async def k8s_node_define_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        await query.answer()

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")

        text = f"""
        🔄 Not quite right? Let's reorient:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status Nodes", callback_data=str(Constants.K8S_NODE_STATUS)),
                InlineKeyboardButton(text="📜 Describe nodes", callback_data=str(Constants.K8S_NODE_DESCRIBE)),
            ],
            [
                InlineKeyboardButton(text="🔄 Show Nodes Resource", callback_data=str(Constants.K8S_NODE_SHOW_RESOURCE)),
            ],

        ]

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NODE_DEFINE
    

    @staticmethod
    async def k8s_node_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")

        command_result = KubernetesAction.get_k8s_nodes_status(cluster_name=cluster_name)
        
        # Convert the result into a string
        result_str = "\n        ".join(
            f"{item['node']} Role: {item['roles']} Status: {'Ready' if item['status'] == 'True' else 'NotReady'} Age: {item['age']} Version: {item['version']}"
            for item in command_result
        )

        text = f"""
        🚀 Getting status of nodes:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        ---------------------------------
        {result_str}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status Nodes", callback_data=str(Constants.K8S_NODE_STATUS)),
                InlineKeyboardButton(text="📜 Describe nodes", callback_data=str(Constants.K8S_NODE_DESCRIBE)),
            ],
            [
                InlineKeyboardButton(text="🔄 Show Nodes Resource", callback_data=str(Constants.K8S_NODE_SHOW_RESOURCE)),
            ],

        ]

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NODE_DEFINE

    @staticmethod
    async def k8s_node_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")

        text = f"""
        🚀 Getting list of nodes:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        """

        nodes =KubernetesAction.get_k8s_nodes(cluster_name=cluster_name)
        nodes_chunks = list(ListChunker.chunks(lst=nodes, n=2))  # Create chunks of size 2

        keyboard = []

        for chunk in nodes_chunks:
            keyboard.append([InlineKeyboardButton(text=f"🏷️ {node}", callback_data=node) for node in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NODE_LIST_DEFINE

    @staticmethod
    async def k8s_node_describe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        node = query.data
        context.user_data['KUBERNETES_NODE_NAME'] = node
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")

        command_result = KubernetesAction.describe_k8s_node(cluster_name=cluster_name, node_name=node)

        # Convert the result into a string
        result_str = (
            f"Name: {command_result['name']}\n"
            f"Labels: {command_result['labels']}\n"
            f"Annotations: {command_result['annotations']}\n"
            f"Capacity: {command_result['capacity']}\n"
            f"Allocatable: {command_result['allocatable']}\n"
            f"Addresses: {command_result['addresses']}\n"
            f"NodeInfo: {command_result['nodeInfo']}\n"
        )

        text = f"""
        🚀 Describe node details:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Node name: {node}
        ---------------------------------
        {result_str}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status Nodes", callback_data=str(Constants.K8S_NODE_STATUS)),
                InlineKeyboardButton(text="📜 Describe nodes", callback_data=str(Constants.K8S_NODE_DESCRIBE)),
            ],
            [
                InlineKeyboardButton(text="🔄 Show Nodes Resource", callback_data=str(Constants.K8S_NODE_SHOW_RESOURCE)),
            ],

        ]

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NODE_DEFINE

    @staticmethod
    async def k8s_node_show_resource(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        resource_type = context.user_data['KUBERNETES_RESOURCE_TYPE']
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")

        command_result = KubernetesAction.get_k8s_node_resources(cluster_name=cluster_name)
        # Retrieve total CPU and memory capacity for each node
        node_capacity = KubernetesAction.get_k8s_node_capacity(cluster_name=cluster_name)

        # Convert the result into a string
        result_str = "\n        ".join(
            f"{item['node']} CPU usage: {round(item['cpu_usage']*0.1 / node_capacity[item['node']]['cpu_capacity'], 2)}% Memory usage: {item['memory_usage']*100/node_capacity[item['node']]['memory_capacity']:.2f}%"
            for item in command_result
        )

        text = f"""
        🚀 Showing resource usage of nodes:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        ---------------------------------
        {result_str}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status Nodes", callback_data=str(Constants.K8S_NODE_STATUS)),
                InlineKeyboardButton(text="📜 Describe nodes", callback_data=str(Constants.K8S_NODE_DESCRIBE)),
            ],
            [
                InlineKeyboardButton(text="🔄 Show Resource", callback_data=str(Constants.K8S_NODE_SHOW_RESOURCE)),
            ],

        ]

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NODE_DEFINE

    @staticmethod
    async def k8s_namespace_define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        resource_type = query.data
        context.user_data['KUBERNETES_RESOURCE_TYPE'] = resource_type
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        🚀 Onwards, Adventurer! You're currently navigating:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        """

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")

        namespaces = KubernetesAction.get_k8s_namespaces(cluster_name=cluster_name)
        namespaces_chunks = list(ListChunker.chunks(lst=namespaces, n=2))  # Create chunks of size 2

        keyboard = []

        for chunk in namespaces_chunks:
            keyboard.append([InlineKeyboardButton(text=f"🏷️ {namespace}", callback_data=namespace) for namespace in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NAMESPACE_DEFINE
    
    @staticmethod
    async def k8s_namespace_define_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        await query.answer()

        if not cluster_name:
            # Handle case when no cluster_name was found in context
            print("No cluster name found")

        namespaces = KubernetesAction.get_k8s_namespaces(cluster_name=cluster_name)
        namespaces_chunks = list(ListChunker.chunks(lst=namespaces, n=2))  # Create chunks of size 2

        text = f"""
        🔄 Not quite right? Let's reorient:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        """

        keyboard = []

        for chunk in namespaces_chunks:
            keyboard.append([InlineKeyboardButton(text=f"🏷️ {namespace}", callback_data=namespace) for namespace in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_NAMESPACE_DEFINE

    @staticmethod
    async def k8s_resource_define(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        namespace = query.data
        context.user_data['KUBERNETES_NAMESPACE'] = namespace
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        You're doing great! Here are the details so far:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}

        Now, it's time to select a specific resource.
        """

        resource = KubernetesAction.get_k8s_resource(resource_type=resource_type, cluster_name=cluster_name, namespace=namespace)
        resource_chunks = list(ListChunker.chunks(lst=resource, n=2))  # Create chunks of size 2

        keyboard = []

        for chunk in resource_chunks:
            keyboard.append([InlineKeyboardButton(text=f"📦 {resource}", callback_data=resource) for resource in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_RESOURCE_DEFINE

    @staticmethod
    async def k8s_resource_define_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        Seems like you took a step back. Here's where we were:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}

        Feel free to choose a different resource.
        """

        resource = KubernetesAction.get_k8s_resource(resource_type=resource_type, cluster_name=cluster_name, namespace=namespace)
        resource_chunks = list(ListChunker.chunks(lst=resource, n=2))  # Create chunks of size 2

        keyboard = []

        for chunk in resource_chunks:
            keyboard.append([InlineKeyboardButton(text=f"📦 {resource}", callback_data=resource) for resource in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_RESOURCE_DEFINE

    @staticmethod
    async def k8s_operation_perform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""
        query = update.callback_query
        resource = query.data
        context.user_data['KUBERNETES_RESOURCE'] = resource
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        Alright, you've selected the resource! Here are the details:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}

        Now you can perform the following operations:
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status", callback_data=str(Constants.K8S_POD_STATUS_CHECK)),
                InlineKeyboardButton(text="📜 Log", callback_data=str(Constants.K8S_POD_LOG_VIEW)),
            ],
            [
                InlineKeyboardButton(text="🔄 Restart", callback_data=str(Constants.K8S_POD_RESTART)),
            ],

        ]

        if resource_type == "deployment":
            keyboard[1].insert(0, InlineKeyboardButton(text="↩️ Rollback", callback_data=str(Constants.K8S_POD_ROLLBACK_HISTORY)))

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_PERFORM

    @staticmethod
    async def k8s_operation_perform_restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Restart Kubernetes resource"""
        query = update.callback_query
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        command_result = KubernetesAction.restart_k8s_resource(resource_type=resource_type, namespace=namespace, resource_name=resource, cluster_name=cluster_name)

        text = f"""
        👌 You've just restarted the resource:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        ---------------------------------
        {command_result}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status", callback_data=str(Constants.K8S_POD_STATUS_CHECK)),
                InlineKeyboardButton(text="📜 Log", callback_data=str(Constants.K8S_POD_LOG_VIEW)),
            ],
            [
                InlineKeyboardButton(text="🔄 Restart", callback_data=str(Constants.K8S_POD_RESTART)),
            ],

        ]

        if resource_type == "deployment":
            keyboard[1].insert(0, InlineKeyboardButton(text="↩️ Rollback", callback_data=str(Constants.K8S_POD_ROLLBACK_HISTORY)))

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_PERFORM

    @staticmethod
    async def k8s_operation_perform_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show status of Kubernetes resource"""
        query = update.callback_query
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        command_result = KubernetesAction.get_k8s_resource_status(resource_type=resource_type, namespace=namespace, resource_name=resource, cluster_name=cluster_name)
        command_result_text = "\n    ".join(command_result)

        text = f"""
        👀 Here's the status of your resource:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        --------------------------------
        {command_result_text}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status", callback_data=str(Constants.K8S_POD_STATUS_CHECK)),
                InlineKeyboardButton(text="📜 Log", callback_data=str(Constants.K8S_POD_LOG_VIEW)),
            ],
            [
                InlineKeyboardButton(text="🔄 Restart", callback_data=str(Constants.K8S_POD_RESTART)),
            ],

        ]

        if resource_type == "deployment":
            keyboard[1].insert(0, InlineKeyboardButton(text="↩️ Rollback", callback_data=str(Constants.K8S_POD_ROLLBACK_HISTORY)))

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_PERFORM

    @staticmethod
    async def k8s_operation_perform_rollback_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show revision history of Kubernetes resource"""
        query = update.callback_query
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        revisions = KubernetesAction.get_k8s_all_rollback_revisions(resource_type=resource_type, namespace=namespace, resource_name=resource, cluster_name=cluster_name)
        revisions_chunks = list(ListChunker.chunks(lst=revisions, n=2))  # Create chunks of size 2

        text = f"""
        🔄 Rollback Revisions:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        """

        keyboard = []

        for chunk in revisions_chunks:
            keyboard.append([InlineKeyboardButton(text=f"🔙 Revision: {revision}", callback_data=revision) for revision in chunk])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_HISTORY

    @staticmethod
    async def k8s_operation_perform_rollback_history_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Return to Kubernetes operation options"""
        query = update.callback_query
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        Operations on your resource:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status", callback_data=str(Constants.K8S_POD_STATUS_CHECK)),
                InlineKeyboardButton(text="📜 Log", callback_data=str(Constants.K8S_POD_LOG_VIEW)),
            ],
            [
                InlineKeyboardButton(text="🔄 Restart", callback_data=str(Constants.K8S_POD_RESTART)),
            ],

        ]

        if resource_type == "deployment":
            keyboard[1].insert(0, InlineKeyboardButton(text="↩️ Rollback", callback_data=str(Constants.K8S_POD_ROLLBACK_HISTORY)))

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_PERFORM

    @staticmethod
    async def k8s_operation_perform_rollback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Perform a rollback to a specific revision"""
        query = update.callback_query
        revision = query.data
        context.user_data['KUBERNETES_RESOURCE_REVISION'] = revision
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()
        command_result = KubernetesAction.rollback_k8s_resource_to_revision(resource_type=resource_type, namespace=namespace, resource_name=resource, cluster_name=cluster_name, revision_number=int(revision))

        text = f"""
        🔄 Rollback Results:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        - Revision: {revision}
        -------
        {command_result}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status", callback_data=str(Constants.K8S_POD_STATUS_CHECK)),
                InlineKeyboardButton(text="📜 Log", callback_data=str(Constants.K8S_POD_LOG_VIEW)),
            ],
            [
                InlineKeyboardButton(text="🔄 Restart", callback_data=str(Constants.K8S_POD_RESTART)),
            ],

        ]

        if resource_type == "deployment":
            keyboard[1].insert(0, InlineKeyboardButton(text="↩️ Rollback", callback_data=str(Constants.K8S_POD_ROLLBACK_HISTORY)))

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_PERFORM

    @staticmethod
    async def k8s_operation_perform_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show logs of Kubernetes resource"""
        query = update.callback_query
        pod_name = query.data
        context.user_data['KUBERNETES_POD_NAME'] = pod_name
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        command_result = KubernetesAction.get_k8s_pod_logs(resource_type=resource_type, namespace=namespace, resource_name=resource, cluster_name=cluster_name, pod_name=pod_name)

        text = f"""
        📚 Logs for your resource:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        - Pod name: {pod_name}
        --------------------------------
        {command_result}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status", callback_data=str(Constants.K8S_POD_STATUS_CHECK)),
                InlineKeyboardButton(text="📜 Log", callback_data=str(Constants.K8S_POD_LOG_VIEW)),
            ],
            [
                InlineKeyboardButton(text="🔄 Restart", callback_data=str(Constants.K8S_POD_RESTART)),
            ],

        ]

        if resource_type == "deployment":
            keyboard[1].insert(0, InlineKeyboardButton(text="↩️ Rollback", callback_data=str(Constants.K8S_POD_ROLLBACK_HISTORY)))

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_PERFORM

    @staticmethod
    async def k8s_operation_perform_pod_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show pods of Kubernetes resource"""
        query = update.callback_query
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        pod_names = KubernetesAction.get_k8s_pod_names_for_resource(resource_type=resource_type, namespace=namespace, resource_name=resource, cluster_name=cluster_name)

        text = f"""
        🔄 Pods:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        """

        keyboard = []

        for pod_name in pod_names:
            keyboard.append([InlineKeyboardButton(text=f"📜 {pod_name}", callback_data=pod_name)])

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_LOG

    @staticmethod
    async def k8s_operation_perform_pod_log_return_prev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show pods of Kubernetes resource"""
        query = update.callback_query
        resource      = context.user_data.get('KUBERNETES_RESOURCE')
        resource_type = context.user_data.get('KUBERNETES_RESOURCE_TYPE')
        namespace     = context.user_data.get('KUBERNETES_NAMESPACE')
        cluster_name  = context.user_data.get('KUBERNETES_CLUSTER_NAME')
        await query.answer()

        text = f"""
        🔄 Pods:
        - Cluster name: {cluster_name}
        - Resource type: {resource_type}
        - Namespace: {namespace}
        - Resource: {resource}
        """

        keyboard = [
            [
                InlineKeyboardButton(text="🔍 Status", callback_data=str(Constants.K8S_POD_STATUS_CHECK)),
                InlineKeyboardButton(text="📜 Log", callback_data=str(Constants.K8S_POD_LOG_VIEW)),
            ],
            [
                InlineKeyboardButton(text="🔄 Restart", callback_data=str(Constants.K8S_POD_RESTART)),
            ],

        ]

        if resource_type == "deployment":
            keyboard[1].insert(0, InlineKeyboardButton(text="↩️ Rollback", callback_data=str(Constants.K8S_POD_ROLLBACK_HISTORY)))

        keyboard.append(
            [
                InlineKeyboardButton(text="🚪 Home", callback_data=str(Constants.RETURN_START)),
                InlineKeyboardButton(text="🔙 Back", callback_data=str(Constants.RETURN_PREV))
            ]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text, reply_markup=reply_markup
        )

        return Constants.K8S_OPERATION_PERFORM
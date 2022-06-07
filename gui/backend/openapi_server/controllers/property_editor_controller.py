import connexion
import six

from openapi_server.models.instance_module import InstanceModule  # noqa: E501
from openapi_server.models.instance_queue import InstanceQueue  # noqa: E501
from openapi_server.models.module_param import ModuleParam  # noqa: E501
from openapi_server.models.queue_param import QueueParam  # noqa: E501
from openapi_server import util

import sys
from . import worker

# x = worker.x

def clean_queue(project_id, instance_id):  # noqa: E501
    """Cleans queue

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Instance
    :type instance_id: str

    :rtype: int
    """
    return 'do some magic!'


def get_instance_module(project_id, instance_id, instance_module_id):  # noqa: E501
    """Get list of instance modules

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Instance
    :type instance_id: str
    :param instance_module_id: ID of Instance
    :type instance_module_id: str

    :rtype: InstanceModule
    """
    return 'do some magic!'


def get_instance_queue(project_id, instance_id):  # noqa: E501
    """Get list of instance queues

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Instance
    :type instance_id: str

    :rtype: InstanceQueue
    """
    return 'do some magic!'


def get_queue_current_image(project_id, instance_id):  # noqa: E501
    """Get list of instance queues

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Instance
    :type instance_id: str

    :rtype: int
    """
    return 'do some magic!'


def list_module_params(project_id, module_id):  # noqa: E501
    """Get list of module params

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module_id: ID of Module
    :type module_id: str

    :rtype: List[ModuleParam]
    """
    
    return worker.x.get_project_module_data(project_id.lower(), module_id)


def list_queue_params(project_id, queue_id):  # noqa: E501
    """Get list of queue params

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param queue_id: ID of Queue
    :type queue_id: str

    :rtype: List[QueueParam]
    """
    return worker.x.get_project_queue_params(project_id, queue_id)


def reset_instance_module(project_id, instance_id, instance_module_id):  # noqa: E501
    """Reset instance module

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Instance
    :type instance_id: str
    :param instance_module_id: ID of Instance
    :type instance_module_id: str

    :rtype: InstanceModule
    """
    return 'do some magic!'


def update_module_param(project_id, module_id, module_param=None):  # noqa: E501
    """Updates module param

     # noqa: E501

    :param project_id: ID of Project that needs to be updated
    :type project_id: str
    :param module_id: ID of Module
    :type module_id: str
    :param module_param: 
    :type module_param: dict | bytes

    :rtype: ModuleParam
    """
    if connexion.request.is_json:
        # module_param = ModuleParam.from_dict(connexion.request.get_json())  # noqa: E501
        module_param = connexion.request.get_json()
    # return 'do some magic!'
    return worker.x.set_module_params(project_id, module_id, module_param)


def update_queue_param(project_id, queue_id, queue_param=None):  # noqa: E501
    """Updates queue param

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param queue_id: ID of Queue
    :type queue_id: str
    :param queue_param: 
    :type queue_param: dict | bytes

    :rtype: QueueParam
    """
    if connexion.request.is_json:
        queue_param = QueueParam.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

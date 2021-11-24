import connexion
import six
import json

from openapi_server.models.instance import Instance  # noqa: E501
from openapi_server.models.instance_module import InstanceModule  # noqa: E501
from openapi_server.models.instance_queue import InstanceQueue  # noqa: E501
from openapi_server.models.module import Module  # noqa: E501
from openapi_server.models.module_def import ModuleDef  # noqa: E501
from openapi_server.models.project_resource import ProjectResource  # noqa: E501
from openapi_server.models.queue import Queue  # noqa: E501
from openapi_server import util

import sys
from . import worker

x = worker.x

def add_instance(project_id):  # noqa: E501
    """Add instance to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    # return x.add_project_instance(project_id, instance_id)
    return x.add_project_instance(project_id)


def add_module(project_id, module):  # noqa: E501
    """Add module to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module: 
    :type module: dict | bytes

    :rtype: Module
    """
    # if connexion.request.is_json:
    #     module = Module.from_dict(connexion.request.get_json())  # noqa: E501
    # return 'do some magic!'
    # return x.add_project_module(project_id, "TODO nazwa modułu")
    return x.add_project_module(project_id, module)


def add_queue(project_id, queue):  # noqa: E501
    """Add queue to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param queue: 
    :type queue: dict | bytes

    :rtype: Queue
    """
    if connexion.request.is_json:
        queue = Queue.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_resource(project_id):  # noqa: E501
    """Add resource to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: ProjectResource
    """
    return 'do some magic!'


def delete_module(project_id, module_id):  # noqa: E501
    """Delete module from project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module_id: ID of Module
    :type module_id: str

    :rtype: None
    """
    return x.delete_project_module(project_id, module_id)


def delete_queue(project_id, module_id):  # noqa: E501
    """Delete queue from project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module_id: ID of Module
    :type module_id: str

    :rtype: None
    """
    return 'do some magic!'


def delete_resource(project_id, resource_id):  # noqa: E501
    """Delete resource from project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param resource_id: ID of Module
    :type resource_id: str

    :rtype: None
    """
    return 'do some magic!'


def get_instance(project_id, instance_id):  # noqa: E501
    """Get specified of project instance

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Module
    :type instance_id: str

    :rtype: Instance
    """
    # return 'do some magic!'
    return x.get_instance(project_id, instance_id)


def get_module(project_id, module_id):  # noqa: E501
    """Get specified project module

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module_id: ID of Module
    :type module_id: str

    :rtype: Module
    """
    return x.get_project_module_data(project_id, module_id)


def get_queue(project_id, module_id):  # noqa: E501
    """Get specified of project queue

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module_id: ID of Module
    :type module_id: str

    :rtype: Queue
    """
    return 'do some magic!'


def get_resource(project_id, resource_id):  # noqa: E501
    """Get specified of project resource

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param resource_id: ID of Module
    :type resource_id: str

    :rtype: ProjectResource
    """
    return 'do some magic!'


def kill_instance(project_id, instance_id):  # noqa: E501
    """Delete instance from project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Module
    :type instance_id: str

    :rtype: None
    """
    return x.delete_project_instance(project_id, instance_id)


def list_instance_modules(project_id, instance_id):  # noqa: E501
    """Get specified project instance

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Instance
    :type instance_id: str

    :rtype: List[InstanceModule]
    """
    return 'do some magic!'


def list_instance_queues(project_id, instance_id):  # noqa: E501
    """Get specified project instance

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param instance_id: ID of Instance
    :type instance_id: str

    :rtype: List[InstanceQueue]
    """
    return 'do some magic!'


def list_instances(project_id):  # noqa: E501
    """Get list of project instances

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: List[Instance]
    """
    return x.get_project_instances(project_id)


def list_module_def():  # noqa: E501
    """Get list of module definitions

     # noqa: E501


    :rtype: List[ModuleDef]
    """
    return x.get_modules()


def list_modules(project_id):  # noqa: E501
    """Get list of project modules

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: List[Module]
    """
    return x.get_project_modules(project_id)


def list_queues(project_id):  # noqa: E501
    """Get list of project queues

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: List[Queue]
    """
    return 'do some magic!'


def list_resources(project_id):  # noqa: E501
    """Get list of project resources

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: List[ProjectResource]
    """
    return x.get_project_resources(project_id)
    # return x.get_project_conf(project_id)


def run_instance(project_id):  # noqa: E501
    """Update instance to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    return 'do some magic!'


def update_module(project_id, module):  # noqa: E501
    """Add module to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module: 
    :type module: dict | bytes

    :rtype: Module
    """
    # if connexion.request.is_json:
    #     module = Module.from_dict(connexion.request.get_json())  # noqa: E501
    # return 'do some magic!'
    return x.set_project_conf(project_id, module) # TODO data?!?!?!??!?!!??!??!


def update_queue(project_id, queue):  # noqa: E501
    """Update queue to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param queue: 
    :type queue: dict | bytes

    :rtype: Queue
    """
    if connexion.request.is_json:
        queue = Queue.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_resource(project_id):  # noqa: E501
    """Update resource to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    return 'do some magic!'

import connexion
import six

from openapi_server.models.instance import Instance  # noqa: E501
from openapi_server.models.instance_module import InstanceModule  # noqa: E501
from openapi_server.models.instance_queue import InstanceQueue  # noqa: E501
from openapi_server.models.module import Module  # noqa: E501
from openapi_server.models.module_def import ModuleDef  # noqa: E501
from openapi_server.models.project_resource import ProjectResource  # noqa: E501
from openapi_server.models.queue import Queue  # noqa: E501
from openapi_server import util


def add_instance(project_id):  # noqa: E501
    """Add instance to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    return 'do some magic!'


def add_module(project_id):  # noqa: E501
    """Add module to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    return 'do some magic!'


def add_queue(project_id):  # noqa: E501
    """Add queue to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
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
    return 'do some magic!'


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
    return 'do some magic!'


def get_module(project_id, module_id):  # noqa: E501
    """Get specified project module

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str
    :param module_id: ID of Module
    :type module_id: str

    :rtype: Module
    """
    return 'do some magic!'


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
    return 'do some magic!'


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
    return 'do some magic!'


def list_module_def():  # noqa: E501
    """Get list of module definitions

     # noqa: E501


    :rtype: List[ModuleDef]
    """
    return 'do some magic!'


def list_modules(project_id):  # noqa: E501
    """Get list of project modules

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: List[Module]
    """
    return 'do some magic!'


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
    return 'do some magic!'


def run_instance(project_id):  # noqa: E501
    """Update instance to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    return 'do some magic!'


def update_queue(project_id):  # noqa: E501
    """Update queue to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    return 'do some magic!'


def update_resource(project_id):  # noqa: E501
    """Update resource to project

     # noqa: E501

    :param project_id: ID of Project
    :type project_id: str

    :rtype: Module
    """
    return 'do some magic!'

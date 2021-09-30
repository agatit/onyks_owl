import connexion
import six

from openapi_server.models.project import Project  # noqa: E501
from openapi_server import util


def add_project(project=None):  # noqa: E501
    """Adding new project

     # noqa: E501

    :param project: 
    :type project: dict | bytes

    :rtype: Project
    """
    if connexion.request.is_json:
        project = Project.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_project(project_id):  # noqa: E501
    """Deletes a Project

     # noqa: E501

    :param project_id: Project id to delete
    :type project_id: str

    :rtype: None
    """
    return 'do some magic!'


def get_project(project_id):  # noqa: E501
    """Find Project by ID

    Returns a single project # noqa: E501

    :param project_id: ID of project to return
    :type project_id: str

    :rtype: Project
    """
    return 'do some magic!'


def list_projects():  # noqa: E501
    """Get list of projects

     # noqa: E501


    :rtype: List[Project]
    """
    return 'do some magic!'


def update_project(project_id, project=None):  # noqa: E501
    """Updates a Project

     # noqa: E501

    :param project_id: ID of Project that needs to be updated
    :type project_id: str
    :param project: 
    :type project: dict | bytes

    :rtype: Project
    """
    if connexion.request.is_json:
        project = Project.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

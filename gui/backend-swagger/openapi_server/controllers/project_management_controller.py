import connexion
import six

from openapi_server.models.project import Project  # noqa: E501
from openapi_server import util

from pathlib import Path
import json

project_path = "../../examples"

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

    response = []
    pathlist = list(Path(project_path).glob(f'**/{project_id}/config.json'))
    if len(pathlist) != 1:
        return connexion.NoContent, 404
    else:
        with open(pathlist[0], "rb") as f:
            config = json.load(f)
        prj = Project(pathlist[0].parent.name, config.get("desc", "no description"))
        return prj


def list_projects():  # noqa: E501
    """Get list of projects

     # noqa: E501


    :rtype: List[Project]
    """

    response = []
    pathlist = Path(project_path).glob('**/*/config.json')
    for path in pathlist:
        print(path.parent.name)
        with open(path, "rb") as f:
            config = json.load(f)
        prj = Project(path.parent.name, config.get("desc", "no description"))
        response.append(prj)

    return response


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

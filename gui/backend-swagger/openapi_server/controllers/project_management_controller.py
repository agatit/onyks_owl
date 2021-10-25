import connexion
from connexion.exceptions import ProblemException
import six

from openapi_server.models.project import Project  # noqa: E501
from openapi_server import util

from pathlib import Path
import json
import slugify
import os
import shutil

project_path = "../../examples"

import sys
sys.path.append('../backend')

from engine import Engine
x = Engine()


def add_project(project=None):  # noqa: E501
    """Adding new project

     # noqa: E501

    :param project: 
    :type project: dict | bytes

    :rtype: Project
    """

    try:
        if connexion.request.is_json:
            project = Project.from_dict(connexion.request.get_json())  # noqa: E501
            project.id = slugify.slugify(project.id, lowercase=True, separator="_")
        
            if os.path.exists(os.path.join(project_path, project.id, "config.json")):
                raise FileExistsError

            if not os.path.exists(os.path.join(project_path, project.id)):  
                os.mkdir(os.path.join(project_path, project.id))

            config = {}
            config['name'] = project.name
            config['desc'] = project.description
            with open(os.path.join(project_path, project.id, "config.json"), 'w') as f:
                json.dump(config, f)
        else:
            raise ProblemException(405, "Invalid input")
      
    except FileExistsError as e:
        raise ProblemException(409, "Project exists")  

    return project


def delete_project(project_id):  # noqa: E501
    """Deletes a Project

     # noqa: E501

    :param project_id: Project id to delete
    :type project_id: str

    :rtype: None
    """
    try:
        if not os.path.exists(os.path.join(project_path, project_id, "config.json")):
            raise FileNotFoundError

        shutil.rmtree(os.path.join(project_path, project_id))

    except FileNotFoundError as e:
        raise ProblemException(404, "Project not exists", str(e))

    return 'Deleted', 200


def get_project(project_id):  # noqa: E501
    """Find Project by ID

    Returns a single project # noqa: E501

    :param project_id: ID of project to return
    :type project_id: str

    :rtype: Project
    """
    try:
        response = []
        pathlist = list(Path(project_path).glob(f'**/{project_id}/config.json'))
        if len(pathlist) != 1:
            raise FileNotFoundError
        else:
            with open(pathlist[0], "rb") as f:
                config = json.load(f)
            prj = Project(pathlist[0].parent.name, config.get("name", pathlist[0].parent.name), config.get("desc", "no description"))
            return prj
    except FileNotFoundError as e:
        raise ProblemException(404, "Project not exists", str(e))
        
    return 'Deleted', 200            
    # TODO na pewno nie "config"
    # return x.get_project_conf(project_id)

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
        prj = Project(path.parent.name, config.get("name", path.parent.name), config.get("desc", "no description"))
        response.append(prj)

    return response
    return x.get_projects()

def update_project(project=None):  # noqa: E501
    """Updates a Project

     # noqa: E501

    :param project_id: ID of Project that needs to be updated
    :type project_id: str
    :param project: 
    :type project: dict | bytes

    :rtype: Project
    """
    try:
        if connexion.request.is_json:
            project = Project.from_dict(connexion.request.get_json())  # noqa: E501
        
            with open(os.path.join(project_path, project.id, "config.json"), 'r') as f:
                config = json.load(f)
           
            config['name'] = project.name
            config['desc'] = project.description
            with open(os.path.join(project_path, project.id, "config.json"), 'w') as f:
                json.dump(config, f)
        else:
            return connexion.NoContent, 400    
    except FileNotFoundError as e:
        raise ProblemException(404, "Project not exists", str(e))

    return project

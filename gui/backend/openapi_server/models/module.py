# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.module_def import ModuleDef
from openapi_server.models.project import Project
from openapi_server.models.queue import Queue
from openapi_server import util

from openapi_server.models.module_def import ModuleDef  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server.models.queue import Queue  # noqa: E501

class Module(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, module_def=None, project=None, input=None, output=None, name=None, comment=None):  # noqa: E501
        """Module - a model defined in OpenAPI

        :param id: The id of this Module.  # noqa: E501
        :type id: str
        :param module_def: The module_def of this Module.  # noqa: E501
        :type module_def: ModuleDef
        :param project: The project of this Module.  # noqa: E501
        :type project: Project
        :param input: The input of this Module.  # noqa: E501
        :type input: Queue
        :param output: The output of this Module.  # noqa: E501
        :type output: Queue
        :param name: The name of this Module.  # noqa: E501
        :type name: str
        :param comment: The comment of this Module.  # noqa: E501
        :type comment: str
        """
        self.openapi_types = {
            'id': str,
            'module_def': ModuleDef,
            'project': Project,
            'input': Queue,
            'output': Queue,
            'name': str,
            'comment': str
        }

        self.attribute_map = {
            'id': 'id',
            'module_def': 'module_def',
            'project': 'project',
            'input': 'input',
            'output': 'output',
            'name': 'name',
            'comment': 'comment'
        }

        self._id = id
        self._module_def = module_def
        self._project = project
        self._input = input
        self._output = output
        self._name = name
        self._comment = comment

    @classmethod
    def from_dict(cls, dikt) -> 'Module':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Module of this Module.  # noqa: E501
        :rtype: Module
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Module.


        :return: The id of this Module.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Module.


        :param id: The id of this Module.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def module_def(self):
        """Gets the module_def of this Module.


        :return: The module_def of this Module.
        :rtype: ModuleDef
        """
        return self._module_def

    @module_def.setter
    def module_def(self, module_def):
        """Sets the module_def of this Module.


        :param module_def: The module_def of this Module.
        :type module_def: ModuleDef
        """

        self._module_def = module_def

    @property
    def project(self):
        """Gets the project of this Module.


        :return: The project of this Module.
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this Module.


        :param project: The project of this Module.
        :type project: Project
        """

        self._project = project

    @property
    def input(self):
        """Gets the input of this Module.


        :return: The input of this Module.
        :rtype: Queue
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this Module.


        :param input: The input of this Module.
        :type input: Queue
        """

        self._input = input

    @property
    def output(self):
        """Gets the output of this Module.


        :return: The output of this Module.
        :rtype: Queue
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this Module.


        :param output: The output of this Module.
        :type output: Queue
        """

        self._output = output

    @property
    def name(self):
        """Gets the name of this Module.


        :return: The name of this Module.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Module.


        :param name: The name of this Module.
        :type name: str
        """

        self._name = name

    @property
    def comment(self):
        """Gets the comment of this Module.


        :return: The comment of this Module.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this Module.


        :param comment: The comment of this Module.
        :type comment: str
        """

        self._comment = comment
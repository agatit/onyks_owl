# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.project import Project
from openapi_server import util

from openapi_server.models.project import Project  # noqa: E501

class Queue(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, project=None, name=None, task_queue_limit=None, stream_queue_limit=None, task_queue_timeout=None, stream_queue_timeout=None):  # noqa: E501
        """Queue - a model defined in OpenAPI

        :param project: The project of this Queue.  # noqa: E501
        :type project: Project
        :param name: The name of this Queue.  # noqa: E501
        :type name: str
        :param task_queue_limit: The task_queue_limit of this Queue.  # noqa: E501
        :type task_queue_limit: int
        :param stream_queue_limit: The stream_queue_limit of this Queue.  # noqa: E501
        :type stream_queue_limit: int
        :param task_queue_timeout: The task_queue_timeout of this Queue.  # noqa: E501
        :type task_queue_timeout: int
        :param stream_queue_timeout: The stream_queue_timeout of this Queue.  # noqa: E501
        :type stream_queue_timeout: int
        """
        self.openapi_types = {
            'project': Project,
            'name': str,
            'task_queue_limit': int,
            'stream_queue_limit': int,
            'task_queue_timeout': int,
            'stream_queue_timeout': int
        }

        self.attribute_map = {
            'project': 'project',
            'name': 'name',
            'task_queue_limit': 'task_queue_limit',
            'stream_queue_limit': 'stream_queue_limit',
            'task_queue_timeout': 'task_queue_timeout',
            'stream_queue_timeout': 'stream_queue_timeout'
        }

        self._project = project
        self._name = name
        self._task_queue_limit = task_queue_limit
        self._stream_queue_limit = stream_queue_limit
        self._task_queue_timeout = task_queue_timeout
        self._stream_queue_timeout = stream_queue_timeout

    @classmethod
    def from_dict(cls, dikt) -> 'Queue':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Queue of this Queue.  # noqa: E501
        :rtype: Queue
        """
        return util.deserialize_model(dikt, cls)

    @property
    def project(self):
        """Gets the project of this Queue.


        :return: The project of this Queue.
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this Queue.


        :param project: The project of this Queue.
        :type project: Project
        """

        self._project = project

    @property
    def name(self):
        """Gets the name of this Queue.


        :return: The name of this Queue.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Queue.


        :param name: The name of this Queue.
        :type name: str
        """

        self._name = name

    @property
    def task_queue_limit(self):
        """Gets the task_queue_limit of this Queue.


        :return: The task_queue_limit of this Queue.
        :rtype: int
        """
        return self._task_queue_limit

    @task_queue_limit.setter
    def task_queue_limit(self, task_queue_limit):
        """Sets the task_queue_limit of this Queue.


        :param task_queue_limit: The task_queue_limit of this Queue.
        :type task_queue_limit: int
        """

        self._task_queue_limit = task_queue_limit

    @property
    def stream_queue_limit(self):
        """Gets the stream_queue_limit of this Queue.


        :return: The stream_queue_limit of this Queue.
        :rtype: int
        """
        return self._stream_queue_limit

    @stream_queue_limit.setter
    def stream_queue_limit(self, stream_queue_limit):
        """Sets the stream_queue_limit of this Queue.


        :param stream_queue_limit: The stream_queue_limit of this Queue.
        :type stream_queue_limit: int
        """

        self._stream_queue_limit = stream_queue_limit

    @property
    def task_queue_timeout(self):
        """Gets the task_queue_timeout of this Queue.


        :return: The task_queue_timeout of this Queue.
        :rtype: int
        """
        return self._task_queue_timeout

    @task_queue_timeout.setter
    def task_queue_timeout(self, task_queue_timeout):
        """Sets the task_queue_timeout of this Queue.


        :param task_queue_timeout: The task_queue_timeout of this Queue.
        :type task_queue_timeout: int
        """

        self._task_queue_timeout = task_queue_timeout

    @property
    def stream_queue_timeout(self):
        """Gets the stream_queue_timeout of this Queue.


        :return: The stream_queue_timeout of this Queue.
        :rtype: int
        """
        return self._stream_queue_timeout

    @stream_queue_timeout.setter
    def stream_queue_timeout(self, stream_queue_timeout):
        """Sets the stream_queue_timeout of this Queue.


        :param stream_queue_timeout: The stream_queue_timeout of this Queue.
        :type stream_queue_timeout: int
        """

        self._stream_queue_timeout = stream_queue_timeout

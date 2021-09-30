# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class QueueParamDef(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, description=None, type=None):  # noqa: E501
        """QueueParamDef - a model defined in OpenAPI

        :param id: The id of this QueueParamDef.  # noqa: E501
        :type id: str
        :param description: The description of this QueueParamDef.  # noqa: E501
        :type description: str
        :param type: The type of this QueueParamDef.  # noqa: E501
        :type type: str
        """
        self.openapi_types = {
            'id': str,
            'description': str,
            'type': str
        }

        self.attribute_map = {
            'id': 'id',
            'description': 'description',
            'type': 'type'
        }

        self._id = id
        self._description = description
        self._type = type

    @classmethod
    def from_dict(cls, dikt) -> 'QueueParamDef':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The QueueParamDef of this QueueParamDef.  # noqa: E501
        :rtype: QueueParamDef
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this QueueParamDef.


        :return: The id of this QueueParamDef.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this QueueParamDef.


        :param id: The id of this QueueParamDef.
        :type id: str
        """

        self._id = id

    @property
    def description(self):
        """Gets the description of this QueueParamDef.


        :return: The description of this QueueParamDef.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this QueueParamDef.


        :param description: The description of this QueueParamDef.
        :type description: str
        """

        self._description = description

    @property
    def type(self):
        """Gets the type of this QueueParamDef.

        TODO: Każdy typ powinien mieć dedykowany edytor w property managerze  # noqa: E501

        :return: The type of this QueueParamDef.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this QueueParamDef.

        TODO: Każdy typ powinien mieć dedykowany edytor w property managerze  # noqa: E501

        :param type: The type of this QueueParamDef.
        :type type: str
        """
        allowed_values = ["string", "float", "integer", "quad", "region", "region_list", "resource"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type
# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.instance_module import InstanceModule  # noqa: E501
from openapi_server.models.instance_queue import InstanceQueue  # noqa: E501
from openapi_server.models.module_param import ModuleParam  # noqa: E501
from openapi_server.models.queue_param import QueueParam  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPropertyEditorController(BaseTestCase):
    """PropertyEditorController integration test stubs"""

    def test_clean_queue(self):
        """Test case for clean_queue

        Cleans queue
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})/queue(instanceQueueId)/clean'.format(project_id='project_id_example', instance_id='instance_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_instance_module(self):
        """Test case for get_instance_module

        Get list of instance modules
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})/module({instanceModuleId})'.format(project_id='project_id_example', instance_id='instance_id_example', instance_module_id='instance_module_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_instance_queue(self):
        """Test case for get_instance_queue

        Get list of instance queues
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})/queue(instanceQueueId)'.format(project_id='project_id_example', instance_id='instance_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_queue_current_image(self):
        """Test case for get_queue_current_image

        Get list of instance queues
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})/queue(instanceQueueId)/current_image'.format(project_id='project_id_example', instance_id='instance_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_module_params(self):
        """Test case for list_module_params

        Get list of module params
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/module({moduleId})/param'.format(project_id='project_id_example', module_id='module_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_queue_params(self):
        """Test case for list_queue_params

        Get list of queue params
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/queue({queueId})/param'.format(project_id='project_id_example', queue_id='queue_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reset_instance_module(self):
        """Test case for reset_instance_module

        Reset instance module
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})/module({instanceModuleId})/reset'.format(project_id='project_id_example', instance_id='instance_id_example', instance_module_id='instance_module_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("*/* not supported by Connexion. Use application/json instead. See https://github.com/zalando/connexion/pull/760")
    def test_update_module_param(self):
        """Test case for update_module_param

        Updates module param
        """
        module_param = openapi_server.ModuleParam()
        headers = { 
            'Accept': '*/*',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/module({moduleId})/param'.format(project_id='project_id_example', module_id='module_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(module_param),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("*/* not supported by Connexion. Use application/json instead. See https://github.com/zalando/connexion/pull/760")
    def test_update_queue_param(self):
        """Test case for update_queue_param

        Updates queue param
        """
        queue_param = openapi_server.QueueParam()
        headers = { 
            'Accept': '*/*',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/queue({queueId})/param'.format(project_id='project_id_example', queue_id='queue_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(queue_param),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

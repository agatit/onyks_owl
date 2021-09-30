# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.instance import Instance  # noqa: E501
from openapi_server.models.instance_module import InstanceModule  # noqa: E501
from openapi_server.models.instance_queue import InstanceQueue  # noqa: E501
from openapi_server.models.module import Module  # noqa: E501
from openapi_server.models.module_def import ModuleDef  # noqa: E501
from openapi_server.models.project_resource import ProjectResource  # noqa: E501
from openapi_server.models.queue import Queue  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProjectEditorController(BaseTestCase):
    """ProjectEditorController integration test stubs"""

    def test_add_instance(self):
        """Test case for add_instance

        Add instance to project
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance'.format(project_id='project_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_module(self):
        """Test case for add_module

        Add module to project
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/module'.format(project_id='project_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_queue(self):
        """Test case for add_queue

        Add queue to project
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/queue'.format(project_id='project_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_resource(self):
        """Test case for add_resource

        Add resource to project
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/resource'.format(project_id='project_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_module(self):
        """Test case for delete_module

        Delete module from project
        """
        headers = { 
        }
        response = self.client.open(
            '/owlapi/project({projectId})/module({moduleId})'.format(project_id='project_id_example', module_id='module_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_queue(self):
        """Test case for delete_queue

        Delete queue from project
        """
        headers = { 
        }
        response = self.client.open(
            '/owlapi/project({projectId})/queue({moduleId})'.format(project_id='project_id_example', module_id='module_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_resource(self):
        """Test case for delete_resource

        Delete resource from project
        """
        headers = { 
        }
        response = self.client.open(
            '/owlapi/project({projectId})/resource({resourceId})'.format(project_id='project_id_example', resource_id='resource_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_instance(self):
        """Test case for get_instance

        Get specified of project instance
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})'.format(project_id='project_id_example', instance_id='instance_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_module(self):
        """Test case for get_module

        Get specified project module
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/module({moduleId})'.format(project_id='project_id_example', module_id='module_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_queue(self):
        """Test case for get_queue

        Get specified of project queue
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/queue({moduleId})'.format(project_id='project_id_example', module_id='module_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_resource(self):
        """Test case for get_resource

        Get specified of project resource
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/resource({resourceId})'.format(project_id='project_id_example', resource_id='resource_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_kill_instance(self):
        """Test case for kill_instance

        Delete instance from project
        """
        headers = { 
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})'.format(project_id='project_id_example', instance_id='instance_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_instance_modules(self):
        """Test case for list_instance_modules

        Get specified project instance
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})/module'.format(project_id='project_id_example', instance_id='instance_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_instance_queues(self):
        """Test case for list_instance_queues

        Get specified project instance
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance({instanceId})/queue'.format(project_id='project_id_example', instance_id='instance_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_instances(self):
        """Test case for list_instances

        Get list of project instances
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance'.format(project_id='project_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_module_def(self):
        """Test case for list_module_def

        Get list of module definitions
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/module_def',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_modules(self):
        """Test case for list_modules

        Get list of project modules
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/module'.format(project_id='project_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_queues(self):
        """Test case for list_queues

        Get list of project queues
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/queue'.format(project_id='project_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_resources(self):
        """Test case for list_resources

        Get list of project resources
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/resource'.format(project_id='project_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_run_instance(self):
        """Test case for run_instance

        Update instance to project
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/instance'.format(project_id='project_id_example'),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_queue(self):
        """Test case for update_queue

        Update queue to project
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/queue'.format(project_id='project_id_example'),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_resource(self):
        """Test case for update_resource

        Update resource to project
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})/resource'.format(project_id='project_id_example'),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

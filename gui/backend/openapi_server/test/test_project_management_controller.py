# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.project import Project  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProjectManagementController(BaseTestCase):
    """ProjectManagementController integration test stubs"""

    @unittest.skip("*/* not supported by Connexion. Use application/json instead. See https://github.com/zalando/connexion/pull/760")
    def test_add_project(self):
        """Test case for add_project

        Adding new project
        """
        project = openapi_server.Project()
        headers = { 
            'Accept': '*/*',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/owlapi/project',
            method='POST',
            headers=headers,
            data=json.dumps(project),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_project(self):
        """Test case for delete_project

        Deletes a Project
        """
        headers = { 
        }
        response = self.client.open(
            '/owlapi/project({projectId})'.format(project_id='project_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_project(self):
        """Test case for get_project

        Find Project by ID
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project({projectId})'.format(project_id='project_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_projects(self):
        """Test case for list_projects

        Get list of projects
        """
        headers = { 
            'Accept': '*/*',
        }
        response = self.client.open(
            '/owlapi/project',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("*/* not supported by Connexion. Use application/json instead. See https://github.com/zalando/connexion/pull/760")
    def test_update_project(self):
        """Test case for update_project

        Updates a Project
        """
        project = openapi_server.Project()
        headers = { 
            'Accept': '*/*',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/owlapi/project'.format(project_id='project_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(project),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

import os
import json
import glob
import shutil
import subprocess
import time
from project import Project
# from .openapi_server.models.project import Project
from openapi_server.models.project import Project as OPProject
from openapi_server.models.queue import Queue as OPQueue
from module import Module
from connexion.exceptions import ProblemException
import ast
import sys
import importlib.util
import logging

owl_path = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../owl'))

if not owl_path in sys.path:
    sys.path.append(owl_path)

DEFAULT_PATH_PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../projects")
DEFAULT_PATH_MODULES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")

class Engine():
    def __init__(self, projects_path = DEFAULT_PATH_PROJECTS, modules_path = DEFAULT_PATH_MODULES):
        logging.root.setLevel(logging.NOTSET)
        self.projects_path = projects_path
        self.modules_path = modules_path
        # TODO czasem 'dir', czasem 'path', nieno, ujednolicić to!
        self.projects = {}
        for project in os.listdir(path = self.projects_path): # TODO winksza walidacja, sprawdzić też config.json. Oddzielna funkcja
            self.add_project(project)

    
    ### DEFINICJE ###
    def get_modules(self):
        modules = os.listdir(path = self.modules_path)
        mod = list(filter(lambda k: '.py' in k, modules))       # pliki z '.py'
        mod2 = list(filter(lambda k: '__init__' not in k, mod)) # pliki bez __init__
        mod3 = [x.replace('.py', '') for x in mod2]
        retval = []
        retval_mod = {}
        for module_name in mod3:
            if module_name == 'module_source_cv' or \
               module_name == 'module_perspective_transform' or \
               module_name == 'module_sink_file':
                retval2 = {}
                mod_data = self.get_module_data(module_name)
                # print("mod data:" + mod_data)
                # print(mod_data)
                retval2['description'] = mod_data.get('description', 'Default description')
                retval2['id'] = mod_data.get('id', module_name)
                retval2['name'] = module_name
                retval.append(retval2)
        return retval

    def get_module_data(self, module_id):
        module_wrapper = importlib.import_module(module_id) # Coś do importu, wrapper na klasę
        r2 = module_wrapper.Module.get_config()
        return r2
    
    # def add_project_instance(self, project_id, instance_id):
    #     return self.projects[project_id].add_project_instance(instance_id)
    def add_project_instance(self, project_id):
        return self.projects[project_id].add_project_instance()
    def get_project_instances(self, project_id):
        return self.projects[project_id].get_project_instances()
    def delete_project_instance(self, project_id, instance_id):
        return self.projects[project_id].delete_project_instance(instance_id)
    def start_project_instance(self, project_id, instance_id):
        return self.projects[project_id].start_project_instance(instance_id)
    def get_instance_config(self, project_id, instance_name):
        return self.projects[project_id].get_instance_config(instance_name)
    ### ZARZĄDZANIE PROJEKTAMI ###
    '''
    Walidacja projektu:
    - Jeżeli nie istnieje plik 'project/config.json', to znaczy że projektu nie ma
        - Więc jeżeli istnieje folder 'project', to można go wywalić, cnie? # TODO
    - Jeżeli plik 'project/config.json' istnieje, to mamy projekt!
        - sprawdzać układ pliku 'config.json'? # TODO
    '''
    def get_projects(self):
        response = []
        for _, project in self.projects.items():
            response.append(project.get_config())
        return response
    def add_project(self, project_id):
        if os.path.isfile(os.path.join(self.projects_path, project_id, "config.json")):
            self.projects[project_id] = Project(os.path.join(self.projects_path, project_id), self.modules_path)
        else:
            print(f'*ACHTUNG* Katalog {os.path.join(self.projects_path, project_id)} nie zawiera pliku "config.json".')
    def create_project(self,data):
        openapi_project = OPProject.from_dict(data)
        try:
            if os.path.exists(os.path.join(self.projects_path, openapi_project.id, "config.json")):
                raise FileExistsError

            if not os.path.exists(os.path.join(self.projects_path, openapi_project.id)):  
                os.mkdir(os.path.join(self.projects_path, openapi_project.id))

            config = {}
            config['id'] = openapi_project.id
            config['name'] = openapi_project.name
            config['desc'] = openapi_project.description
            config['modules'] = {}
            config['queues'] = {}
            
            with open(os.path.join(self.projects_path, openapi_project.id, "config.json"), 'w') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            self.add_project(openapi_project.id)
            return [{}], 201 # TODO albo openapi_project
        except FileExistsError as e:
            raise ProblemException(409, "Project exists")
    def update_project(self, data):
        openapi_project = OPProject.from_dict(data)
        with open(os.path.join(self.projects_path, openapi_project.id, "config.json"), 'r') as f:
            config = json.load(f)
        if config['name'] != data['name']:
            self.change_project_name(config['name'], data['name'])
        config['name'] = openapi_project.name
        config['desc'] = openapi_project.description
        config['modules'] = {}
        with open(os.path.join(self.projects_path, openapi_project.id, "config.json"), 'w') as f:
            json.dump(config, f)

        return config
    def delete_project(self, project_id):
        # TODO jakiś project_kill
        try:
            if not os.path.exists(os.path.join(self.projects_path, project_id, "config.json")):
                raise FileNotFoundError
            self.kill_project(project_id)
            shutil.rmtree(os.path.join(self.projects_path, project_id))

        except FileNotFoundError as e:
            raise ProblemException(404, "Project not exists", str(e))

        return 'Deleted', 200
    def kill_project(self, project_id):
        self.projects[project_id].stop_project()
        del self.projects[project_id]
    def get_project_conf(self, project_id):
        return self.projects[project_id].get_config()
    def set_project_conf(self, project_id, data):
        retval = self.projects[project_id].set_config(data)
        if project_id != data.id:
            self.change_project_name(project_id, data.id)
        return retval
    def change_project_name(self, project_id, new_project_id):
        # usuń projekt z obiektów
        self.kill_project(project_id)
        # zmień nazwę folderu
        old_path = os.path.join(self.projects_path, project_id)
        new_path = os.path.join(self.projects_path, new_project_id)
        os.rename(old_path, new_path)
        # stwórz obiekt projektu
        self.add_project(new_project_id)
    def get_project_resources(self, project_id):
        return self.projects[project_id].get_resources()
    ### EDYCJA TORU PRZETWARZANIA ###
    def get_project_modules(self, project_id):
        return self.projects[project_id].get_modules()
        
    def add_project_module(self, project_id, module_name):
        return self.projects[project_id].add_module(module_name)
    def update_project_module(self, project_id, module_data):
        return self.projects[project_id].update_module(module_data)
    def get_project_module_data(self, project_id, module_id):
        return self.projects[project_id].get_module_data(module_id)

    def delete_project_module(self, project_id, module_id):
        return self.projects[project_id].delete_module(module_id)

    def get_module_params(self, project_id, module_id):
        return self.projects[project_id].get_module_params(module_id)
        
    def get_module_parameter(self, project_id, module_id, parameter):
        config = self.get_project_conf(project_id)
        param = config['modules'][module_id]['params'][parameter]
        return param
    # def set_module_parameter(self, project_id, module_id, parameter, value):
    #     config = self.get_project_conf(project_id)
    #     config['modules'][module_id]['params'][parameter] = value
    #     return self.set_project_conf(project_id,config)

    def set_module_params(self, project_id, module_id, params):
        return self.projects[project_id].set_module_params(module_id, params)
    
    ### URUCHOMIENIE/DEBUG ###
    def get_module_state(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        return config['modules'][module_id]['settings']['status']
    def set_module_state(self, project_id, module_id, value):
        config = self.get_project_conf(project_id)
        config['modules'][module_id]['settings']['status'] = value
        return self.set_project_conf(project_id,config)
    def module_start(self, project_id, module_id):
        config = self.get_project_conf(project_id)
        config['modules'][module_id]['settings']['status'] = True
        return self.set_project_conf(project_id,config)
        # TODO jakoś to jednak trzeba wystartować, a nie że ja tylko se zmiennom w pliku zmjenjam...
        # TODO walidacja, nie wystartuję już wystartowanego modułu
        # TODO jak ogarnę powyższe, to dopiero te pod spodem ogarnąć
    def module_stop(self, project_id, module_id):
        pass
    def module_restart(self, project_id, module_id):
        pass
    def get_module_log(self, project_id, module_id):
        pass
    
    def list_queues(self, project_id):
        queues = self.projects[project_id].list_queues()
        retval = []
        for name, vals in queues.items():
            task_queue_limit = vals.get('task_queue_limit')
            stream_queue_limit = vals.get('stream_queue_limit')
            task_queue_timeout = vals.get('task_queue_timeout')
            stream_queue_timeout = vals.get('stream_queue_timeout')
            project = self.projects[project_id].get_project()
            q = OPQueue(project, name, task_queue_limit, stream_queue_limit, task_queue_timeout, stream_queue_timeout)
            retval.append(q)
        return retval
    def get_queue(self, project_id, module_id):
        return self.projects[project_id].get_queue(module_id)
    def add_project_queue(self, project_id, queue):
        return self.projects[project_id].add_queue(queue)
    def modify_project_queue(self, project_id, queue):
        return self.projects[project_id].modify_queue(queue)
    def delete_project_queue(self, project_id, queue_id):
        return self.projects[project_id].delete_queue(queue_id)
    def get_project_queue_params(self, project_id, queue_id):
        return self.projects[project_id].get_project_queue(queue_id)
import sys
if __name__ == '__main__':
    x = Engine()
    print('xd')
    # print(x.list_queues('debug'))
    # print(x.get_queue('debug2', 'module_source_cv'))
    # print(x.create_project({"id": "ras", "name": "dwa", "description": "czy"}))
    # print(x.get_projects())
    # print(x.delete_project("ras"))
    # print(x.get_projects())
    # print(List.get_names())
    # print(x.get_projects())
    # print(x.get_project_conf('perspective_transform'))
    # print(x.get_modules())
    # print(x.get_project_modules('perspective_transform'))
    # print(x.delete_project_module('perspective_transform','module_sink_file'))
    # print(x.get_project_modules('perspective_transform'))
    # print(x.get_project_module_data('perspective_transform', 'module_source_cv'))
    # print(x.get_module_params('perspective_transform', 'module_source_cv'))
    
    # print(x.create_project('xddd'))
    # print(x.get_projects())
    # print(x.get_module_params('perspective_transform', 'module_sink_file'))
    print(x.get_module_data('module_source_cv'))
    # rd = x.get_module_data('perspective_transform')
    # print(rd[0].decode('utf-8'), rd[1].decode('utf-8'))
    # print(x.get_modules())
    # /project({projectId})/instance
    # x.add_project_instance('perspective_transform', 'erste_iksden')
    # x.add_project_instance('perspective_transform', 'zweite_iksden')
    # x.start_project_instance('perspective_transform', 'erste_iksden')
    # x.start_project_instance('perspective_transform', 'zweite_iksden')
    
    # while True:
        # time.sleep(30)
    # print(x.get_project_instances('perspective_transform'))
    # print(x.get_project_conf('perspective_transform'))





    # x.projects['perspective_transform'].start_project()
    # time.sleep(5)
    # # print(x.projects['perspective_transform'].get_logs())

    # # with open('xd.json', 'w') as y:
    # #     json.dump(x.projects['perspective_transform'].get_logs(), y, ensure_ascii=False, indent=4)
    # x.projects['perspective_transform'].stop_project()
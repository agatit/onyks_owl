import os
import json
import glob
import shutil
import subprocess
import time
from project import Project
# from .openapi_server.models.project import Project
from openapi_server.models.project import Project as OPProject
from module import Module
from connexion.exceptions import ProblemException
import ast

DEFAULT_PATH_PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../projects")
DEFAULT_PATH_MODULES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")

EMPTY_CONFIG = {
    'modules': {},
    'pipeline': {}
}
# TODO description i coś jeszcze
class Engine():
    def __init__(self, projects_path = DEFAULT_PATH_PROJECTS, modules_path = DEFAULT_PATH_MODULES):
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
                print(mod_data)
                retval2['description'] = mod_data.get('description', 'Default description')
                retval2['id'] = mod_data.get('id', 'Default ID')
                retval2['name'] = module_name
                
                # temp_mod = Module(module_name, None, os.path.join(self.modules_path, module_name + '.py'), None)
                # retval[module_name]['description'] = temp_mod.get_config.get('description', 'Default description')
                # retval[module_name]['id'] = temp_mod.get_config.get('id', 'Default ID')
                # retval[module_name]['name'] = module_name
                # TODO nno ten kod to mocno placeholderowy jest
                retval.append(retval2)
        return retval

    def get_module_data(self, module_id):
        # TODO kaman, mogę już ten subproces wywalić...
        proc = subprocess.Popen(['python3'], stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.stdin.write(bytes('import os\n', encoding='utf-8'))
        proc.stdin.write(bytes('os.chdir("' + DEFAULT_PATH_MODULES + '")\n', encoding='utf-8'))
        # proc.stdin.write(bytes('print(os.getcwd())\n', encoding='utf-8'))
        proc.stdin.write(bytes('from ' + module_id + ' import Module\n', encoding='utf-8'))
        # proc.stdin.write(bytes("x = Module(['" + module_id + "', '" + DEFAULT_PATH_PROJECTS + "/" + module_id + "/config.json', 'None'])\n", encoding='utf-8')) # TODO czy tutaj się nie rypnie bez "os.path.join()" ?
        proc.stdin.write(bytes('print(Module.get_config())', encoding='utf-8'))
        return_value = proc.communicate()[0].decode('utf-8')
        proc.kill()
        # print(return_value)
        r2 = ast.literal_eval(return_value)
        return r2
    
    def add_project_instance(self, project_id, instance_id):
        return self.projects[project_id].add_project_instance(instance_id)
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
    def add_project(self, id):
        self.projects[id] = Project(os.path.join(self.projects_path, id), self.modules_path)
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
            
            with open(os.path.join(self.projects_path, openapi_project.id, "config.json"), 'w') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            self.add_project(openapi_project.id)
            return config # TODO albo openapi_project
        except FileExistsError as e:
            raise ProblemException(409, "Project exists")
    def update_project(self, data):
        openapi_project = OPProject.from_dict(data)
        with open(os.path.join(self.projects_path, openapi_project.id, "config.json"), 'r') as f:
            config = json.load(f)
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
        return self.projects[project_id].set_config(data)
    
    def get_project_resources(self, project_id):
        return self.projects[project_id].get_resources()
    ### EDYCJA TORU PRZETWARZANIA ###
    def get_project_modules(self, project_id):
        return self.projects[project_id].get_modules()
        
    def add_project_module(self, project_id, module_name):
        return self.projects[project_id].add_module(module_name)
        
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
    def set_module_parameter(self, project_id, module_id, parameter, value):
        config = self.get_project_conf(project_id)
        config['modules'][module_id]['params'][parameter] = value
        return self.set_project_conf(project_id,config)

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

import sys
if __name__ == '__main__':
    x = Engine()
    print('xd')
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
    # print(x.get_module_data('module_source_cv'))
    # rd = x.get_module_data('perspective_transform')
    # print(rd[0].decode('utf-8'), rd[1].decode('utf-8'))
    # print(x.get_modules())
    # /project({projectId})/instance
    x.add_project_instance('perspective_transform', 'erste_iksden')
    # x.add_project_instance('perspective_transform', 'zweite_iksden')
    x.start_project_instance('perspective_transform', 'erste_iksden')
    # x.start_project_instance('perspective_transform', 'zweite_iksden')
    
    while True:
        time.sleep(30)
    # print(x.get_project_instances('perspective_transform'))
    # print(x.get_project_conf('perspective_transform'))





    # x.projects['perspective_transform'].start_project()
    # time.sleep(5)
    # # print(x.projects['perspective_transform'].get_logs())

    # # with open('xd.json', 'w') as y:
    # #     json.dump(x.projects['perspective_transform'].get_logs(), y, ensure_ascii=False, indent=4)
    # x.projects['perspective_transform'].stop_project()
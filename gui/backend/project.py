import os
import subprocess
import time 
import json
import sys
from module import Module

EXAMPLES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")
PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")

class Project():
    def __init__(self, project_path, modules_path): # TODO właśnie wywaliłem 'project_id', raczej nie będzie potrzebne, cnie?
        self.project_path = project_path
        self.config_path = os.path.join(self.project_path, 'config.json')
        self.config_json = self.load_config()
        self.modules_path = modules_path
        self.modules = {} # Nazwy modułów bez '.py'
        self.instances = {}
        """
        Instancja - lista modułów
        self.instances = {instance_id: {module_id: module_object}}
        # TODO ejkurwa, a instancje nie będą na siebie nachodzić?
        tylko jeżeli mam takie cuś teraz, to czy muszę tworzyć obiekty modułów?
        """
        # for mod in self.get_modules():
        #     self.modules[mod] = Module(os.path.join(self.modules_dir, mod + '.py'),self.config_path)
        self.load_modules()

    def add_project_instance(self, instance_id):
        if instance_id in self.instances:
            return None
        self.instances[instance_id] = {}
        for module_name in self.config_json['modules']:
            self.instances[instance_id][module_name] = Module(module_name, self.project_path, os.path.join(self.modules_path, module_name + '.py'), self.config_path, instance_id)
            self.instances[instance_id][module_name].module_start()
            print("Module ", module_name, " in ", instance_id, " started.")
    def get_project_instances(self):
        return list(self.instances.keys())
    def delete_instance(self, instance_name):
        if instance_name not in self.instances:
            return None
        for module in self.instances[instance_name]:
            module.module_stop()
        del self.instances[instance_name]
    def get_instance(self, instance_name):
        pass
        # TODO suma configów modułów
    def get_instance_module(self, instance_name, instance_module):
        pass
        # TODO config jednego modułu
    def load_config(self):
        try:
            with open(self.config_path) as file:
                config = json.load(file)
            return config
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return None
            # TODO Nnnnnnnnno chcę porobić te try/catche, ale pewnie da się to jeszcze nieco ulepszyć

    def load_modules(self):
        for mod in self.config_json['modules']:
            self.modules[mod] = Module(mod, self.project_path, os.path.join(self.modules_path, mod + '.py'), self.config_path, None)
    
    def set_config(self, data):
        try:
            self.config_json = data
            with open(self.config_path, 'w') as file:
                json.dump(data,file, ensure_ascii=False, indent=4)
            return 'coś'    # TODO returny
        except:
            return None
    def add_module(self, module_name):
        self.modules[module_name] = Module(module_name, self.project_path, os.path.join(self.modules_path, module_name + '.py'), self.config_path)
        # TODO if self.modules[module_name] is None: return "Łups :("
        self.config_json['modules'][module_name] = self.modules[module_name].get_default_config()
        return 'coś'

    def get_module_data(self, module_name):
        return self.config_json['modules'][module_name]
    def get_modules(self):
        return list(self.modules.keys())
    def delete_module(self, module_name):
        del self.config_json['modules'][module_name]
        del self.modules[module_name]

    def get_module_params(self, module_name):
        return self.modules[module_name].get_params()
    def get_config(self):
        return self.config_json
    def start_project(self):
        for x, y in self.modules.items():
            y.module_start()
            print(x, ' started')
    def stop_project(self):
        for x, y in self.modules.items():
            y.module_stop()
            print(x, ' stopped')
    def get_logs(self):
        return_value = {}
        for x, y in self.modules.items():
            return_value[x] = y.module_log()
            print(x, ' log acquired')
        return return_value
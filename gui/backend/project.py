import os
import subprocess
import time 
import json
import sys
from module import Module
from openapi_server.models.queue import Queue as OPQueue
# from queue import Queue

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
        self.queues = {}
        self.instance_helper = 0
        """
        Instancja - lista modułów
        self.instances = {instance_id: {module_id: module_object}}
        # TODO ejkurwa, a instancje nie będą na siebie nachodzić?
        tylko jeżeli mam takie cuś teraz, to czy muszę tworzyć obiekty modułów?
        """
        # for mod in self.get_modules():
        #     self.modules[mod] = Module(os.path.join(self.modules_dir, mod + '.py'),self.config_path)
        self.load_modules()
    def add_project_instance(self):
        instance_id = 'nazwa_projektu' + '_' + f'{self.instance_helper:02d}'
        if instance_id in self.instances:
            return None
        self.instances[instance_id] = {}
        # self.set_instance_config(instance_id)
        for module_name in self.config_json['modules']:
            self.instances[instance_id][module_name] = Module(module_name, self.project_path, os.path.join(self.modules_path, module_name + '.py'), self.config_path, instance_id)
            # self.instances[instance_id][module_name] = Module(module_name, self.project_path, os.path.join(self.modules_path, module_name + '.py'), self.instances[instance_id]['config'], instance_id)
        self.instance_helper += 1
        self.start_project_instance(instance_id)
        return "gitara"
    def get_project_instances(self):
        return list(self.instances.keys())
    def start_project_instance(self, instance_id):
        for module_name in self.config_json['modules']:
            self.instances[instance_id][module_name].module_start()
            print("Module ", module_name, " in ", instance_id, " started.")
    def stop_project_instance(self, instance_id):
        for module_name in self.config_json['modules']:
            self.instances[instance_id][module_name].module_stop()
            print("Module ", module_name, " in ", instance_id, " started.")
    def delete_project_instance(self, instance_name):
        if instance_name not in self.instances:
            return 'Łups :('
        for module in self.instances[instance_name]:
            module.module_stop()
        del self.instances[instance_name]
        return self.instances
    def get_instance(self, instance_name):
        if instance_name not in self.instances:
            return 'Łups :('
        return instance_name + " a co więcej to nie wiem :ppp"
        # TODO suma configów modułów
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
            if '#' in mod:
                name = mod[:mod.find("#")]
            else:
                name = mod
            self.modules[mod] = Module(name, self.project_path, os.path.join(self.modules_path, name + '.py'), self.config_path, None)
    def set_config(self, data):# def add_project_instance(self, project_id, instance_id):
        ### ZMIANA NAZWY PROJEKTU ###
        print('lol')
        # if self.config_json != da
        try:
            with open(self.config_path, 'w') as file:
                json.dump(data,file, ensure_ascii=False, indent=4)
            self.config_json = data
            return self.config_json
        except:
            return 'Łups :('
    def add_module(self, module_name):
        owl_path = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../owl')) # TODO owl_path jakiś globalniejszy zrobić...
        if not owl_path in sys.path:
            sys.path.append(owl_path)
        module_local_name = module_name
        name_helper = 0
        while module_local_name in self.modules:
            name_helper += 1
            module_local_name = module_name + '#' + str(name_helper)
        self.modules[module_local_name] = Module(module_name, self.project_path, os.path.join(self.modules_path, module_name + '.py'), self.config_path, None)
        if self.modules[module_local_name] is None: 
            return "Łups :("
        self.config_json['modules'][module_local_name] = self.modules[module_local_name].get_default_config()
        self.config_json['modules'][module_local_name]['id'] = module_name
        self.set_config(self.config_json)
        return {module_local_name:self.config_json['modules'][module_local_name]}
    def update_module(self, module):
        
        x = 2
        pass
    def get_module_data(self, module_name):
        if module_name in self.config_json['modules']:
            # response = 
            return self.config_json['modules'][module_name]
            # return self.modules[module_name].get_data()
        return 'Łups :('
    def set_module_params(self, module_id, params):
        self.config_json['modules'][module_id] = params
        self.set_config(self.config_json)
        return self.config_json['modules'][module_id]

    def get_modules(self):
        # return list(self.modules.keys())
        # response = {}
        response = []
        # response["input"] = None
        # response["output"] = None
        # response["comment"] = "Skąd to wziąć? Chyba gdzieś tutaj to jest..."
        # response["id"] = "w sumie to po co to brać, spoko podbijam cały 'project'?"
        # response["name"] = "O tu, zaraz pod spodem jest..."
        # response["project"] = self.get_config()
        for x, y in self.modules.items():
            # response[x] = y.get_params()
            # response.append(y.get_params())
            config = y.get_default_config()
            config['id'] = x
            config['name'] = y.name
            # y['id'] = x
            response.append(y.get_default_config())
        # response2 = [response]
        return response
    def delete_module(self, module_name):
        del self.config_json['modules'][module_name]
        del self.modules[module_name]
        self.set_config(self.config_json)
        return self.config_json['modules']

    def get_resources(self):
        return ["chwila moment", "nie tak szybko", "zrobie to bendom"]
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
        for x, y in self.instances.items():
            self.stop_project_instance(x)
    def get_logs(self):
        return_value = {}
        for x, y in self.modules.items():
            return_value[x] = y.module_log()
            print(x, ' log acquired')
        return return_value
    
    def list_queues(self):
        return self.config_json['queues']
    def add_queue(self, queue):
        name = queue.name
        id = queue._id
        id_helper = 0
        while id in self.config_json['queues']:
            id_helper += 1
            id = queue._id + '#' + str(id_helper)
        self.config_json['queues'][id] = {}
        self.config_json['queues'][id]['name'] = name
        self.config_json['queues'][id]['task_queue_limit'] = queue.task_queue_limit if queue.task_queue_limit != None else 6
        self.config_json['queues'][id]['task_queue_timeout'] = queue.task_queue_timeout if queue.task_queue_timeout != None else 5
        self.config_json['queues'][id]['stream_queue_limit'] = queue.stream_queue_limit if queue.stream_queue_limit != None else 0
        self.config_json['queues'][id]['stream_queue_timeout'] = queue.stream_queue_timeout if queue.stream_queue_timeout != None else 1
        self.set_config(self.config_json)
        return {id:self.config_json['queues'][id]}
    def modify_queue(self, queue):
        name = queue.name
        id = queue._id
        self.config_json['queues'][id] = {}
        self.config_json['queues'][id]['name'] = name
        self.config_json['queues'][id]['task_queue_limit'] = queue.task_queue_limit
        self.config_json['queues'][id]['task_queue_timeout'] = queue.task_queue_timeout
        self.config_json['queues'][id]['stream_queue_limit'] = queue.stream_queue_limit
        self.config_json['queues'][id]['stream_queue_timeout'] = queue.stream_queue_timeout
        self.set_config(self.config_json)
        return self.config_json['queues'][id]
    def get_queue(self, module_id):
        # return self.modules[module_id].get_queue()
        retval = {'input_queues': [],
                    'output_queues': []}
                
        iq = self.config_json['modules'][module_id].get('input_queues')
        if iq is not None:
            for q in iq:
                data = self.config_json['queues'].get(q)
                task_queue_limit = data.get('task_queue_limit')
                stream_queue_limit = data.get('stream_queue_limit')
                task_queue_timeout = data.get('task_queue_timeout')
                stream_queue_timeout = data.get('stream_queue_timeout')
                temp = OPQueue(self.get_project(), iq, task_queue_limit, stream_queue_limit, task_queue_timeout, stream_queue_timeout)
                retval['input_queues'].append(temp)
                
        oq = self.config_json['modules'][module_id].get('output_queues')
        if oq is not None:
            for q in oq:
                data = self.config_json['queues'].get(q)
                task_queue_limit = data.get('task_queue_limit')
                stream_queue_limit = data.get('stream_queue_limit')
                task_queue_timeout = data.get('task_queue_timeout')
                stream_queue_timeout = data.get('stream_queue_timeout')
                temp = OPQueue(self.get_project(), oq, task_queue_limit, stream_queue_limit, task_queue_timeout, stream_queue_timeout)
                retval['output_queues'].append(temp)

        return retval
    def get_project_queue(self, queue_id):
        retval = self.config_json['queues'][queue_id]
        return retval
    
    def delete_queue(self, queue_id):
        try:
            del self.config_json['queues'][queue_id]
        except:
            pass
        for mod in self.config_json['modules']:
            try:
                self.config_json['modules'][mod]['input_queues'].remove(queue_id)
            except:
                pass
            try:
                self.config_json['modules'][mod]['output_queues'].remove(queue_id)
            except:
                pass
        self.set_config(self.config_json)
        return self.config_json['queues']
    def get_project(self):
        retval = {
        "description": self.config_json.get('description'),
        "id": self.config_json.get('id'),
        "name": self.config_json.get('name')
        }
        return retval
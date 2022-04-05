import os
import multiprocessing
import importlib.util
import sys
import datetime
import logging
import json
from copy import deepcopy

owl_path = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../owl'))

class Module():
    def __init__(self, name, project_path, module_path, config_path, instance_id):
        self.name = name
        self.project_path = project_path
        self.module_path = module_path
        self.config = {}
        self.config_json = {}
        self.default_config = {}
        self.default_config_normalized = {}
        self.config_path = config_path
        self.instance_id = instance_id
        self.log_object = None
        if self.instance_id:
            self.stdout_path = os.path.join(self.project_path, 'logs', self.instance_id, str(datetime.datetime.now()) + '_' + self.name + '.txt')
            if not os.path.exists(os.path.join(self.project_path, 'logs', self.instance_id)):
                os.makedirs(os.path.join(self.project_path, 'logs', self.instance_id))
        self.process_handler = None

        self.import_config_json()
        self.import_default_config()
        self.normalize_default_config()
        # self.import_class()
        # print(self.default_config)
        # print(self.default_config_normalized)

    def create_logger(self):
        handler = logging.FileHandler(self.stdout_path, mode = 'x')
        handler.setLevel(logging.NOTSET)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        # logging.basicConfig(level=logging.DEBUG, handlers=[handler])
        self.log_object = logging.getLogger(name='owl_' + self.instance_id + "_" + self.name)
        # log_object.setLevel(logging.DEBUG)
        self.log_object.addHandler(handler)
        self.log_object.info(f"Logger {'owl_' + self.instance_id + '_' + self.name} created")
        print(f"Logger {'owl_' + self.instance_id + '_' + self.name} created")

    def import_class(self):
        sys.path.append(owl_path)
        module_wrapper = importlib.import_module(self.name) # Coś do importu, wrapper na klasę
        # self.module_object = module_wrapper.Module(self.config, None) # Stricte obiekt
        self.module_object = module_wrapper.Module.from_cmd(['xd',self.config_path, self.instance_id]) # Stricte obiekt

    def import_config_json(self):
        try:
            with open(self.config_path) as file:
                config = json.load(file)
                self.config_json = config
        except:
            print("Unexpected error:", sys.exc_info()[0])
    def import_default_config(self):
        # self.default_config = self.module_object.get_config()
        self.default_config = importlib.import_module(self.name).Module.get_config()
        self.config = self.default_config.copy()

    def normalize_default_config(self):
        self.default_config_normalized['params'] = {}
        for x, y in self.default_config['params'].items():
            self.default_config_normalized['params'][x] = y['value']
        if 'output_queues' in self.config_json['modules'][self.name]:
            self.default_config_normalized['params']['output_queues'] = self.config_json['modules'][self.name]['output_queues']
        if 'input_queues' in self.config_json['modules'][self.name]:
            self.default_config_normalized['params']['input_queues'] = self.config_json['modules'][self.name]['input_queues']
        
        # for x, y in self.default_config['output_classes'].items():
        #     # print(x, y.__module__, y.__name__)
        #     # self.default_config_normalized['params']['output_queues'][x] = f"{y.__module__}.{y.__name__}"
        #     self.default_config_normalized['params']['output_queues'].append(x)
        # for x, y in self.default_config['input_classes'].items():
        #     # print(x, y.__module__, y.__name__)
        #     # self.default_config_normalized['params']['input_queues'][x] = f"{y.__module__}.{y.__name__}"
        #     self.default_config_normalized['params']['input_queues'].append(x)
    def module_start(self):
        self.create_logger()
        self.import_class()
        self.process_handler = multiprocessing.Process(target=self.module_object.run, daemon=True)
        # self.process_handler = multiprocessing.Process(target=self.wrap(self.module_object.run, self.stdout_path), daemon=True)
            # proc = multiprocessing.Process(target=wrap(task, name), name=name,)
        self.process_handler.start()
    def module_stop(self):
        try:
            self.process_handler.terminate()
            self.process_handler.join()
            self.process_handler = None
        except:
            pass
    def module_restart(self):
        if self.process_handler is not None:
            self.module_stop()
            self.module_start()
    def module_status(self):
        return self.process_handler is not None # True albo false, odpalony albo nie
    
    def module_log(self, size=10):
        if size>10:
            size=10
        log_file = open(self.stdout_path, "r")
        # Google twierdzi że jak w tym samym programie otwieram ten sam plik kilka razy, to nie jest to straszne
        logs = log_file.readlines()
        return_value = logs[size*-1:]
        log_file.close()
        return return_value

    def get_default_config(self):
        # return self.default_config
        return self.default_config_normalized
    def get_data(self):
        return self.default_config_normalized['params']
    
    def get_params(self):
        # retval = self.config.deepcopy()
        # retval = {key: value for key, value in self.config.items()}
        retval = deepcopy(self.config)
        for x, y in retval['output_classes'].items():
            # print(x, y.__module__, y.__name__)
            retval['output_classes'][x] = f"{y.__module__}.{y.__name__}"
        for x, y in retval['input_classes'].items():
            # print(x, y.__module__, y.__name__)
            retval['input_classes'][x] = f"{y.__module__}.{y.__name__}"
        retval['id'] = self.name
        return retval
    def wrap(self, task, path):
        def wrapper(*args, **kwargs):
            # with open(os.path.join(path, name), 'x') as f:
            with open(path, 'x') as f:
                sys.stdout = f
                sys.stderr = f
                task(*args, **kwargs)
        return wrapper
    def get_queue(self):
        print(self.config)
# import tempfile
# tempdir = tempfile.mkdtemp()

# procs = []
# for i in range(8):
#     name = str(i)
#     proc = multiprocessing.Process(target=wrap(task, name), name=name,)
#     proc.start()
#     procs.append(proc)
# for proc in procs:
#     proc.join()
#     with open(os.path.join(tempdir, proc.name)) as f:
#         do_stuff_with(f.read())
# shutil.rmtree(tempdir)
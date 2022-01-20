import os
import multiprocessing
import importlib.util
import sys
import datetime
import logging

owl_path = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../owl'))

class Module():
    def __init__(self, name, project_path, module_path, config_path, instance_id):
        self.name = name
        self.project_path = project_path
        self.module_path = module_path
        self.config = {}
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

        self.import_default_config()
        self.normalize_default_config()
        # self.import_class()
        # print(self.default_config)
        # print(self.default_config_normalized)

    def create_logger(self):
        # handler = logging.StreamHandler(sys.stdout)
        handler = logging.FileHandler(self.stdout_path, mode = 'x')
        handler.setLevel(logging.NOTSET)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        # logging.basicConfig(level=logging.DEBUG, handlers=[handler])
        self.log_object = logging.getLogger(name='owl_' + self.instance_id + "_" + self.name)
        # log_object.setLevel(logging.DEBUG)
        self.log_object.addHandler(handler)
        self.log_object.setLevel(logging.NOTSET)
        self.log_object.info(f"Logger {'owl_' + self.instance_id + '_' + self.name} created")
        print(f"Logger {'owl_' + self.instance_id + '_' + self.name} created")

    def import_class(self):
        sys.path.append(owl_path)
        module_wrapper = importlib.import_module(self.name) # Coś do importu, wrapper na klasę
        # self.module_object = module_wrapper.Module(self.config, None) # Stricte obiekt
        self.module_object = module_wrapper.Module.from_cmd(['xd',self.config_path, self.instance_id]) # Stricte obiekt

    def import_default_config(self):
        # self.default_config = self.module_object.get_config()
        self.default_config = importlib.import_module(self.name).Module.get_config()
        self.config = self.default_config.copy()

    def normalize_default_config(self):
        self.default_config_normalized['params'] = {}
        for x, y in self.default_config['params'].items():
            self.default_config_normalized['params'][x] = y['value']
    def module_start(self):
        self.create_logger()
        self.import_class()
        self.process_handler = multiprocessing.Process(target=self.module_object.run, daemon=True)
        # self.process_handler = multiprocessing.Process(target=self.wrap(self.module_object.run, self.stdout_path), daemon=True)
            # proc = multiprocessing.Process(target=wrap(task, name), name=name,)
        self.process_handler.start()
    def module_stop(self):
        self.process_handler.terminate()
        self.process_handler.join()
        self.process_handler = None
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
        return self.config
    def wrap(self, task, path):
        def wrapper(*args, **kwargs):
            # with open(os.path.join(path, name), 'x') as f:
            with open(path, 'x') as f:
                sys.stdout = f
                sys.stderr = f
                task(*args, **kwargs)
        return wrapper
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
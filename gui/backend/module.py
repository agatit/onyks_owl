import os
import multiprocessing
import importlib.util
import sys

owl_path = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../owl'))

class Module():
    def __init__(self, name, project_path, module_path, config_path, instance_id):
        self.name = name
        self.project_path = project_path
        self.module_path = module_path
        self.default_config = {}
        self.default_config_normalized = {}
        self.config_path = config_path
        self.instance_id = instance_id

        self.stdout_path = os.path.join(self.project_path, 'logs', name + '.txt') # TODO zaraz zmieniam lokację, takżę ten...

        self.process_handler = None

        self.import_class()
        self.import_default_config()
        self.normalize_default_config()
        # print(self.default_config)
        # print(self.default_config_normalized)

    def import_class(self):
        sys.path.append(owl_path)
        module_wrapper = importlib.import_module(self.name) # Coś do importu, wrapper na klasę
        self.module_object = module_wrapper.Module([self.name,self.config_path, self.instance_id]) # Stricte obiekt

    def import_default_config(self):
        self.default_config = self.module_object.get_config()

    def normalize_default_config(self):
        for x, y in self.default_config.items():
            self.default_config_normalized[x] = y[1]
    def module_start(self):
        self.process_handler = multiprocessing.Process(target=self.module_object.run, daemon=True)
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
        return self.default_config
    def get_params(self):
        return self.config
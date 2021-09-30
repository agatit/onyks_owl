import os
import subprocess
import multiprocessing
import importlib.util
import sys
import threading

# TODO ejkurwadefaultconfigtotenztypami!!!!!!1111!1!1!!!
owl_path = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../owl'))

class Module():
    def __init__(self, name, project_path, module_path, config_path):
        self.name = name
        self.project_path = project_path
        self.module_path = module_path
        self.default_config = {}
        self.config_path = config_path
        
        self.stdout_path = os.path.join(self.project_path, name + '_stdout.txt')
        self.stderr_path = os.path.join(self.project_path, name + '_stderr.txt')

        self.process_handler = None
        # self.thread_handler = None

        self.import_class()
        self.import_default_config()

        # self.thread_handler = threading.Thread(target=self.module_object.run) # TODO nieco dziwnie to wygląda, ale raczej zadziała
        # self.thread_handler.daemon = True
        self.process_handler = multiprocessing.Process(target=self.module_object.run, daemon=True)

    def import_class(self):
        sys.path.append(owl_path)
        module_wrapper = importlib.import_module(self.name) # Coś do importu, wrapper na klasę
        self.module_object = module_wrapper.Module([self.name,self.config_path]) # Stricte obiekt

    def import_default_config(self):
        self.default_config = self.module_object.get_config()

    def module_start(self):
        self.process_handler.start()
        # self.thread_handler.run()
        # self.process_handler = Module([self.name, self.config_path])
        # self.process_handler.run()
        '''
        except:
            return 'ej, coś się zjebało'
        '''
        pass
    def module_stop(self):
        self.process_handler.terminate()
        self.process_handler.join() # TODO przenieść tego join'a wyżej w klasach
        pass
    def module_restart(self):
        if self.module_stop() == 'ej, to już nie żyje i tak...':
            return 'question mark'
        return self.module_start()
        # TODO jakiś try/catch? Tu się jakby kilka rzeczy więcej może wywalić...
    def module_status(self):
        return self.process_handler is not None # True albo false, odpalony albo nie
    
    def module_log(self, size=0):
        # TODO uwzględnić "size"
        log1 = open(self.stdout_path, "r")
        log2 = open(self.stderr_path, "r")
        # Google twierdzi że jak w tym samym programie otwieram ten sam plik kilka razy, to nie jest to straszne
        return_value = {}
        return_value['stdout'] = log1.read()
        return_value['stderr'] = log2.read()
        log1.close()
        log2.close()
        return return_value

    def get_default_config(self):
        return self.default_config
    def get_params(self):
        return self.config
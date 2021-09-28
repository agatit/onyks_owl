import os
import subprocess
import multiprocessing
import importlib.util
import sys

# TODO ejkurwadefaultconfigtotenztypami!!!!!!1111!1!1!!!
mod_nam_2 = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../owl'))

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

        proc = subprocess.Popen(['python3'], stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.stdin.write(bytes('import os\n',                                                                   encoding='utf-8'))
        proc.stdin.write(bytes('os.chdir("' + self.module_path + '")\n',                                        encoding='utf-8'))
        proc.stdin.write(bytes('print(os.getcwd())\n',                                                          encoding='utf-8'))
        proc.stdin.write(bytes('from module_perspective_transform import Module\n',                             encoding='utf-8'))
        proc.stdin.write(bytes("x = Module('" + self.project_path + "/perspective_transform/config.json')\n",   encoding='utf-8'))
        proc.stdin.write(bytes('print(x)\n',                                                                    encoding='utf-8'))
        self.default_config = proc.communicate()[0].decode('utf-8')
        proc.kill()
        # TODO wywalić stąd kiedyś ten 'subprocess' raczej...


        sys.path.append(mod_nam_2)
        w = importlib.util.find_spec(self.name, self.module_path)
        itertools = importlib.import_module(self.name)
        x = itertools.Module([self.name,self.config_path])
        print(x.get_config())
        module = importlib.util.module_from_spec(w)
        sys.modules[self.name] = module # TODO ta linijka chyba hasiok
        # TODO ogólnie nazwy w tej okolicy ogarnąć

    def module_start(self):

        file_path = self.module_path + self.name + '.py'
        module_name = 'Module'

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        self.process_handler = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.process_handler)
        # TODO logi?
        '''
        except:
            return 'ej, coś się zjebało'
        '''
    def module_stop(self):
        if self.process_handler:
            self.process_handler = None
        else:
            return 'ej, to już nie żyje i tak...'
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
import os
import subprocess


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

    def module_start(self):
        if self.process_handler is None:
            self.file1 = open(self.stdout_path, "w")
            self.file2 = open(self.stderr_path, "w")
            self.process_handler = subprocess.Popen(['python3', self.module_path, self.config_path], stdout=self.file1, stderr=self.file2)
            return 'jest gites'
        else:
            return 'ej, to już jest odpalone...'
        '''
        except:
            return 'ej, coś się zjebało'
        '''
    def module_stop(self):
        if self.process_handler:
            self.process_handler.kill()
            self.file1.close()
            self.file2.close()
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
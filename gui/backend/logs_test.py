import os
import subprocess
import time 
import json
import sys

EXAMPLES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")
PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")

file1 = open("log1.txt", "w")
file2 = open("log2.txt", "w")

process_1 = subprocess.Popen(['python3', EXAMPLES + '/module_source_cv.py', PROJECTS + '/file_view/config.json'], stdout=file1)
process_2 = subprocess.Popen(['python3', EXAMPLES + '/module_sink_win.py', PROJECTS + '/file_view/config.json'],  stdout=file2)

time.sleep(5)
process_1.kill()
process_2.kill()

# "python.exe" "%(here)s/../../owl/module_source_cv.py" "%(here)s/config.json"
# "python.exe" "%(here)s/../../owl/module_sink_win.py" "%(here)s/config.json"
# TODO co potem?
# będą uchwyty, trzeba będzie je gdzieś przechować
# może jakaś klasa "PROCESSES", obiekty byłyby o tej samej nazwie co projekty
# hmm... jeżeli logów na prawdę nie będzie za wiele, bo 'logging' zapętla (a widziałem ze raczej zapętla) to logi też mógłbym przechowywać w tej klasie
    # kurfa, na dobrą sprawę to mógłbym raz wczytać configi z plików na starcie i tyle!
    # nieno, ale jakieś niekontrolowane wyłączenie serwera?
    # ...
    # jeżeli był update configu, to co minutę zapisywanie go do pliku?
        # coś takiego, bo w sumie na chuj tyle tych operacji IO?!?!
        # albo zapisywanie przy każdym ważnym evencie, typu start projektu, albo request save'a od użytkownika
            # request save'a, nawet jeżeli sensowny, odstawiłbym na okolice robienia logowania
                # ej, właśnie, UŻYTKOWNICY!
                    # jprdleNIE, starczy rozkmin, jazda pracować!

# TODO jak bardziej ogarnę te dwie klasy niżej, to trzebaby to jakoś zmergować z 'file_read...'
class Project():
    def __init__(self, project_path, modules_path): # TODO właśnie wywaliłem 'project_id', raczej nie będzie potrzebne, cnie?
        self.project_path = project_path
        self.config_path = os.path.join(self.project_path, 'config.json')
        self.config_json = self.load_config()
        # TODO jak ładowanie się rypnie to jakiś error przesłać "Error while loading config.json", czy tam "Error while loading Project"
        self.modules_path = modules_path
        self.modules = {} # Nazwy modułów bez '.py'
        # for mod in self.get_modules():
        #     self.modules[mod] = Module(os.path.join(self.modules_dir, mod + '.py'),self.config_path)
        self.load_modules()

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
            self.modules[mod] = Module(os.path.join(self.modules_path, mod + '.py'), self.config_path)
    
    def set_config(self, data):
        try:
            self.config_json = data
            with open(self.config_path, 'w') as file:
                json.dump(data,file, ensure_ascii=False, indent=4)
            return 'coś'    # TODO returny
        except:
            return None
    def add_module(self, module_name):
        pass
    def get_modules(self):
        return self.modules.keys()
    def get_config(self):
        return self.config_json
class Module():
    def __init__(self, module_path, config_path):
        self.module_path = module_path
        self.default_config = {}
        self.config_path = config_path # TODO config_path? Już myślałem że na pamięci więcej siedzę :(((
        # self.stdout_path = os.path.join() # TODO logs path
        # self.stderr_path = os.path.join() # TODO logs path
        # self.launch_args = [ścieżka do pliku modułu, ścieżka do configu]
    def module_start(self):
        if self.process_handler is None:
            self.process_handler = subprocess.Popen(['python3', self.module_path, self.config_path], stdout=file1, stderr=file2)
        else:
            return 'ej, to już jest odpalone...'
    def module_stop(self):
        if self.process_handler:
            pass # TODO jak zabić proces potem? Kill? Terminate? Signal & Wait?
        else:
            return 'ej, to już nie żyje i tak...'
    def module_restart(self):
        if self.stop_module() == 'ej, to już nie żyje i tak...':
            return 'question mark'
        # TODO jakiś try/catch? Tu się jakby kilka rzeczy więcej może wywalić...
    def module_status(self):
        return self.process_handler is not None
    
    def module_log(self, size):
        pass
        # TODO co ja tu mam zwrócić?
            # nazwę pliku?
            # całego loga?
            # loga całego i niecałego?
        # TODO ogólnie to jak subprocess ogarnia pliki? Co jak otworzę kilka razy ten sam plik? Nie będzie melabejdo?
    # log
    def get_default_config(self):
        proc = subprocess.Popen(['python3', self.module_path, self.config_path], stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print (proc.communicate('from module_perspective_transform import Module'))
        print (proc.communicate('x = Module("./../examples/perspective_transform/config.json")'))
        print (proc.communicate('x.get_config()'))
        """
        from module_perspective_transform import Module
        x = Module("./../examples/perspective_transform/config.json")
        x.get_config()
        """
        pass
import os
import subprocess
import time 


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
    def __init__(self, project_path): # TODO właśnie wywaliłem 'project_id', raczej nie będzie potrzebne, cnie?
        self.project_path = project_path
        self.config_path = os.path.join(self.project_path, 'config.json')
        self.modules_dir = 'xd'
        # TODO jakoś tu przekazać 'modules_dir'
        # jakoś... raczej nie będę bawił się z parentem, po prostu zmienna więcej do konstruktora
        self.modules = {}
        for mod in self.get_modules():
            self.modules[mod] = Module(os.path.join(self.modules_dir, mod + '.py'),self.config_path)
        
    def get_modules(self):
        pass

class Module():
    def __init__(self, module_path, config_path):
        self.module_path = module_path
        self.config_path = config_path
        self.stdout_path = os.path.join() # TODO logs path
        self.stderr_path = os.path.join() # TODO logs path
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
    pass
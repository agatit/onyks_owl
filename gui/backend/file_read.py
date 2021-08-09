import os
import json 
import configparser

MY_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")

class Files():
    def __init__(self, examples_dir = MY_PATH):
        self.dir = examples_dir
        examples = os.listdir(path=MY_PATH)
        self.examples = {}
        for x in examples:
            if x != 'split':
                self.examples[x] = Example(x)
    def get_names(self):
        return self.examples.keys()
    def create_example(self, name):
        # TODO tworzenie nowego folderu/example'a
        pass
    def read_modules(self):
        # TODO na później - ogarnianie plików z './owl'
        pass
    def xdebug(self):
        for x in self.examples.values():
            x.read_logs()




class Example():
    def __init__(self, example_name): # TODO nieno, może bez defaulta, ale z wywalaniem błędu jak NULL
        # TODO przygotować wersję pod "create"
        self.name = example_name
        self.path = os.path.join(MY_PATH, self.name)
        self.config_path = os.path.join(self.path, 'config.json')
        self.supervisord = configparser.ConfigParser()  # TODO okej, parser se robię, a config otwieram i zamykam...
                                                        # co w końcu lepsze?!?!?!
        self.exec_path = os.path.join(self.path, 'run.bat') # TODO wersja również na linuxa
        self.logs_path = os.path.join(self.path, 'tmp')

        self.read_supervisord()

    def read_config(self):
        file = open(self.config_path)
        config = json.load(file)
        file.close()
        return config

    def save_config(self, data):
        # TODO zapisanie przyjętego słownika jako "config.json"
        pass
    def read_supervisord(self):
        self.supervisord.read(os.path.join(self.path, 'supervisord.conf'))
        # TODO przerobić zawartość obiektu na plaintext

    def save_supervisord(self, data):
        pass
        # TODO zapisywanie przyjętego słownika jako "supervisord.conf"
    
    def read_logs(self):
        ### OGARNIANIE NAZW MODUŁÓW ###
        modules = []
        for item in self.supervisord.sections():
            if item.startswith("program:"):
                # modules.append(item.removeprefix('program:'))
                modules.append(item[8:])
        ### OGARNIANIE NAZW I ZAWARTOŚCI PLIKÓW LOGÓW ###
        log_file_list = os.listdir(path=self.logs_path)
        logs = {}
        # TODO japierdole, jeszcze teraz numerki do SORSów domontowywać :////////////
        # TODO odpalić każdy moduł chociaż raz
        # TODO porobić wyjątki na wypadek braku plików
        # TODO ej mordo, tak sobie patrzę na "camera_view"
            # No i chyba pierdolę i wysyłam jak jest i chuj
        # TODO jak niby wysyłać video z takiego np. "camera_view"?
        

        for mod in modules:
            # if any(mod + '-stderr' in s for s in log_file_list):
            #     pass
            match_out = [s for s in log_file_list if mod + '-stdout' in s]
            match_err = [s for s in log_file_list if mod + '-stderr' in s]
            fmo = open(os.path.join(self.logs_path, match_out))
            logs[mod + '-stdout'] = fmo.read()
            fme = open(os.path.join(self.logs_path, match_err))
            logs[mod + '-stderr'] = fme.read()
        ### NAZWY I ZAWARTOŚCI PLIKÓW - "SINK" ###
        for i in range(self.supervisord['program:sink']['numprocs']):
            match_out = [s for s in log_file_list if 'sink_' + str(i) + '-stdout' in s]
            match_err = [s for s in log_file_list if 'sink_' + str(i) + '-stderr' in s]
            fmo = open(os.path.join(self.logs_path, match_out))
            logs[mod + '-stdout'] = fmo.read()
            fmo.close()

            fme = open(os.path.join(self.logs_path, match_err))
            logs[mod + '-stderr'] = fme.read()
            fme.close()

        ### PLIK SUPERVISORD.LOG ###
        fs = open(os.path.join(self.logs_path, 'supervisord.log'))
        logs['supervisord.log'] = fs.read()
        fs.close()
        print(logs)

    def read_exec(self):
        file = open(self.exec_path)
        data = json.load(file)
        file.close()
        return data
    def save_exec(self, data):
        # TODO ogarnianie pliku ".bat"/".sh"
            # nie wiem, pewnie póki co skopiować tak jak są i tyle, taki hardcode
        pass
    def run_example(self):
        # TODO odpalanie/wyłączanie procesu modułu
        pass

if __name__ == '__main__':
    List = Files()
    # print(List.get_names())
    List.xdebug()

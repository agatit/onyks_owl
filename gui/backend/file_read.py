import os

MY_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")

class Files():
    def __init__(self, examples_dir = MY_PATH):
        self.dir = examples_dir
        self.examples = os.listdir(path='./examples')
# TODO zczytanie folderów
# TODO example w słownik{'nazwa': obiekt}
# TODO dla każdego folderu - obiekt klasy tej poniżej
# TODO tworzenie nowego folderu/example'a
# TODO na później - ogarnianie plików z './owl'

class Example():
    def __init__(self, examples_dir = MY_PATH): # TODO nieno, może bez defaulta, ale z wywalaniem błędu jak NULL
        self.dir = examples_dir
# TODO zczytanie "config.json" do słownika
# TODO zapisanie przyjętego słownika jako "config.json"
# TODO czytanie pliku "supervisord.conf", pewnie do słownika
# TODO zapisywanie przyjętego słownika jako "supervisord.conf"
# TODO zczytywanie plików logów
    # logów nigdzie specjalnie nie zapisywać
        # otworzyć plik
        # pobrać tekst
        # zamknąć plik
        # zwrócić tekst
        # elo
    # po ogarnięciu pliku "supervisord.conf" będzie wiadomo jakich plików się spodziewać
        # na każdy moduł plik "*-stderr" & "*-stdout"
        # plik "supervisord.log"
# TODO ogarnianie pliku ".bat"/".sh"
    # nie wiem, pewnie póki co skopiować tak jak są i tyle, taki hardcode
# TODO odpalanie/wyłączanie procesu modułu
    def read_config(self):
        pass
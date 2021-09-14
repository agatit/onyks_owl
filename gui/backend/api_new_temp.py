from file_read_new_temp import Files
# TODO "api_new_temp", "api_real"... Nno te nazwy poogarniać...

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
# TODO (może wraz z frontem za jakiś czas) eleganckie środowisko uruchomieniowe
    # w sensie niech by to było ostatecznie na Dockerze, Kubernetsie, czy w kartonie.
    # Ale już teraz zacząć się zastanawiać nad takim ogarnięciem "podprojektów" i instrukcji do nich, żeby zaraz potem wpisać jedną/dwie linijki na spokojnie, a nie dzwonić potem do każdego o 4 nad ranem że coś skiepścił a chciał tylko popaczeć...

app = Flask(__name__)
api = Api(app)
data = Files()
# TODO po podorabianiu NULL'i, tutaj przy NULL zwracać ładny komunikat
# TODO a przy powodzeniach kod 200, czy coś w ten tegies
# TODO czy ja w ogóle regulaminowe klamerkowo etc. dane teraz zwracam?
    # postarajmy się żeby w tym drugim pliku było to obcykane
# TODO co zwraca POST/PUT?
    # Z tutka tak wygląda jakby "to co GET, ale poziom niżej".
# A DELETE?
    # "should return the updated resource" gdzieś Stack mamrocze. Raczej tego się trzymam
    # Jakby, i tak się bym trzymał, ale miałem nadzieję znaleźć jakieś profesjonalniejsze poprawcie w tej sprawie :ppp

"""
Kolejki zdarzeń z mapowaniem strumieni (do rozważenia, w tej chwili pliki config nie przewidują takiej struktury):
/owlapi/projects(<id>)/task_queues
/owlapi/projects(<id>)/task_queues(id)
/owlapi/projects(<id>)/task_queues(id)/params
/owlapi/projects(<id>)/task_queues(id)/params(<name>)
/owlapi/projects(<id>)/task_queues(id)/mapping - tablica par wejście-wyjście
"""
"""
/owlapi/modules (lista modułów ogólnie dostępnych)
/owlapi/modules/<string:module_id> (dostępne parametry modułu)
"""

class Modules(Resource):
    def get(self):
        return data.get_modules()
        # TODO ej, czy jak na tych GET'ach jest taka lista, to gites?!?!

class Module_x(Resource):
    def get(self, module_id):
        return data.get_module_data(module_id)

class Projects(Resource):
    def get(self):
        return data.get_projects()
        # TODO może zwracać projekt dopiero po znalezieniu config'u w folderze...
        # tylko to też w tej funkcji głębiej ogarnąć sytuację, gdy będzie trzeba stworzyć folder, a on już istnieje
    def post(self):
        json_data = request.get_json(force=True) # TODO po co ten "force"? Ogólnie to jest skopiowane ze Stacka i działa, nie to co wcześniej...
        return data.create_project(json_data['name'])
class Project_x(Resource):
    def get(self, project_id):
        return data.get_project_conf(project_id)

class Project_modules(Resource):
    def get(self, project_id):
        return data.get_project_modules(project_id)
    def post(self, project_id):
        json_data = request.get_json(force=True) # TODO po co ten "force"? Ogólnie to jest skopiowane ze Stacka i działa, nie to co wcześniej...
        return data.add_project_module(project_id, json_data['name'])
        
class Project_module_x(Resource):
    def get(self, project_id, module_id):
        return data.get_project_module_data(project_id, module_id)
    def delete(self, project_id, module_id):
        data.delete_project_module(project_id, module_id)
        return data.get_project_modules(project_id) # TODO nieno, te returny coś ten tegies...
    # TODO ten DELETE to może do klasy wyżej...
class Input_queue(Resource):
    '''
    TODO GET,PUT - nazwa kolejki (wydzielone określanie kolejek do rysowania połaczeń)
    '''
    pass
class Output_queue(Resource):
    '''
    TODO GET,PUT - nazwa kolejki (wydzielone określanie kolejek do rysowania połaczeń)
    W obu zwrócenie nazwy kolejki. Albo NULLa jeżeli np. inputa nie ma, bo zamiast tego jest 'input device' czy coś
    '''
    pass
class Param_defs(Resource):
    '''
    TODO GET - lista paramatrów z typami, mogą być typy złożone do których będzie trzeba zrobić edytory
    'params' + typ danych
        kłania się walidacja i rzutowanie
    tylko skąd wziąć typ danych?
        musi być zdefiniowany wcześniej, szczególnie jeżeli typy mają być "złożone"...
    '''
    pass
class Params(Resource):
    def get(self, project_id, module_id):
        return data.get_module_params(project_id, module_id)

# Do tego miejsca ogarnięte get/put/delete/post
# więcej jak zrobię podstawowe configi modułów z typami danych
class Parameter(Resource):
    '''
    GET,PUT - zmiana wartości parametru
    sam pojedyńczy 'params'
    '''
    def get(self, project_id, module_id, parameter):
        return data.get_module_parameter(project_id, module_id, parameter)
    def put(self, project_id, module_id, parameter):
        parser = reqparse.RequestParser()
        parser.add_argument('value')
        value = parser.parse_args()
        # TODO gdzieś w tej okolicy walidacja/porównanie typu otrzymanej wartości z typem który być powinien
        data.set_module_parameter(project_id, module_id, parameter, value)
        return data.get_module_parameter(project_id, module_id, parameter)

class Module_state(Resource):
    '''
    czyli dorabiamy 'SETTINGS'/metadane 
        ale nie do całego 'projektu', tylko do 'modułów'
        ... nie. W 'configu' raczej nie ma co tego trzymać...
        Oddzielnie jakoś, w samej 'bazie danych'
        Nawet nie w bazie. Tutaj, w klasie!
    GET,PUT - czy działa
    Metadata #1 - status. ON/OFF
    '''
    def get(self, project_id, module_id):
        return data.get_module_state(project_id, module_id)
    def put(self, project_id, module_id):
        pass

# TODO te poniżej START, STOP i RESTART, to żeby jakieś ogarnianie było że jak jest wystartowane, to raczej START nie zadziała. Albo RESTART jak jest STOP odpalony
# Zwracać pewnie będą kod && MODULE_STATE
# ...
# Może w drugim pliku walidacja, i na returnie MODULE_STATE i opinia(udało się/nie udało się)
# Chociaż taka skomplikowana procedura, przy zmianie wartości zero-jedynkowej...
# OWSZEM! JAKIŚ PROBLEM?
# Ale fakt, jakieś toto trochę skomplikowane, do tego się przysiądzie po zrobieniu poprzednich modułów

class Module_start(Resource):
    '''
    POST
    '''
    def post(self, project_id, module_id):
        pass
class Module_stop(Resource):
    '''
    POST
    Zmiana statusu
    '''
    def post(self, project_id, module_id):
        pass
class Module_restart(Resource):
    '''
    POST
    If ON: turn OFF, turn ON; else NULL;
    '''
    def post(self, project_id, module_id):
        pass
class Module_log(Resource):
    '''
    GET - pobranie loga. w parametrze może być ilośc wpisów
    Tylko gdzie/skąd będą logi, jak nie z supervisora?
    '''
    def get(self, project_id, module_id):
        pass
class Task_queue_length(Resource):
    '''
    Ilość tasków w kolejce
    albo "Ile modułów korzysta z kolejki?"
    '''
    # C H O C I A Ż
    # Jak to będzie ogarniane inaczej niedługo, to pewnie nie będę musiał główkować nad zczutywaniem parametrów po kolei i domyślaniu się, tylko zczytam np. inną tabelę z bazy
    pass
class Task_queue_flush(Resource):
    '''
    ???
    '''
    pass

### DEFINICJE ###
api.add_resource(Modules,                   '/owlapi/modules')
api.add_resource(Module_x,                  '/owlapi/modules(<string:module_id>)/params')

### ZARZĄDZANIE PROJEKTAMI ###
api.add_resource(Projects,                  '/owlapi/projects')
api.add_resource(Project_x,                 '/owlapi/projects(<string:project_id>)')

### EDYCJA TORU PRZETWARZANIA ###
api.add_resource(Project_modules,           '/owlapi/projects(<string:project_id>)/modules')
api.add_resource(Project_module_x,          '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)')
api.add_resource(Input_queue,               '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/input_queue')
api.add_resource(Output_queue,              '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/output_queue')
api.add_resource(Param_defs,                '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/param_defs')
api.add_resource(Params,                    '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/params')
api.add_resource(Parameter,                 '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/params(<string:parameter>)')

### URUCHOMIENIE/DEBUG ###

api.add_resource(Module_state,              '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/state')
api.add_resource(Module_start,              '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/start')
api.add_resource(Module_stop,               '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/stop')
api.add_resource(Module_restart,            '/owlapi/projects(<string:project_id>)/modules(<string_module_id>)/restart')
api.add_resource(Module_log,                '/owlapi/projects(<string:project_id>)/modules(<string:module_id>)/log')

api.add_resource(Task_queue_length,         '/owlapi/projects(<string:project_id>)/modules(<string:task_queue_id>)/length')
api.add_resource(Task_queue_flush,          '/owlapi/projects(<string:project_id>)/modules(<string:task_queue_id>)/flush')

if __name__ == '__main__':
    app.run(debug=True)
# TODO "api_new_temp", "api_real"... Nno te nazwy poogarniać...

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json


app = Flask(__name__)
api = Api(app)

"""
Kolejki zdarzeń z mapowaniem strumieni (do rozważenia, w tej chwili pliki config nie przewidują takiej struktury):
/owlapi/projects(<id>)/task_queues
/owlapi/projects(<id>)/task_queues(id)
/owlapi/projects(<id>)/task_queues(id)/params
/owlapi/projects(<id>)/task_queues(id)/params(<name>)
/owlapi/projects(<id>)/task_queues(id)/mapping - tablica par wejście-wyjście

"""

class Projects(Resource):
    def get(self):
        pass
    def post(self):
        pass
class Project_x(Resource):
    pass

class Modules(Resource):
    pass
class Module_x(Resource):
    pass
class Input_queue(Resource):
    pass
class Output_queue(Resource):
    pass
class Param_defs(Resource):
    pass
class Params(Resource):
    pass
class Parameter(Resource):
    pass
class Module_state(Resource):
    pass
class Module_start(Resource):
    pass
class Module_stop(Resource):
    pass
class Module_restart(Resource):
    pass
class Module_log(Resource):
    pass
class Task_queue_length(Resource):
    pass
class Task_queue_flush(Resource):
    pass
class Module_x(Resource):
    pass
class Module_x(Resource):
    pass
class Module_x(Resource):
    pass
class Module_x(Resource):
    pass

### ZARZĄDZANIE PROJEKTAMI ###
api.add_resource(Projects,          '/owlapi/projects')                                                     # TODO widok 'projektów'
# A więc jak stworzyć projekt?
# Patrząc na to co teraz mam, to "projektem" byłby nowy folder z foderu "examples", z 'config.json', skryptami odpalającymi, i 'supervisord.conf'
# Z JEDNYM skryptem odpalającym
# I BEZ 'supervisord.conf', bo odchodzimy od tego 
# Dobra, tutaj wystawiał będę same nazwy projektów
# TODO foldery z 'examples' wczytywać jako "projekty"
                                                                                                            # TODO GET & POST
api.add_resource(Project_x,         '/owlapi/projects<string:project_id>')                                  # TODO pojedyńczy projekt 
# Nno pojedyńczy projekt, ale co zwracać?
# 'config.json'?
# 'state' projektu?

### EDYCJA TORU PRZETWARZANIA ###
api.add_resource(Modules,           '/owlapi/<string:project_id>/modules')                                  # TODO GET, POST listowanie/dodawanie
# Lista modułów w projekcie
    # czyli elementów z 'owl'
        # czyli pierwszych elementów z 'config.json'
api.add_resource(Module_x,          '/owlapi/<string:project_id>/<string:module_id>')                       # TODO GET,DELETE - info/usuwanie
# Na 'delete' skasowanie modułu
# Na 'get' info o module
    # czyli wchodzimy głębiej w słownik/configs
api.add_resource(Input_queue,       '/owlapi/<string:project_id>/<string:module_id>/input_queue')           # TODO GET,PUT - nazwa kolejki (wydzielone określanie kolejek do rysowania połaczeń)
api.add_resource(Output_queue,      '/owlapi/<string:project_id>/<string:module_id>/output_queue')          # TODO GET,PUT - nazwa kolejki (wydzielone określanie kolejek do rysowania połaczeń)
# W obu zwrócenie nazwy kolejki. Albo NULLa jeżeli np. inputa nie ma, bo zamiast tego jest 'input device' czy coś

api.add_resource(Param_defs,        '/owlapi/<string:project_id>/<string:module_id>/param_defs')            # TODO GET - lista paramatrów z typami, mogą być typy złożone do których będzie trzeba zrobić edytory
# 'params' + typ danych
    # kłania się walidacja i rzutowanie
api.add_resource(Params,            '/owlapi/<string:project_id>/<string:module_id>/params')                # TODO GET - lista paramatrów z wartościami
# samo 'params'
api.add_resource(Parameter,         '/owlapi/<string:project:id>/<string:project_id>/<string:parameter>')   # TODO GET,PUT - zmiana wartości parametru
# sam pojedyńczy 'params'

### URUCHOMIENIE/DEBUG ###
# czyli dorabiamy 'SETTINGS'/metadane 
    # ale nie do całego 'projektu', tylko do 'modułów'
    # ... nie. W 'configu' raczej nie ma co tego trzymać...
    # Oddzielnie jakoś, w samej 'bazie danych'
    # Nawet nie w bazie. Tutaj, w klasie!
api.add_resource(Module_state,      '/owlapi/<string:project_id>/<string:module_id>/state')                 # TODO GET,PUT - czy działa
# Metadata #1 - status. ON/OFF
api.add_resource(Module_start,      '/owlapi/<string:project_id>/<string:module_id>/start')                 # TODO POST
api.add_resource(Module_stop,       '/owlapi/<string:project_id>/<string:module_id>/stop')                  # TODO POST
# Zmiana statusu
api.add_resource(Module_restart,    '/owlapi/<string:project_id>/modules<string_module_id>/restart')        # TODO POST
# If ON: turn OFF, turn ON; else NULL;
api.add_resource(Module_log,        '/owlapi/<string:project_id/<string:module_id>/log')                    # TODO GET - pobranie loga. w parametrze może być ilośc wpisów
# Tylko gdzie/skąd będą logi, jak nie z supervisora?
api.add_resource(Task_queue_length, '/owlapi/<string:project_id>/<string:task_queue_id>/length')
# Ilość tasków w kolejce
    # albo "Ile modułów korzysta z kolejki?"
api.add_resource(Task_queue_flush,  '/owlapi/<string:project_id>/<string:task_queue_id>/flush')
# ???
if __name__ == '__main__':
    app.run(debug=True)
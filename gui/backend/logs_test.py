import os
import subprocess
import time 

EXAMPLES = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../owl")
PROJECTS = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../../examples")

config_json = {
    "module_source_cv" : {   
        "output_queue" : "stage1",    
        "stream_queue_limit" : 100,
        "params": {
            "device": "../../samples/youtube/out_2_21.mp4"
        }
    },

    "module_sink_win" : {   
        "input_queue" : "stage1",    
        "input_streams" : {
            "color" : "stream_video",
            "metrics" : "stream_data"
        },
        "params": {
            "window_name": "camera_view"
        }        
    }
}

file1 = open("log1.txt", "w")
file2 = open("log2.txt", "w")

process_1 = subprocess.Popen(['python3', EXAMPLES + '/module_source_cv.py', PROJECTS + '/file_view/config.json'], stdout=file1)
process_2 = subprocess.Popen(['python3', EXAMPLES + '/module_sink_win.py', PROJECTS + '/file_view/config.json'],  stdout=file2)
# TODO jak zabić proces potem? Kill? Terminate? Signal & Wait?
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

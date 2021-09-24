main.py - Plik główny, znajduje się tam całe stricte API

"całe stricte API" to zrozumiale?

Nno apka Flaskowa oraz klasy odpowiadające zapytaniom API. Przyjmuje zapytania, zwraca jakieś dane, jakieś kody, a za całe myślenie/brudną robotę odpowiada:

engine.py - znajdująca się tam klasa 'engine' sprawdza jakie mamy dostępne moduły, jakie istnieją projekty, tworzy/modyfikuje projekty. Do projektów tworzy obiekty klasy 'project' znajdującej się w pliku:

project.py - Klasa 'project'. Zarządzanie projektem. Config. Dodawanie/kasowanie modułów. Odpalanie projektu/modułów. Ale na moduły też jest oddzielna klasa

module.py - o tutaj. Odpalanie modułu należącego do projektu. Logi modułu.
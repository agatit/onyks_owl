main.py - Plik główny, znajduje się tam całe stricte API

"całe stricte API" to zrozumiale?

Nno apka Flaskowa oraz klasy odpowiadające zapytaniom API. Przyjmuje zapytania, zwraca jakieś dane, jakieś kody, a za całe myślenie/brudną robotę odpowiada:

engine.py - znajdująca się tam klasa 'engine' sprawdza jakie mamy dostępne moduły, jakie istnieją projekty, tworzy/modyfikuje projekty. Do projektów tworzy obiekty klasy 'project' znajdującej się w pliku:

project.py - Klasa 'project'. Zarządzanie projektem. Config. Dodawanie/kasowanie modułów. Odpalanie projektu/modułów. Ale na moduły też jest oddzielna klasa

module.py - o tutaj. Odpalanie modułu należącego do projektu. Logi modułu.


Do pogadania:

- mam configi zwykłe, i takie z typami. Trzymamy oba, czy wszędzie decydujemy się na jeden rodzaj?

-jak operować configami? zapisywać od razu do pliku, a potem operować na danych z pliku? Otwierać go 50 razy na sekundę? Czy operować głównie na danych w pamięci, a save'a do pliku robić raz na sekundę/minutę/trigger od usera?

---

# TODO

- CTRL+F -> "setdefault"

- type()
- JEżeli lista jest pusta
    - ciepnij_placeholder()
# Sprawozdanie techniczne

## PARALAKSA

- Efekt występujący np. przy zwykłej obserwacji obiektu "na własne oczy": jedno oko będzie widziało ten obiekt nieco inaczej niż drugie.
- W przypadku obrazu video przyjąłem że klatka X to widok z jednego oka, a klatka X+1 to widok z drugiego oka.
- Folder "poc/parallax"

Paralaksę próbowałem wykorzystać do wytworzenia "z-buffera" - maski pokazującej jak daleko obiekt znajduje się od kamery. Miało to pomóc w identyfikacji przejeżdżającego pociągu.

Przetestowałem następujące funkcje biblioteki OpenCV:

- MOG

- StereoBM

- StereoSGBM

- StereoRectify

Spośród tych funkcji, najlepsze wyniki dostarcza funkcja StereoSGBM. Przetwarzanie obrazu jest stosunkowo czasochłonne,(dlatego późniejsze przetwarzanie miało miejsce na obrazie przeskalowanym do 480p), jednak przetworzony obraz najbardziej pokrywa się z rzeczywistością/oczekiwaniami. Z drugiej zaś strony barykady stoi MOG. MOG dostarcza wyników szybko, ale nie są wystarczająco precyzyjne.

Warto nadmienić, że każda z testowanych funkcji/algorytmów miała problemy z delikatnym ruchem samej kamery i wykrywaniem przejeżdżających cystern.

## PANORAMA

- Próba połączenia zdjęć pociągu z kolejnych klatek, celem stworzenia jednego ciągłego zdjęcia

- Folder "poc/parallax", pliki zaczynające się od "panorama"

Próba wykorzystywała OpenCV ORB do wykrycia kluczowych punktów na zdjęciach, a potem połączenie zdjęć przez dokonanie ich transformacji względem podobnych punnktów kluczowych

Próba udana dla pojedyńczych klatek, nieudana dla całego materiału

## ODSZUMIANIE

- Folder "poc/denoise"

- Delikatna próba poprawienia jakości obrazu z kamer

Próba zakończona na sprawdzeniu Dekonwolucji Weinera(niesatysfakcjonujące wyniki, przynajmniej bez zmiany parametrów), oraz znalezieniu [repozytorium](https://github.com/subeeshvasu/Awesome-Deblurring#multi-imagevideo-motion-deblurring) z wieloma różnymi sposobami na odszumianie różnego rodzaju materiałów

## ROZDZIELANIE WAGONÓW

- Folder "poc/wagon_split"

- Próba pobrania z video zdjęć poszczególnych wagonów

Wykorzystałem maskę wytworzoną przy okazji PARALAKSY. Potem na określonym obszarze dokonywałem pomiaru:

- Najwyższego (w osi Y) piksela z maski

- Średniej ilości pikseli z maski

Przy określonym spadku badanego parametru był robiony screenshot. W ulepszonej wersji algorytmu można by po wspomnianej detekcji dodatkowo przesuwać badany obszar wzdłuż toru jazdy pociągu, i w momencie dotarcia do następnego spadku wartości zapisać obraz pomiędzy tymi dwoma obszarami.

Metoda fajna, ale wymaga dobrej maski.

## MODEL 3D

- Folder "pod/parallax_3d"

- Próba wykonania modelu 3D przejeżdżającego pociągu

Wykorzystanie wspomnianej już paralaksy dało wyniki określone jako "... meh"

Jakaś ta paralaksa jest taka jakaś "... meh"

Wygląda ładnie, szybko, zrozumiale, ale potem przejeżdża cysterna, cała gładka, paralaksa nie ma wielu punktów odniesienia na niej, masz potem cysternę, krawędzie są gites, ale cała cysterna wklęsła.

Wspominałem o ruszaniu samą kamerą?

O śniegu i deszczu na pewno nie wspominałem. Bo nie sprawdzałem tego. Bo się boję...

# WRACAJĄC...

Paralaksa & Open3D - meh

OpenSFM - o, to już jest interesujące

Materiał mieli się... nno... 60 klatek (z 600 klatkowego materiału) pół godziny

... i potem wychodzi z tego chmura punktów. Chmura jest nawet gites.

Nie wspominając o czasie przetwarzania, dopracowania wymaga przerobienie chmury punktów na faktyczny model 3D, oraz pobranie do modelu tekstury z filmu, żeby być dokładniejszym niż kolory z chmury punktów.

# GUI

- Branch "GUI"

- Interfejs graficzny do całego programu, ustawiaie modułóœ, pipeline'ow, czytanie logów...

React <=> RestAPI <=> Flask

_Work in progress..._

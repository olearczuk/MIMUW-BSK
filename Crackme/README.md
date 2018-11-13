# Overview
Idea of this task was to find flag - password, that will be accepted by the program.


1. Opis programu
- po wpisaniu hasła program sprawdza, czy słowo ma 29 znaków (jeśli nie, to wypisuje 'Wrong.' i kończy działanie)
- wywoływana jest funkcja decrypt, która "naprawia" funkcję check (wcześniej były tam jakies dziwne rzeczy)
- wywoływana jest funkcja check, która zwraca 0, gdy hasło jest poprawne i 1 w przeciwnym wypadku
- w funkcji check dla kolejnego znaku w podanym haśle
	- wywoływana jest funkcja decrypt z argumentami 
		- wskaźnik z wartością 0xfeed000000 + 2 liczby oznaczające aktualny znak
		- wskaźnik do tablicy (0x4040e0)
	- nadpisuje ona na 1 wskaźnik wynik funkcji
	- wynik funkcji jest potem porównywany z kolejnym indeksem w tablicy correct_pass (adres 0x404060)
- jeśli nastąpi równość w porównaniu dla każdego znaku to check zwraca 0, w przeciwnym wypadku 1

2. Opis rozwiązania
- za pomocą pliku decrypt.c dla wszystkich 256 znaków wypisuję parę (1 argument, wynik) dla funkcji decrypt z argumentami
	- wskaźnik z wartością 0xfeed000000 + 2 liczby oznaczające aktualny znak
	- wskaźnik do tablicy (0x4040e0)
- na koniec wykonuje exit(0) -> mam wszystko, czego potrzebuję
- w pliku process_pairs.py trzymam w tablicy wartości tablicy correct_pass i korzystając z wygenerowanych danych 
  znajduję takie wejścia, dla których funkcja decrypt daje wynik odpowiadający kolejnym polom w tablicy correct_pass
- znając wejścia, znam kolejne litery z flagi, więc mogę odtworzyć flagę

polecenie sh script.sh wypisze flagę na standardowe wyjście 

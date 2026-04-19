---
title: Total Commander – wtyczka obsługująca własny format archiwum
url: https://asawicki.info/articles/total_commander_plugin_pl.php
published: '2026-01-01'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

*Ten artykuł został oryginalnie opublikowany w numerze 5/2025 (120) magazynu Programista.*

**W tym artykule zaprojektujemy własny format pliku, który pozwala spakować i skompresować wiele plików do jednego archiwum, podobnie jak format ZIP czy 7Z. Używając języka C++ i środowiska Visual Studio pod Windows, napiszemy następnie wtyczkę do managera plików Total Commander, który pozwoli na tworzenie i manipulowanie takim archiwum, w tym swobodne dodawanie i usuwanie plików w jego wnętrzu.**

Większość użytkowników Windowsa zapewne zarządza plikami z użyciem domyślnego, systemowego Eksploratora Windows. Istnieją jednak osobne aplikacje dedykowane do tego celu. Wśród nich warto poznać [ Total Commander](https://www.ghisler.com). Narzędzie to cechuje charakterystyczny interfejs podzielony na dwie kolumny. W każdej z nich – po lewej i po prawej stronie – znajdujemy się zawsze wewnątrz wybranego folderu z naszego dysku. Możliwe jest też tworzenie wielu zakładek po każdej stronie. To pozwala wygodnie przeglądać i porównywać pliki, a także wykonywać operacje takie jak kopiowanie i przenoszenie z jednej strony na drugą. Przykładowy zrzut ekranu zaprezentowano na Rysunku 1.

![Rysunek 1. Zrzut ekranu z programu Total Commander](../../assets/39dba660417a9bdb.png)

*Rysunek 1. Zrzut ekranu z programu Total Commander*

Total Commander dostępny jest na licencji shareware. Zapewnia pełną funkcjonalność za darmo. Podczas uruchamiania pokazuje jedynie dodatkowe okienko przypominające o wymaganej rejestracji. Po 30 dniach używania należy go zarejestrować. Choć i bez tego nadal działa, warto być w zgodzie z licencją i wesprzeć autora wymaganą kwotą 42 euro. Szczególnie że autor – szwajcarski programista Christian Ghisler – rozwija swój produkt niestrudzenie od 1993 roku.

Oprócz prostych operacji na plikach i folderach Total Commander ma mnóstwo innych przydatnych funkcji, w tym podgląd i porównywanie plików, synchronizację folderów, zaawansowane wyszukiwanie, wsadową zmianę nazwy wielu plików, obliczanie sum kontrolnych czy wbudowanego klienta FTP. Obsługuje też wiele formatów archiwów, w tym ZIP, RAR, ARJ. Systemowy eksplorator plików Windowsa od pewnego czasu też wprawdzie obsługuje archiwa ZIP, ale omawiany tutaj program wspiera więcej różnych formatów. Obsługuje także wtyczki, za pomocą których można dodawać wsparcie dla kolejnych takich formatów plików. Właśnie o tym będzie niniejszy artykuł.

Po co w ogóle pakować wiele plików do jednego archiwum? Powodów może być wiele. Pojedynczy plik łatwiej i wygodniej jest pobierać z Internetu czy udostępnić komuś przez Internet, kopiować czy przenosić. Sama operacja kopiowania czy nawet usuwania tysięcy małych plików byłaby też wolniejsza, niż operacja na jednym pliku. Kiedy zbiór plików stanowi pewną całość, spakowane razem są też mniej narażone na skopiowanie tylko części z nich lub omyłkowe usunięcie niektórych, co mogłoby doprowadzić do niespójnego stanu programu, który ich używa, a w konsekwencji do różnych błędów.

Ponadto, pakując pliki do archiwum, mamy często możliwość kompresji. Musimy tu jednak rozróżnić dwie rzeczy:

Słowo „kompresja” można rozumieć na wiele sposobów. Kompresja może być stratna lub bezstratna. Kompresję stratną stosujemy do treści multimedialnych, gdzie pewna utrata jakości jest akceptowalna. Stosują ją formaty plików takie jak obrazki (np. JPEG), muzyka (np. MP3) czy video (np. MP4 i kodeki takie jak H.264). Taką kompresją nie będziemy się jednak zajmować, ponieważ nam chodzi o możliwość pakowania dowolnych plików, a wszelkie inne ich rodzaje (jak dokumenty tekstowe, pliki wykonywalne czy dowolne inne pliki binarne) po spakowaniu i rozpakowaniu nie mogą mieć zmienionego nawet jednego bitu. Tak więc w tym artykule wykorzystamy jedynie kompresję bezstratną.

O kompresji bezstratnej możemy z kolei rozmawiać w kontekście wykorzystania określonego algorytmu. Takim algorytmem jest np. Deflate obsługiwany przez bibliotekę [zlib](https://zlib.net), czy LZMA, który również ma swoje SDK. Biblioteki tego rodzaju wspierają kompresowanie i dekompresowanie strumienia danych w pamięci. Dopiero na ich podstawie projektowane są określone formaty plików, które dodatkowo umożliwiają spakowanie wielu plików do jednego archiwum, definiują potrzebne nagłówki i inne elementy formatu. Na przykład format ZIP domyślnie używa algorytmu Deflate, a 7Z – algorytmu LZMA.

Tak więc kompresja danych i pakowanie wielu plików do jednego formatu archiwum często idą w parze, ale nie są tym samym, więc warto być świadomym tego rozróżnienia. Dobrym przykładem są tu wywodzące się ze świata Uniksa/Linuksa formaty: TAR, który obsługuje pakowanie wielu plików, ale nie obsługuje kompresji, oraz GZIP, który obsługuje kompresję, ale pakuje naraz tylko jeden plik. Dopiero ich połączenie daje możliwość spakowania i skompresowania wielu plików naraz. Stąd w świecie linuksowym spotykane są pliki o łączonym rozszerzeniu .tar.gz lub .tgz.

My tutaj, już w następnym rozdziale, zaprojektujemy własny format archiwum podobny do ZIP. Na początku zajmiemy się jedynie pakowaniem wielu plików i operacjami na nich, a dopiero na końcu dodamy obsługę kompresji z użyciem biblioteki zlib.

Można jeszcze zadać pytanie: Po co w ogóle projektować **własny format pliku archiwum** zamiast skorzystać z istniejącego, takiego jak np. ZIP? Takie podejście jest popularne m.in. wśród twórców gier i silników gier. Tysiące małych plików z modelami, teksturami czy efektami dźwiękowymi pakowane bywa do dużych archiwów nie tylko dla wygody i lepszej wydajności ładowania gry (dzięki zastosowanej kompresji), ale także celem schowania tych zasobów przed wścibskim okiem gracza, który mógłby chcieć wykraść te dane lub je zmodyfikować. To jednak na dłuższą metę nie jest skuteczne i stanowi błędne podejście *security by obscurity*, bo nie powstrzyma zaawansowanych programistów znających reverse engineering.

Zaprojektujemy teraz własny, prosty format pliku archiwum. Na początku określmy jego podstawowe parametry. Jego nazwą niech będzie „Sample Archive”, a zalecanym rozszerzeniem pliku: .smpa. Będzie to plik binarny, w którym liczby wielobajtowe zapisane są w porządku *little endian*, czyli naturalnym dla komputerów PC z procesorem x86. Budowę pliku przedstawiono na Rysunku 2.

![Rysunek 2. Struktura naszego pliku archiwum](../../assets/613ac4595d307b4f.png)

*Rysunek 2. Struktura naszego pliku archiwum*

Plik zaczyna się od 8-bajtowego nagłówka, który stanowią znaki: `"SMPA100A"`

. To dobra praktyka, aby format pliku mógł zostać zidentyfikowany już na samym początku. Dzięki sprawdzeniu takiego nagłówka unikniemy bowiem próby odczytu pliku w innym formacie jako naszego archiwum, co mogłoby doprowadzić do różnych błędów na późniejszym etapie. Pierwsze 4 znaki `"SMPA"`

niech identyfikują nasz format pliku, a następne 4 – `"100A"`

– stanową numer wersji. W przyszłości możemy bowiem rozbudować nasz format o nowe funkcje. Wówczas zaktualizowany program mógłby dzięki temu zidentyfikować i obsłużyć starą wersję formatu, jak i nową, o numerze wersji na przykład `"200A"`

, która z kolei będzie nieznana dla starej wersji programu. W tym artykule pozostaniemy jednak wyłącznie przy pierwszej wersji.

Za nagłówkiem, aż do końca pliku, ciągną się wpisy `Entry`

na temat kolejnych plików i katalogów. Każdy taki wpis może mieć zmienną długość, ale zawsze zaczyna się liczącym 28 bajtów nagłówkiem wpisu – `EntryHeader`

. Ten z kolei zawiera kilka pól:

`magic`

(32 bity) – magiczna liczba idenfikująca początek wpisu, o stałej wartości 0x1743C8F1 (zwróćmy uwagę, że wg porządku `flags`

(8 bitów) – flagi bitowe: 0x1 oznacza wpis usunięty (plik lub katalog nie istnieje, należy go zignorować i przeskoczyć), 0x2 oznacza dane skompresowane (obsługę kompresji dodamy dopiero w późniejszym rozdziale).`attributes`

(8 bitów) – kolejne flagi bitowe, tym razem kodujące atrybuty pliku lub katalogu, w formacie zgodnym z API Total Commandera. Na uwagę zasługuje wartość 0x10, która mówi o tym, że wpis jest katalogiem, a nie plikiem. Pozostałe to zwyczajne atrybuty, jakie możemy nadawać plikom, znane z systemu Windows.`time`

(32 bity) – data modyfikacji pliku, w formacie takim, jakiego używa Total Commander.`pack_size`

(64 bity) – długość danych pliku w bajtach tak, jak są one zapisane w archiwum, być może już po kompresji.`unp_size`

(64 bity) – oryginalna długość pliku w bajtach, przed kompresją. W przypadku braku kompresji te dwa rozmiary są sobie równe.`path_len`

(16 bitów) – długość łańcucha ze ścieżką do pliku/katalogu – liczba znaków Unicode.Po każdym takim nagłówku występuje ścieżka do pliku lub katalogu, zapisana jako ciąg 16-bitowych znaków Unicode (`wchar_t`

). Łańcuch ten nie jest zakończony zerem, bo znamy jego długość z wczytanego wcześniej nagłówka. Na przykład w archiwum testowym znajduje się jeden katalog, w nim jeden plik .jpg ze zdjęciem, a ponadto plik tekstowy. Razem więc archiwum zawiera 3 wpisy:

path = "Photos", attributes = 0x10 (DIRECTORY) path = "Photos\IMG_4627.jpg", attributes = 0x20 path = "TextFile.txt", attributes = 0x20

Wreszcie, po ścieżce występują już właściwe dane. W przypadku katalogów danych oczywiście nie ma, więc wtedy `pack_size = unp_size = 0`

.

**Dlaczego taki format pliku?**

Dlaczego nasz format pliku zaprojektowany został w ten sposób, z następującymi po sobie wpisami dotyczącymi kolejnych katalog i plików? Czy przechodzenie wszystkich wpisów po kolei oraz związane z tym skakanie po różnych miejscach archiwum, aby ominąć dane plików, nie jest mniej wydajne? Czy nie lepsze byłoby zaprojektowanie formatu tak, aby miał jakiś jeden, centralny indeks wszystkich plików i katalogów z ich nazwami i atrybutami (najlepiej zorganizowany hierarchicznie), a do danych odnosilibyśmy się dopiero w razie potrzeby pod konkretne offsety w archiwum?

Owszem, to wszystko prawda. Jednak ten format stanowi przykład edukacyjny, więc powinien być jak najprostszy. Równocześnie, API Total Commandera dotyczące wtyczek WCX pracuje w takim właśnie modelu, żądając przeglądania liniowo wszystkich wpisów. Nie jest to optymalne, a wynika pewnie ze względów historycznych – z budowy formatów takich jak ZIP i TAR. Nasz format zaprojektowaliśmy więc w ten sposób, aby obsługującą go wtyczkę do Total Commandera było jak najłatwiej zaimplementować.

Kod opisywany w tym artykule znaleźć można na GitHubie, w repozytorium: [ sawickiap/TotalCommanderPluginTutorial](https://github.com/sawickiap/TotalCommanderPluginTutorial). Będziemy się do niego odnosić w dalszej części artykułu. Do implementacji naszej wtyczki wykorzystamy język C++20 i środowisko Visual Studio 2022. Będzie to projekt stworzony w Visual Studio, bez użycia dodatkowych narzędzi, jak Cmake.

Total Commander obsługuje 4 rodzaje wtyczek:

Dokumentację do API dla wtyczek WCX znaleźć można na stronie [ghisler.com](https://www.ghisler.com), w dziale Addons → Plugins, ściągając i rozpakowując „WCX Plugin Guide” i otwierając plik *pkplugin.chm*. Format CHM jest obsługiwany między innymi przez aplikację SumatraPDF.

Nasz projekt musi kompilować się do biblioteki ładowanej dynamicznie **DLL**, jednak z rozszerzeniem zmienionym na **.wcx64** – co można ustawić w opcjach projektu → Advanced → Target File Extension.

Total Commander, jako aplikacja rozwijana od wielu dekad, zachowuje kompatybilność wsteczną ze starymi wersjami API dla wtyczek. My zaimplementujemy tylko najnowszą wersję – jako kod 64-bitowy, obsługujący 64-bitowe rozmiary plików (aby obsługiwać pliki większe, niż mieszczący się na 32 bitach rozmiar 4 GB) oraz ścieżki w postaci Unicode (aby obsługiwać polskie znaki diakrytyczne i dowolne inne symbole w nazwach plików i katalogów). Tak więc nasz projekt Visual Studio kompilowany będzie wyłącznie w wersji 64-bitowej, a funkcje API Total Commandera, które przyjmują łańcuchy znaków, będą miały przyrostek „W” oznaczający łańcuchy „szerokie” (ang. wide), a więc typu **wchar_t** – podobnie, jak w WinAPI.

Prawidłowo zaimplementowana wtyczka do Total Commandera nie tylko musi być biblioteką DLL, ale też musi **eksportować** określone funkcje. Jedne z nich są wymagane, inne – opcjonalne. Eksportowane funkcje oznaczone są następującymi dyrektywami:

`extern "C"`

– wyłącza „manglowanie” nazw funkcji C++, aby nazwa brzmiała dokładnie tak, jak została zapisana.`__declspec(dllexport)`

– eksportuje funkcję na zewnątrz (alternatywą byłoby posłużenie się osobnym plikiem .def z listą takich funkcji).`__stdcall`

– deklaruje standardową konwencję wywołania (kolejność podawania parametrów na stosie).W pliku *entry_points_legacy.cpp* zobaczyć możemy te spośród eksportowanych funkcji, które są przestarzałe. Pozostawiamy je niezaimplementowane. W swoim wnętrzu wykonują one `assert(0)`

oraz zwracają kod błędu. Liczymy na to, że nowe wersje Total Commandera uruchamiane na nowych, 64-bitowych wersjach Windowsa nigdy ich nie wywołują. Z kolei te funkcje wywoływane przez Total Commander, które faktycznie chcemy zaimplementować, znajdują się w pliku *entry_points.cpp*. Ich deklaracje przedstawiono w Listingu 1. W dalszej części artykułu zajmiemy się ich omówieniem.

*Listing 1. Funkcje API Total Commandera dla wtyczek WCX*

int __stdcall GetPackerCaps(); int __stdcall GetBackgroundFlags(); HANDLE __stdcall OpenArchiveW(tOpenArchiveDataW* archiveData); int __stdcall CloseArchive(HANDLE hArcData); int __stdcall ReadHeaderExW(HANDLE hArcData, tHeaderDataExW *headerData); int __stdcall ProcessFileW(HANDLE hArcData, int operation, wchar_t *destPath, wchar_t *destName); void __stdcall SetChangeVolProcW(HANDLE hArcData, tChangeVolProcW pChangeVolProc1); void __stdcall SetProcessDataProcW(HANDLE hArcData, tProcessDataProcW pProcessDataProc); // PK_CAPS_BY_CONTENT BOOL __stdcall CanYouHandleThisFileW(wchar_t* FileName); // PK_CAPS_NEW, PK_CAPS_MODIFY int __stdcall PackFilesW(wchar_t *packedFile, wchar_t *subPath, wchar_t *srcPath, wchar_t *addList, int flags); // PK_CAPS_DELETE int __stdcall DeleteFilesW(wchar_t *packedFile, wchar_t *deleteList);

Najpierw jednak musimy omówić kilka tematów ogólnych. Kompilując naszą wtyczkę do pliku .wcx64, **możemy ją zainstalować** w Total Commanderze w oknie Configuration → Options → Plugins → sekcja Packer plugins (.WCX) → przycisk Configure, wpisując rozszerzenie pliku smpa i wybierając ścieżkę do naszego skompilowanego pliku .wcx64. Przykład pokazano na Rysunku 3.

![Rysunek 3. Konfiguracja wtyczki WCX w Total Commanderze](../../assets/fe31140e322489d9.png)

*Rysunek 3. Konfiguracja wtyczki WCX w Total Commanderze*

Warto wiedzieć, że choć nie budujemy pliku wykonywalnego EXE, nadal możemy używać Visual Studio do **debugowania** naszego kodu. Musimy jedynie skonfigurować projekt tak, aby uruchamiał plik EXE Total Commandera. W tym celu, w opcjach projektu, w zakładce Debugging, w polu Command ustawiamy ścieżkę do programu taką jak *c:\Program Files\totalcmd\TOTALCMD64.EXE*. Wówczas po zbudowaniu projektu wystarczy wydać polecenie Debug → Start Debugging (skrót klawiszowy F5), a uruchomi się Total Commander. Kiedy tylko wejdziemy w nim do archiwum .smpa, nasza biblioteka zostanie załadowana, a wtedy zaczynają działać breakpointy i wszelkie inne funkcje debuggera.

Przed rozpoczęciem kodowania warto ustalić i spisać pewien standard, którego będziemy się trzymać. Ponieważ używamy nowoczesnego C++, błędy będziemy zgłaszać jako **wyjątki**. API Total Commandera definiuje szereg liczbowych kodów błędów (plik *third_party\wcxhead.h*, stałe `E_END_ARCHIVE`

, `E_NO_MEMORY`

itd.) W razie wystąpienia błędu będziemy więc rzucać takimi wartościami liczbowymi jako wyjątkami. Ponieważ jednak nasze API jest w C, wyjątek nie może opuścić naszej biblioteki. Dlatego funkcje najwyższego poziomu (te eksportowane z biblioteki DLL) łapią wyjątki i zamieniają je na zwrócenie kodu błędu jako wyniku funkcji.

Kiedy posługujemy się wyjątkami, aby nie groziły nam wycieki pamięci, warto nie alokować pamięci bezpośrednio funkcją `malloc`

czy operatorem `new`

, tylko używać techniki RAII i **inteligentnych wskaźników**. Tak właśnie zrobimy – do przechowywania wskaźników na zasoby użyjemy `std::unique_ptr`

. Nawet inne rodzaje zasobów, niż zwykła dynamicznie zaalokowana pamięć, będą przechowywane w tych wskaźnikach, a do ich prawidłowego zwolnienia posłuży nam własny *deleter*. W kodzie odnaleźć możemy strukturę `FcloseDeleter`

(wywołującą `fclose`

), `CloseHandleDeleter`

(wywołującą `CloseHandle`

) i inne podobne.

Do przechowywania **łańcuchów znaków** Unicode (jak te ze ścieżkami do plików) posłuży nam standardowy typ `std::wstring`

. Natomiast wszędzie tam, gdzie chodzi o przekazanie stałej referencji do istniejącego łańcucha, zamiast typu `std::wstring_view`

posłużymy się klasą `wstr_view`

z zewnętrznej [biblioteki str_view](https://github.com/sawickiap/str_view). Stanowi ona ulepszoną wersję takiego „widoku na łańcuch” oferującą konwersję na łańcuch zakończony zerem (metoda `c_str`

zwracająca typ `const wchar_t*`

) i pamiętającą, czy oryginalny łańcuch był zakończony zerem, aby bez potrzeby nie alokować nowego.

Total Commander może użyć naszej wtyczki do otwarcia archiwum w jednym z kilku trybów. Do zaimplementowania tej logiki dobrze nadaje się programowanie obiektowe. W plikach *archive.hpp* i *archive.cpp* klasa bazowa `ArchiveBase`

definiuje te pola i metody, które są wspólne dla różnych trybów, podczas gdy klasy pochodne będą implementowały poszczególne tryby pracy.

Pierwsza eksportowana funkcja:

ma za zadanie zwrócić flagi mówiące o tym, jakie funkcje obsługuje nasza wtyczka. Jako podstawowe warto zwrócić:**GetPackerCaps**

`PK_CAPS_MULTIPLE`

– mówi o tym, że nasze archiwum obsługuje pakowanie wielu plików naraz. Wydaje się to oczywiste, ale pamiętajmy, że nie każdy format spełnia to wymaganie (jak wspomniany wcześniej GZ).`PK_CAPS_SEARCHTEXT`

– pozwala Total Commanderowi wykorzystywać naszą wtyczkę do przeszukiwania wnętrza archiwum tak, jakby to był zwykły katalog, w tym przeglądania treści plików w środku celem wyszukiwania pełnotekstowego. Co ciekawe, nie musimy robić niczego specjalnego, aby ta funkcja działała, tak więc nie zaszkodzi dodać tę flagę.Druga eksportowana funkcja to

. Zwraca ona flagi mówiące o tym, że nasza wtyczka jest bezpieczna wątkowo podczas pakowania (**GetBackgroundFlags**`BACKGROUND_PACK`

), jak i rozpakowywania (`BACKGROUND_UNPACK`

), co pozwoli użytkownikowi na wykonywanie operacji na naszych archiwach w tle. Możemy te flagi zwrócić, ponieważ nasz kod naturalnie będzie bezpieczny wątkowo, jako że posłużymy się klasami i obiektami zamiast przechowywać bieżący stan w zmiennych globalnych.

Pierwszy i podstawowy tryb pracy polega na otwarciu archiwum do odczytu i przejściu po wszystkich plikach i katalogach w nim zawartych. Jego implementacja zawarta jest w pierwszej klasie pochodnej: `ReadingArchive`

.

W eksportowanej funkcji

naszym zadaniem jest otworzyć plik podany w parametrze **OpenArchiveW**`archiveData->ArcName`

oraz zwrócić jakiś „uchwyt” do otwartego archiwum. W tym celu w implementacji tej funkcji tworzymy obiekt klasy `ReadingArchive`

, a wskaźnik do tego obiektu zwracamy do Total Commandera jako uchwyt, zrzutowany na typ `HANDLE`

. Ten sam uchwyt otrzymamy następnie przekazany z powrotem jako pierwszy parametr do pozostałych funkcji omówionych w tym rozdziale.

Plik archiwum otwieramy jako binarny tylko do odczytu, a więc wywołujemy funkcję `_wfopen_s`

z parametrem `"rb"`

. Analogicznie, eksportowana funkcja

ma za zadanie zamknąć archiwum, więc w jej implementacji rzutujemy otrzymany uchwyt z powrotem na wskaźnik do obiektu naszej klasy, po czym usuwamy nasz obiekt. Spowoduje to automatyczne wywołanie funkcji **CloseArchive**`fclose`

na polu `archive_file_`

będącym inteligentnym wskaźnikiem.

Pomiędzy funkcją otwarcia i zamknięcia archiwum aplikacja wywołuje na przemian funkcje `ReadHeaderExW`

i `ProcessFileW`

.

ma za zadanie odczytać parametry następnego wpisu (pliku lub katalogu) i zwrócić je przez przekazany wskaźnik do struktury. Na przykład do parametru **ReadHeaderExW**`headerData->FileName`

trafić powinna nazwa wraz z lokalną ścieżką do danego elementu, a do `headerData->FileAttr`

– jego atrybuty, jak wskazane na Rysunku 2 pole `attributes`

. Funkcja powinna zwrócić 0, jeżeli odczytanie następnego wpisu się udało, lub `E_END_ARCHIVE`

, jeżeli się nie udało, ponieważ osiągnięty został koniec archiwum. Inne zwracane wartości też są oczywiście dopuszczalne w celu zasygnalizowania błędu.

Po każdym odczytaniu nagłówka, Total Commander wywołuje funkcję

, w której naszym zadaniem jest przetworzyć odczytany ostatnio plik lub katalog. Parameter operation mówi o tym, co powinniśmy z nim zrobić, i może przyjmować wartość:**ProcessFileW**

`PK_SKIP`

– pomijamy ten wpis. Należy przeskoczyć do następnego. My w tym celu wywołujemy funkcję `_fseeki64`

, która skacze w pliku archiwum do przodu o tyle bajtów, ile zajmują dane bieżącego pliku.`PK_TEST`

– testujemy ten wpis, np. obliczając i sprawdzając sumę kontrolną danych w pliku. Nasz format nie obsługuje sum kontrolnych, więc po prostu przeskakujemy wpis tak samo, jak w poprzednim przypadku.`PK_EXTRACT`

– rozpakowujemy katalog lub plik.W przypadku naszego testowego archiwum sekwencja funkcji, jaką Total Commander wywołuje z naszej biblioteki i zwracanych przez nie danych, zapisana w pseudokodzie, może wyglądać tak:

OpenArchiveW(ArcName="C:\Tmp\SampleArchive.smpa") → returned handle ReadHeaderExW(handle) → FileName="Photos", returned 0 ProcessFileW(handle, PK_SKIP) ReadHeaderExW(handle) → FileName="Photos\IMG_4627.jpg", returned 0 ProcessFileW(handle, PK_SKIP) ReadHeaderExW(handle) → FileName="TextFile.txt", returned 0 ProcessFileW(handle, PK_SKIP) ReadHeaderExW(handle) → returned E_END_ARCHIVE CloseArchive(handle)

Rozpakowanie implementuje funkcja `ReadingArchive::ExtractFile`

. Wykonuje ona kilka operacji:

`CombinePath`

. Na przykład jeżeli użytkownik chce rozpakować wspominany plik .jpg, a katalogiem docelowym jest `CreateDirectoryW`

.`ReadingArchive::UnpackFileContent`

.`SetFileAttributes`

.`SetFileTime`

.Ponieważ archiwa mogą być bardzo duże, a ich pakowanie i rozpakowywanie może trwać długo, warto pokazywać użytkownikowi pasek postępu. Total Commander wyposażony jest w taką możliwość. Jako twórcy wtyczki musimy jednak zaimplementować aktualizowanie tego paska. W tym celu implementujemy eksportowaną funkcję

. Dzięki niej aplikacja przekazuje do naszego kodu wskaźnik do funkcji **SetProcessDataProcW***callback* typu `tProcessDataProc`

, którą następnie my możemy wywoływać w różnych momentach, aby zaktualizować interfejs użytkownika z paskiem postępu podczas naszych operacji.

Wywołanie tej funkcji może się odbywać w dwóch trybach:

`ArchiveBase::UpdateBytesProcessedProgress`

.`ArchiveBase::UpdateDirectProgress`

.Jak często należy wywoływać funkcję aktualizującą pasek postępu? Z jednej strony warto informować użytkownika o postępach w miarę często, żeby nie miał on wrażenia, że program się zawiesił. Warto to robić nie tylko między plikami, ale również podczas rozpakowywania pojedynczego, dużego pliku. Z drugiej jednak strony, jeśli wywołanie tej funkcji powoduje odrysowanie się okienka aplikacji, to wywoływanie jej zbyt często może stanowić wąskie gardło dla wydajności, ograniczając ją bardziej, niż samo przetwarzanie danych – szczególnie operując na nowoczesnych, szybkich dyskach SSD.

Aby pogodzić te dwie przeciwstawne racje, obie nasze wspomniane wyżej funkcje realizują dodatkową logikę, w której odpytują system o aktualny czas w milisekundach (funkcja systemowa `GetTickCount64`

) i wywołują funkcję Total Commandera aktualizującą pasek postępu tylko wówczas, kiedy od poprzedniej aktualizacji minęła co najmniej określona liczba milisekund (stała `kProgressUpdateIntervalMilliseconds = 40`

).

Dodatkowo, okienko z paskiem postępu daje użytkownikowi możliwość wciśnięcia przycisku *Cancel*. Funkcja *callback* zwraca wówczas wartość 0. W naszym programie obsługujemy to, przerywając trwającą operację. Dodatkowo, plik, którego rozpakowywanie zostało przerwane lub zakończyło się błędem, zostaje usunięty funkcją systemową `DeleteFileW`

tak, aby nie pozostawić na dysku pliku pustego lub niekompletnego.

Na tym właściwie moglibyśmy zakończyć implementowanie naszej wtyczki, jeżeli jej zadaniem jest tylko przeglądanie wnętrza archiwów .smpa i rozpakowywanie katalogów i plików. Od tego momentu zaczynamy omawianie funkcji dodatkowych.

Pierwszą i najprostszą taką funkcją jest rozpoznawanie formatu pliku na podstawie jego treści. Bez niej Total Commander używa tylko rozszerzenia pliku do zidentyfikowania jego formatu. Kiedy nasza wtyczka zacznie obsługiwać rozpoznawanie swojego formatu po treści, użytkownik będzie mógł „wejść” do takiego archiwum klawiszem Enter, nawet jeżeli plik ma zupełnie inne rozszerzenie. Gdyby to rozszerzenie było skojarzone z otwarciem pliku w jakiejś aplikacji, nadal można to zrobić alternatywnym skrótem klawiszowym Ctrl+PgDn.

Aby dodać tę funkcję do naszej wtyczki, musimy zrobić dwie rzeczy:

`PK_CAPS_BY_CONTENT`

z eksportowanej funkcji `GetPackerCaps`

.**CanYouHandleThisFileW**

.Warto wiedzieć, że po dodaniu nowych flag zwracanych przez `GetPackerCaps`

trzeba wtyczkę usunąć i od nowa dodać w konfiguracji Total Commandera, ponieważ program zachowuje sobie flagi zainstalowanych wtyczek.

Funkcja `CanYouHandleThisFileW`

to nic innego, jak nowy tryb działania naszego kodu. Total Commander nie wywołuje wówczas funkcji `OpenArchiveW`

ani żadnej innej omówionej wcześniej w rozdziale „Odczyt archiwum”, a jedynie tę jedną. W tym trybie naszym zadaniem jest otworzyć wskazane archiwum do odczytu, a następnie sprawdzić tylko jego nagłówek (pierwsze 8 bajtów), aby zweryfikować, czy zgadza się ze specyfikacją naszego formatu pliku. Do tego celu posłuży nam druga klasa pochodna: `HeaderCheckingArchive`

. Na końcu funkcja `CanYouHandleThisFileW`

ma zwrócić wartość typu `BOOL`

– prawdę, kiedy udało się rozpoznać wskazany plik jako archiwum w naszym formacie, i fałsz, kiedy się to nie udało lub wystąpił jakikolwiek inny problem.

Możliwość przeglądania wnętrza archiwum tak, jakby to był zwykły katalog, a także rozpakowywania (kopiowania) plików z jego wnętrza, jest bardzo wygodna. Jednak dopiero możliwość tworzenia nowych i modyfikowania istniejących archiwów dostarcza pełni funkcjonalności, jaką Total Commander oferuje.

Aby utworzyć nowe archiwum, należy:

Aby dodać pliki do istniejącego archiwum, wystarczy po jednej stronie wejść do tego archiwum jak do katalogu, a po drugiej zaznaczyć wybrane pliki lub katalogi i wydać zwyczajne polecenie ich skopiowania na przeciwną stronę (klawisz F5).

Aby nasza wtyczka zaczęła obsługiwać obie te funkcje, musimy zrobić dwie rzeczy:

`PK_CAPS_NEW`

i `PK_CAPS_MODIFY`

z eksportowanej funkcji `GetPackerCaps`

.**PackFilesW**

.Funkcja ta to nic innego, jak kolejny element pełnej obsługi nowego formatu archiwum przez nasz kod. Tworzymy więc nową klasę pochodną: `PackingArchive`

. W metodzie `OpenForPack`

będzie ona otwierała plik archiwum do zapisu. Najpierw wywołuje funkcję `_wfopen_s`

z parametrem `"r+b"`

, próbując otworzyć istniejący plik do odczytu i zapisu. Jeżeli to się nie uda, tworzy nowy plik, używając parametru `"wb"`

.

Parametry przekazywane do `PackFilesW`

są dość skomplikowane, więc wymagają dokładnego omówienia.

`PackedFile`

to ścieżka bezwzględna do archiwum, które mamy utworzyć lub wzbogacić o nowe pliki.`SubPath`

zawiera na ścieżkę względną wewnątrz naszego archiwum, gdzie mamy umieścić dodawane pliki. Może też być `NULL`

– wówczas pliki dodajemy na najwyższym poziomie archiwum, nie w żadnym podkatalogu.`SrcPath`

to bazowa ścieżka bezwzględna, gdzie znajdują się pliki i katalogi źródłowe przeznaczone do dodania.`AddList`

zawiera całą listę ścieżek względnych do poszczególnych plików i katalogów, które mamy dodać. Każda pozycja na tej liście zakończona jest zerem, a po ostatniej pozycji następują dwa bajty zerowe. Inaczej mówiąc, lista zakończona jest łańcuchem pustym. Musimy więc umiejętnie posłużyć się wskaźnikami, aby odczytać po kolei wszystkie łańcuchy z tej listy. W naszym kodzie odpowiada za to funkcja `ParseStringList`

.Aby lepiej to zrozumieć, rozpatrzmy przykład. Opisywaną sytuację pokazano na Rysunku 4. Czerwoną strzałką zaznaczony jest katalog, w którym znajdujemy się aktualnie w Total Commanderze, odpowiednio po lewej i po prawej stronie. Użytkownik chce dodać więcej zdjęć do podkatalogu *Photos* w naszym przykładowym archiwum. W tym celu:

![Rysunek 4. Przykład dodawania plików do archiwum](../../assets/6275af10dd6299fc.png)

*Rysunek 4. Przykład dodawania plików do archiwum*

Wówczas do wykonania całej tej operacji nasza wtyczka otrzymuje pojedyncze wywołanie funkcji `PackFilesW`

z następującymi parametrami:

`PackedFile="c:\Tmp\SampleArchive.smpa"`

– ścieżka docelowego archiwum`SubPath="Photos"`

– docelowy katalog wewnątrz archiwum`SrcPath="c:\MyNewPhotos\"`

– bazowy katalog źródłowy (zwróć uwagę na dodatkowy ukośnik na końcu)`AddList`

– lista łańcuchów ze ścieżkami do plików i katalogów źródłowych:
`"London at night.jpg"`

`"Family\"`

(tu również pozycja będąca katalogiem kończy się odwrotnym ukośnikiem)`"Family\Mother.jpg"`

`"Family\Son.jpg"`

Nową zawartość archiwum po wykonaniu całej operacji zilustrowano na Rysunku 5.

![Rysunek 5. Archiwum po dodaniu nowych plików](../../assets/d9e7e1a2185c0c06.png)

*Rysunek 5. Archiwum po dodaniu nowych plików*

Wykonanie takiej operacji byłoby dość proste, gdyby zawsze chodziło tylko o dodanie nowych plików i katalogów do archiwum. W końcu nasz format pliku zaprojektowany został tak, że wpisy następują kolejno po sobie, więc wystarczyłoby otworzyć plik w trybie *append* (parametr `"ab"`

) i dodać nowe wpisy na końcu.

Jednakże może się zdarzyć tak, że nowo dodawane pliki nazywają się tak samo, jak istniejące już w archiwum. Wówczas sytuacja staje się bardziej skomplikowana. Nie chcemy mieć w archiwum dwóch plików o tej samej nazwie (nawet różniących się wielkością liter – podążając za konwencją Windowsa, nazwy porównujemy bez rozróżniania wielkości liter, a więc funkcją `_wcsicmp`

).

Jeżeli więc otworzyliśmy istniejące archiwum, a nie utworzyliśmy nowe, to musimy przejrzeć wszystkie istniejące wpisy i usunąć te, które odpowiadają nadpisywanym plikom. Temu służy większość logiki w metodzie `PackingArchive::PackFilesW`

, a w szczególności wywołanie metody `PackingArchive::DeleteIf`

. W naszym formacie pliku wpisy usuwamy, po prostu zaznaczając je jako usunięte – dodając do pola `EntryHeader::flags`

wartość `Deleted = 0x1`

.

Nadal nie omówiliśmy jeszcze ostatniego parametru funkcji `PackFilesW`

– `flags`

. Może on przyjmować dodatkowe flagi bitowe oznaczające specjalne tryby pracy:

`PK_PACK_MOVE_FILES`

– oznacza, że pakowane pliki i katalogi źródłowe powinny być przenoszone, a nie kopiowane, więc po ich zapisaniu do archiwum należy oryginalne usunąć. Katalogi usuwamy funkcją systemową `RemoveDirectoryW`

, a pliki – `DeleteFileW`

.`PK_PACK_SAVE_PATHS`

to tryb, w którym użytkownik może zażądać spakowania jedynie płaskiej listy plików, bez struktury podkatalogów, odznaczając w okienku Pack files pole „Also pack path names (only recursed)". Nie wydaje się to zbyt przydatną funkcją, ale dla kompletności w przykładowej wtyczce zostało zaimplementowane.Jako ostatnia opcjonalna część API Total Commandera, którą zaimplementujemy, pozostała nam możliwość usuwania plików i katalogów wewnątrz archiwum. Z punktu widzenia użytkownika jej wykorzystanie jest proste: Wystarczy wejść do wnętrza archiwum jak do katalogu, zaznaczyć wybrane elementy i wydać polecenie usunięcia (klawisz F8 lub Del).

Aby nasza wtyczka zaczęła obsługiwać tę funkcję, musimy zrobić dwie rzeczy:

`PK_CAPS_DELETE`

z eksportowanej funkcji `GetPackerCaps`

.**DeleteFilesW**

.Parametry przekazywane do funkcji `DeleteFilesW`

są pewnym stopniu podobne do `PackFilesW`

. Pierwszy parametr to ponownie pełna ścieżka do pliku archiwum, na którym mamy operować. Drugi natomiast to cała lista ścieżek do katalogów i plików wewnątrz archiwum, które powinniśmy usunąć.

Jeżeli użytkownik wejdzie do archiwum opisanego w poprzedniej sekcji, wzbogaconego już o nowe pliki .jpg (Rysunek 5), wejdzie do podkatalogu *Photos*, zaznaczy wszystkie 3 znajdujące się tam elementy i wyda polecenie ich usunięcia, wówczas wywołana zostanie jeden raz funkcja `DeleteFilesW`

, a w parametrze `deleteList`

znajdą się następujące łańcuchy:

"Photos\Family\*.*" "Photos\IMG_4627.jpg" "Photos\London at night.jpg"

Zwróćmy uwagę, że – inaczej, niż to było dotychczas – tym razem Total Commander nie podaje ścieżki do każdego pliku i katalogu osobno. Zamiast tego specyfikuje cały katalog do usunięcia, oczekując, że usuniemy z niego rekurencyjnie wszystkie pliki i podkatalogi.

Ścieżka do katalogu zakończona jest łańcuchem `"\*.*"`

, ale nie wydaje się, abyśmy potrzebowali traktować ten element jako prawdziwą maskę plików do usunięcia, ponieważ użytkownik nie ma możliwości wybrania żadnej innej, aby na przykład usunąć tylko pliki o określonym rozszerzeniu. To tylko sposób, w jaki Total Commander sygnalizuje, że chodzi o usunięcie całego katalogu wraz z zawartością, a nie pojedynczego pliku. W naszym kodzie maskę tę po prostu usuwamy z końca łańcucha.

Implementacja metody `DeletingArchive::DeleteFilesW`

buduje więc wektor łańcuchów z nazwami ścieżek do plików i katalogów przeznaczonych do usunięcia (zamienione na duże litery i posortowane, dla łatwiejszego wyszukiwania), by w końcu wywołać wspomnianą już wcześniej metodę `DeleteIf`

, która przechodzi po wszystkich wpisach w archiwum, i te, które spełniają podany predykat, zaznacza jako usunięte dodając odpowiednią flagę.

**Jak usuwać pliki z archiwum?**

Jak zapewne do tej pory domyśliłeś/aś się, usuwanie plików z archiwum poprzez zaznaczanie ich flagą Deleted, aby były pomijane przy przetwarzaniu, nie jest najlepszą metodą. Nie tylko nasze archiwum pozostaje tej samej wielkości po usunięciu wybranych czy nawet wszystkich jego elementów, ale też dane usuniętych plików nadal się tam znajdują, co mogłoby powodować niepożądany wyciek wrażliwych danych. Taka metoda usuwania została zaimplementowana w przykładowym kodzie ze względu na prostotę.

Jak można to zrobić lepiej? Niestety, pośród funkcji operujących na plikach nie istnieje taka, która by wycięła część bajtów ze środka pliku. Jedyne, co możemy robić, to dopisywać nowe bajty na końcu pliku (zwiększając tym jego rozmiar) lub nadpisywać istniejące bajty (kiedy przestawimy kursor gdzieś pośrodku pliku). Istnieje też funkcja, która ustawia długość pliku skracając go i porzucając dane na jego końcu (`_chsize_s`

z biblioteki standardowej Visual Studio lub `SetEndOfFile`

z WinAPI). Korzystając z tych funkcji, możemy sobie wyobrazić różnorodne rozwiązania usuwania elementów z wnętrza archiwum:

Jako ostatnią część kodu naszej wtyczki dodamy obsługę kompresji. Nasz format pliku jest już na to przygotowany. Nie musimy więc definiować jego nowej wersji. Struktura `EntryHeader`

może mieć flagę Compressed (wartość 0x2) oraz zawiera osobne pole na długość danych skompresowanych w archiwum `pack_size`

i nieskompresowanych `unp_size`

. Wystarczy, że teraz zrobimy użytek z tych możliwości.

Do kompresji użyjemy biblioteki [zlib](https://zlib.net). Jest to znana biblioteka open source, która implementuje algorytm Deflate. Cała napisana jest w języku C i takim stylu ma też interfejs, więc może on wydać się nieprzystępny dla programistów przyzwyczajonych do programowania obiektowego. Przyda się więc wyjaśnienie prawidłowego sposobu jego użycia.

Kod kompresujący dane znaleźć możemy w metodzie `PackingArchive::PackFileContent`

. W przypadku wyłączonej kompresji tworzy ona pojedynczy bufor w pamięci (o rozmiarze `kBufSize`

równym 64 KB), do którego po kawałku wczytuje dane z otwartego już pliku wejściowego i zapisuje je do wyjściowego pliku archiwum. W przypadku włączonej kompresji natomiast, odwołuje się do biblioteki zlib.

Aby skompresować dane w pamięci, należy:

`z_stream`

, która stanowi główną strukturę „kontekstu” dla algorytmu kompresji i zainicjalizować ją zerami.`deflateInit`

, która inicjalizuje tę strukturę, a więc niejako tworzy obiekt główny algorytmu.`src_buf`

, wskaźnik przypisany do pola `next_in`

struktury) i drugi na skompresowane dane wyjściowe (zmienna `dst_buf`

, wskaźnik przypisany do pola `next_out`

struktury).`deflateEnd`

, czym zajmuje się inteligentny wskaźnik wyposażony w niestandardowy Przez „wykonanie kompresji danych” rozumiemy natomiast kod, który w pętli wywołuje funkcję `deflate`

. Funkcja ta kompresuje fragment danych. Przesuwa przy tym wskaźnik `next_in`

i zmniejsza licznik `avail_in`

w strukturze o liczbę bajtów skonsumowanych na wejściu, a także przesuwa wskaźnik `next_out`

i zmniejsza licznik `avail_out`

o liczbę bajtów zapisanych na wyjściu. Nasz kod w pętli musi więc dodatkowo zrobić dwie rzeczy:

`deflate`

sprawdzamy, czy bufor wejściowy jest pusty. Jeżeli tak, wczytujemy nowe 64 KB danych do tego bufora (chyba, że wcześniej natrafiliśmy na koniec pliku wejściowego).Dekompresja działa w analogiczny sposób. Jej implementację znaleźć można w metodzie `ReadingArchive::UnpackFileContent`

. Używamy jedynie innych funkcji z biblioteki zlib – `inflateInit, inflate, inflateEnd`

. Bufor wejściowy dostarcza wówczas danych skompresowanych, a docelowy – zdekompresowanych.

Zauważmy, że w żadnym momencie nie przechowujemy jednocześnie w pamięci danych całego pliku, czy to skompresowanych, czy to nieskompresowanych. Operujemy tu raczej na „strumieniu” danych, wczytywanych i zapisywanych po kawałku. Dzięki temu nasz program może operować na dowolnie dużych plikach obojętnie, ile komputer posiada pamięci RAM.

Na początku artykułu zapoznaliśmy się z oknem Total Commandera, które pozwala dodać naszą wtyczkę (plik .wcx64) do obsługi wybranego rozszerzenia plików archiwum. Okazuje się jednak, że program ten oferuje wygodniejsze rozwiązanie do instalacji takich wtyczek. Oto, co musimy zrobić:

Wówczas użytkownik, kiedy tylko wejdzie do takiego archiwum ZIP, zobaczy komunikat o treści: *„This archive contains the following Total Commander plugin/addon: Sample Archive from Tutorial. Do you want to install it?”* Po potwierdzeniu wtyczka zostanie skopiowana do katalogu instalacyjnego Total Commandera i zainstalowana w nim.

*Listing 2. Plik „pluginst.inf” dla instalatora wtyczki*

[plugininstall] description=Sample Archive from Tutorial type=wcx file=SampleArchive.wcx64 defaultdir=SampleArchive defaultextension=smpa

W artykule tym poznaliśmy Total Commander jako wygodną aplikację do zarządzania plikami w systemie Windows. Nauczyliśmy się pisać wtyczkę typu Packer Plugin (WCX) w języku C++, która pozwala mu obsługiwać nowe formaty archiwum. Dzięki niej można pakować i kompresować wiele plików i katalogów do jednego pliku. Zaprojektowaliśmy przy tym własny, prosty format tego rodzaju. Dodatkiem do artykułu jest przykładowy kod, który można znaleźć w repozytorium GitHub: [ sawickiap/TotalCommanderPluginTutorial](https://github.com/sawickiap/TotalCommanderPluginTutorial).

Ta wiedza może się przydać do stworzenia własnego, zoptymalizowanego i dostosowanego do potrzeb formatu archiwum lub do napisania wtyczki, która doda do Total Commandera obsługę jakiegoś istniejącego formatu. Tym formatem wcale nie musi być odpowiednik ZIP czy 7Z! Możemy przecież wyobrazić sobie możliwość „wchodzenia” do plików EXE, DLL (to akurat Total Commander już potrafi) czy dowolnych innych binarnych formatów i oferowanie przeglądania zawartych w nich różnego rodzaju danych (zasobów) w postaci „wirtualnych” plików i podkatalogów.

Na koniec warto zwrócić uwagę na fakt, jak wiele funkcji Total Commander dodaje i obsługuje sam, bez naszej interwencji, a które czynią manipulowanie plikami archiwów prawie tak wygodnym, jak nawigację po zwykłych katalogach na dysku. Na przykład kod z rozdziału „Odczyt archiwum” automatycznie daje możliwość nie tylko przeglądania i rozpakowywania plików, ale także ich przeszukiwania (po nazwie lub pełnotekstowo po treści) oraz podglądania klawiszem F3 (w tym celu plik zostaje wypakowany do katalogu tymczasowego). Podobnie, podczas pakowania czy rozpakowywania, aplikacja sama pyta użytkownika, czy zastąpić istniejący plik.

Na tym kończy się opis naszej implementacji przykładowej wtyczki WCX do Total Commandera, ale nie kończą się możliwości takich wtyczek. Istnieje kilka funkcji, których nie zaimplementowaliśmy. O ile dodanie wersji 32-bitowej pliku DLL nie wydaje się w dzisiejszych czasach potrzebne, o tyle przydatne może być dodanie obsługi funkcji takich, jak:

`PK_TEST`

).`PK_CAPS_OPTIONS`

, eksportowana funkcja `ConfigurePacker`

).`PackSetDefaultParams`

).`PK_CAPS_ENCRYPT`

).`SetChangeVolProc`

, callback `tChangeVolProc`

).
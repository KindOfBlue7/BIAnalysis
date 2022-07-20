# BIAnalysis
Repozytorium zawierające kod do własnego tworzenia analiz
z plików wygenerowanych przez analizator bioimpedancyjny.

## Instalacja

```bash
git clone github.com/KindOfBlue7/BIAnalysis/master
```

## Użycie
Analizy generuje się poprzez wywołanie głównego skryptu (tj. main.py) z poziomu
głównego folderu repozytorium i jako argument wywołania podać scieżkę
do pliku z danymi.

```bash
python3 main.py data/dawid-0077.mfu
```

Można modyfikować plik main.py, aby np. dodać generowanie wykresu Cole'a, wystarczy wtedy
dodać oprócz print_summary() np.

```python
bia.plot_cole()
```

lub dodatkowo z wyznaczonym promieniem

```python
bia.plot_cole_with_radius()
```

Cały kod jest otwarty, więc można samemu dodawać swoje własne nowe funkcjonalności.
 

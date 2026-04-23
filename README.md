# Financial Risk Analysis App

Aplikacja do analizy ryzyka instrumentow finansowych na podstawie danych z Yahoo Finance przy użyciu biblioteki streamlit.

## Funkcjonalnosci

- Pobieranie cen zamkniecia z Yahoo Finance.
- Obsluga wielu tickerow jednoczesnie.
- Wybieralny interwal danych w panelu bocznym:
  - `1d` (dzienny)
  - `1wk` (tygodniowy)
  - `1mo` (miesieczny)
- Obliczanie logarytmicznych stop zwrotu.
- Wykresy cen i stop zwrotu.
- Statystyki opisowe aktywow.
- Histogramy stop zwrotu z benchmarkiem i dopasowaniem rozkladow.
- Historyczny VaR.
- Monte Carlo: symulacje sciezek i VaR Monte Carlo.

## Wymagania dot. tickerow

Podawaj tickery w formacie Yahoo Finance, np.:

- `CDR.WA`
- `AAPL`
- `^GSPC`
- `^GDAXI`

W aplikacji wyswietlana jest przypominajaca notatka o tym formacie.

## Struktura plikow

- `app.py` - glowna aplikacja Streamlit (UI i sterowanie analiza).
- `data_loader.py` - pobieranie danych z Yahoo Finance i przygotowanie cen.
- `asset.py` - klasa `Asset` (ceny i logarytmiczne stopy zwrotu).
- `analytics.py` - statystyki i histogramy z dopasowaniem rozkladow.
- `risk.py` - metody VaR i symulacje Monte Carlo.
- `plots.py` - funkcje rysujace wykresy.

## Instalacja i uruchomienie

1. Zainstaluj zaleznosci:

```bash
pip install -r requirements.txt
```

2. Uruchom aplikacje:

```bash
streamlit run app.py
```

## Jak uzywac

1. W panelu bocznym wpisz tickery (oddzielone przecinkami).
2. Ustaw zakres dat.
3. Wybierz interwal danych Yahoo (`1d`, `1wk`, `1mo`).
4. Ustaw parametry ryzyka (`alpha`, liczba dni i sciezek Monte Carlo).
5. Kliknij `Uruchom analize`.

## Uwagi

- Dla niektorych tickerow lub zakresow dat Yahoo Finance moze zwrocic niepelne dane.
- Interwaly sa mapowane na czestotliwosci wykorzystywane wewnatrz aplikacji (`WD`, `1W`, `ME`).

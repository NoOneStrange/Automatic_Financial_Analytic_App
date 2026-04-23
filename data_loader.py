import pandas as pd
import yfinance as yf

FREQ_WORKING_DAYS = 'WD'

def load_prices(tickers, start, end, freq=FREQ_WORKING_DAYS):
    """
    Wczytuje dane cenowe z serwisu Yahoo Finance dla listy tickerów.

    Parametry:
    - tickers: lista symboli (np. ['AAPL.US', 'MSFT.US'])
    - start, end: zakres dat
    - freq:
        'WD'  -> sesje giełdowe (bez dodatkowego resamplingu)
        inne  -> resampling do zadanej częstotliwości

    Zwraca:
    - DataFrame z cenami zamknięcia
    """

    freqs = (FREQ_WORKING_DAYS, '1W', '2W', '3W', 'ME', '2M')
    if freq not in freqs:
        raise ValueError(f'Nieobsługiwany interwał: {freq}, użyj np. {freqs}')

    yahoo_tickers = [t.strip().upper() for t in tickers]

    df = yf.download(
        tickers=yahoo_tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        raise ValueError('Brak danych dla podanych tickerów i zakresu dat.')

    if isinstance(df.columns, pd.MultiIndex):
        close_df = df['Close'].copy()
    else:
        close_df = df[['Close']].rename(columns={'Close': yahoo_tickers[0]})

    # Przywracamy nazwy kolumn zgodne z wejściem użytkownika.
    rename_map = dict(zip(yahoo_tickers, [t.strip().lower() for t in tickers]))
    close_df = close_df.rename(columns=rename_map)

    close_df = close_df.ffill().dropna()

    if freq == FREQ_WORKING_DAYS:
        return close_df

    return close_df.resample(freq).last().dropna()
    
def get_default_benchmark(ticker):
    """
    Zwraca domyślny benchmark rynkowy dla danego instrumentu.
    """
    ticker = ticker.lower()

    if ticker.endswith(""):
        return "^gspc" 
    elif ticker.endswith(".de"):
        return "^gdaxi"
    else:
        return "wig.wa"
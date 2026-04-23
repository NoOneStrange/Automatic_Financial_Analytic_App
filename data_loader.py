import pandas as pd
import yfinance as yf

FREQ_WORKING_DAYS = 'WD'


def _download_close_series(yahoo_symbol, start, end):
    """Pobiera serię cen zamknięcia dla pojedynczego symbolu Yahoo."""
    df = yf.download(
        tickers=yahoo_symbol,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        if 'Close' not in df.columns.levels[0]:
            return None
        close_series = df['Close'].squeeze()
    else:
        if 'Close' not in df.columns:
            return None
        close_series = df['Close']

    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]

    return close_series.dropna()


def _benchmark_candidates(symbol):
    symbol_upper = symbol.strip().upper()

    benchmark_fallbacks = {
        '^WIG': ['^WIG', '^WIG20', '^GSPC'],
        '^WIG20': ['^WIG20', '^WIG', '^GSPC'],
        '^GDAXI': ['^GDAXI', '^GSPC'],
        '^GSPC': ['^GSPC']
    }

    return benchmark_fallbacks.get(symbol_upper, [symbol_upper])


def _load_ticker_with_fallbacks(ticker, start, end):
    requested = ticker.strip()
    for candidate in _benchmark_candidates(requested):
        series = _download_close_series(candidate, start, end)
        if series is not None and not series.empty:
            return series.rename(requested)

    raise ValueError(f'Brak danych dla tickera: {requested}')


def working_days(start, end):
    """
    Zwraca indeks dni sesyjnych na podstawie benchmarku rynkowego.
    """
    for calendar_symbol in ('^WIG20', '^GSPC'):
        series = _download_close_series(calendar_symbol, start, end)
        if series is not None and not series.empty:
            return pd.DataFrame(index=series.index)

    # Awaryjnie: dni robocze (pon-pt), gdy Yahoo nie zwróci danych indeksu.
    return pd.DataFrame(index=pd.bdate_range(start=start, end=end))


def all_days(start, end):
    """
    Zwraca indeks wszystkich dni kalendarzowych w zadanym okresie.
    """
    return pd.DataFrame(index=pd.date_range(start=start, end=end, freq='D'))

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

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    if freq == FREQ_WORKING_DAYS:
        df_merged = working_days(start, end)
    else:
        df_merged = all_days(start, end)

    for ticker in [t.strip() for t in tickers]:
        close_series = _load_ticker_with_fallbacks(ticker, start, end)
        close_df = close_series.to_frame().truncate(before=start, after=end)

        df_merged = pd.merge(
            left=df_merged,
            right=close_df,
            how='left',
            left_index=True,
            right_index=True
        )

    df_merged = df_merged.ffill().dropna()

    if freq == FREQ_WORKING_DAYS:
        return df_merged

    return df_merged.asfreq(freq)
    
def get_default_benchmark(ticker):
    """
    Zwraca domyślny benchmark rynkowy dla danego instrumentu.
    """
    ticker = ticker.lower()

    if ticker.endswith(".wa"):
        return "^wig"
    elif ticker.endswith(".us"):
        return "^gspc"
    elif ticker.endswith(".de"):
        return "^gdaxi"
    else:
        return "^gspc"
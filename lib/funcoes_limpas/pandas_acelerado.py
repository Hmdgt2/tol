
try:
    import modin.pandas as mpd
    MODIN_AVAILABLE = True
except ImportError:
    MODIN_AVAILABLE = False
from typing import List, Dict


def _modin_correlation_analysis(df):
    'Análise de correlação paralelizada.'
    try:
        df['squared'] = (df['values'] ** 2)
        df['lag1'] = df['values'].shift(1)
        corr_matrix = df.corr()
        return corr_matrix.to_dict()
    except:
        return {'correlation': 'insufficient_data'}


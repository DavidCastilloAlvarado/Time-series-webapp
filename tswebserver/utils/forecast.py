import pandas as pd
import numpy as np

from sklearn.metrics import r2_score

from sklearn import linear_model

from statsmodels.tsa.stattools import adfuller

import statsmodels.api as sm
import datetime


class ForecastTask:
    def __init__(self,):
        self.table = pd.read_csv("tswebserver/utils/database/tsbyproduct.csv", index_col="Periodo")
        self.articulos = pd.read_csv("tswebserver/utils/database/articulos.csv")
    
    def forecast(self, id_articulo, ahead, before=12):
        mod = sm.tsa.statespace.SARIMAX(self.table[id_articulo], order=(1, 1, 0), seasonal_order=(2, 1, 0, 12),freq='MS')
        mod_trained = mod.fit(disp=False)
        before = self.table[id_articulo].tail(before)
        before = dict(
            before_index = before.index.tolist(),
            before_val = before.tolist()
        )
        return before, mod_trained.forecast(steps=ahead)
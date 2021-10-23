import pandas as pd
import numpy as np

from sklearn.metrics import r2_score

from sklearn import linear_model

from statsmodels.tsa.stattools import adfuller

import statsmodels.api as sm
from dateutil.relativedelta import relativedelta
from datetime import datetime

class BasketAnalysis:
    def __init__(self,):
        self.table = pd.read_csv("tswebserver/utils/database/basket_analysis.csv",)

    def get_items_related(self, idArticulo):
        return self.table.query(f"antecedents=={idArticulo}")['idArticulo'].tolist()

class ForecastTask:
    def __init__(self,):
        self.table = pd.read_csv("tswebserver/utils/database/tsbyproduct.csv", index_col="Periodo")
        self.articulos = pd.read_csv("tswebserver/utils/database/articulos.csv")
        self.articulos.drop_duplicates(subset=['idArticulo'], inplace=True)
    
    def forecast(self, id_articulo, ahead, before=12):
        mod = sm.tsa.statespace.SARIMAX(self.table[id_articulo], order=(1, 1, 0), seasonal_order=(2, 1, 0, 12),freq='MS')
        mod_trained = mod.fit(disp=False)
        before = self.table[id_articulo].tail(before)
        name = self.articulos.query(f"idArticulo=={id_articulo}")["DescProducto"].tolist()[0]
        return self.format_output(before, mod_trained, ahead) , ahead, name

    @staticmethod
    def format_output(before, model, n_ahead):
        forecast_vals = model.forecast(steps=n_ahead)
        before_index = before.index.tolist()
        before_val = before.tolist() + forecast_vals.tolist()

        for _ in range(n_ahead):
            finalmonth = datetime.strptime(str(before_index[-1]), '%Y-%m-%d').date()
            # finalmonth = before_index[-1]
            datefut = finalmonth + relativedelta(months = 1)
            before_index.append(datefut)

        return dict(
            labels = before_index,
            values = before_val
        )


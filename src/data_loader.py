import pandas as pd
import numpy as np


class DataLoader:
    def load_data(path):
        data = pd.read_excel(path, index_col=0)
        data = DataLoader._convert_to_float(data)
        data = DataLoader._nan_removing(data)
        return data

    def _convert_to_float(data):
        return data.applymap(lambda x: pd.to_numeric(x, errors="coerce"))

    def _nan_removing(data):
        return data.replace("-", np.nan)

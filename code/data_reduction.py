from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
import numpy as np


def pca_reducer(values, ncomponents=6):
    scaler = MinMaxScaler()
    normalized = scaler.fit_transform(values)
    pca = PCA(n_components=ncomponents)
    pca.fit(normalized)
    return pca.transform(normalized)

def pls_reducer(values, y, ncomponents=6):
    scaler = MinMaxScaler()
    normalized_values = scaler.fit_transform(values)
    pls = PLSRegression(n_components=ncomponents)
    pls.fit(normalized_values, y)
    return pls.transform(normalized_values)
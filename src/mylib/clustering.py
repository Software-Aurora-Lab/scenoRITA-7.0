from pathlib import Path

import numpy as np
import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler


def cluster_df(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) == 1:
        df["cluster"] = 1
        return df
    data = df.iloc[:, 1:]  # remove the first column
    data_scaled = MinMaxScaler().fit_transform(data)
    knn = NearestNeighbors(n_neighbors=2)
    neighbors = knn.fit(data_scaled)
    distances, _ = neighbors.kneighbors(data_scaled)
    sorted_distances = np.sort(distances, axis=0)[:, 1]

    i = np.arange(len(sorted_distances))
    knee = KneeLocator(
        i,
        sorted_distances,
        S=1.00,
        curve="convex",
        direction="increasing",
    )
    if knee.knee:
        epsilon = sorted_distances[knee.knee]
    else:
        epsilon = sorted_distances[round(len(sorted_distances) / 2)]

    est = DBSCAN(eps=epsilon, min_samples=1, metric="euclidean")
    clusters = est.fit_predict(data_scaled)

    df["cluster"] = clusters
    df.sort_values("cluster", inplace=True)

    return df


def cluster(filename: Path) -> pd.DataFrame:
    df = pd.read_csv(filename)
    return cluster_df(df)

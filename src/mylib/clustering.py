from pathlib import Path

import numpy as np
import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler


def cluster(filename: Path) -> np.ndarray:
    df = pd.read_csv(filename)
    data = df.iloc[:, 1:]  # remove the first column
    data_scaled = MinMaxScaler().fit_transform(data)
    knn = NearestNeighbors(n_neighbors=2)
    neighbors = knn.fit(data_scaled)
    distances, _ = neighbors.kneighbors(data_scaled)
    sorted_distances = np.sort(distances, axis=0)[:, 1]

    i = np.arange(len(sorted_distances))
    knee = KneeLocator(i, sorted_distances, S=1, curve="convex", direction="increasing")
    if knee.knee:
        epsilon = sorted_distances[knee.knee]
    else:
        epsilon = sorted_distances[round(len(sorted_distances) / 2)]

    est = DBSCAN(eps=epsilon, min_samples=1, metric="cityblock")
    clusters = est.fit_predict(data_scaled)

    df["cluster"] = clusters
    df.sort_values("cluster", inplace=True)
    print(df)

    return clusters


if __name__ == "__main__":
    filename = Path("/Users/yuqihuai/Downloads/_UnsafeLaneChange.csv")
    clusters = cluster(filename)

    num_violations = len(clusters)
    num_clusters = len(np.unique(clusters))

    print(f"Number of violations: {num_violations}")
    print(f"Number of clusters: {num_clusters}")
    eliminated = num_violations - num_clusters
    print(f"Elimination ratio: {eliminated / num_violations * 100:.2f}%")

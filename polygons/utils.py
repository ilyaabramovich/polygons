from os import path

import numpy as np
import pandas as pd


def area(coords):
    x, y = zip(*coords)
    return 0.5 * np.abs(np.dot(x[:-1], y[1:]) + x[-1]*y[0] -
                        np.dot(y[:-1], x[1:]) - y[-1]*x[0])


def dist(point1, point2):
    return np.linalg.norm(np.subtract(point2, point1))


def split_point(triangle, area):
    p1, p2, p3 = triangle
    k = p2[0]*(p1[1]-p3[1]) + p1[0]*(p3[1]-p2[1]) + p3[0]*(p2[1]-p1[1])
    x = (2*area*(p3[0]-p2[0])+p2[0]*k) / k
    y = (p2[1]-p3[1])*(x-p3[0])/(p2[0]-p3[0]) + p3[1]
    return (x, y)


def read_polygon(filename):
    data = pd.read_csv(filename, sep=';', decimal=',')
    return data.astype({"x": float, "y": float})


def coords(dataframe, inverse=False):
    columns = ["x", "y"]
    if inverse:
        columns.reverse()
    coords = dataframe[columns].values.tolist()
    return coords


def transform_coords(coords, start, stop):
    basis = dist(start, stop)
    cos, sin = np.divide(np.subtract(stop, start), basis)
    transform_matrix = np.array([[cos, sin], [-sin, cos]])

    transformed = [np.matmul(transform_matrix, np.subtract(
        point, start)).tolist() for point in coords]
    return transformed


def to_csv(data, path):
    data.to_csv(path, index=False, sep=';')


def list_to_csv(elements, output_dir):
    for i, e in enumerate(elements):
        to_csv(e, path.join(output_dir, "file_{}.csv".format(i)))

import numpy as np
import pandas as pd
from .utils import (split_point, dist, coords, area)


class MyPolygon:
    def __init__(self, data, inverse=False):
        self.data = data
        self.coords = coords(self.data, inverse)
        self.area = area(self.coords)

    def get_coords(self):
        return self.coords

    def get_area(self):
        return self.area

    def get_data(self):
        return self.data

    @staticmethod
    def split(coords, startIndex=0):
        triangles = [[coords[startIndex], *coords[i:i+2]]
                     for i in range(len(coords)-2)]
        areas = {i: area(
            triangle) for i, triangle in enumerate(triangles)}

        half_area = area(coords)*0.5
        current_area = 0
        index = -1

        while(current_area < half_area):
            index += 1
            current_area += areas.get(index)

        triangle_area = areas.get(index) - (current_area-half_area)
        splitting_point = split_point(
            triangles[index], triangle_area)
        new_coords = coords[:]
        new_coords.insert(index+1, splitting_point)
        return (new_coords, coords[startIndex], splitting_point)

    def smooth(self, status):
        start_row = self.data[self.data.status.eq("start")]
        stop_row = self.data[self.data.status.eq("stop")]
        start = start_row[["x", "y"]].values[0]
        stop = stop_row[["x", "y"]].values[0]
        x_start, y_start = start
        x_stop, y_stop = stop
        # data for new square
        new_data = self.data[self.data.status.ne('+')]
        new_coords = coords(new_data)

        # difference of squares
        diff_area = self.area-area(new_coords)

        # def - для локальной СК, чтобы сразу считать
        basis = dist(start, stop)
        cos = (y_stop - y_start)/basis
        sin = (x_stop - x_start)/basis
        h = 2*diff_area/basis

        part = self.data.dropna()
        len_part = len(part)

        # Точки сглаживания в локальной СК.
        # По значению y_l_NEW можно понять, где входит H.
        dict_x = []
        dict_y = []
        for i in range(len_part):
            x = part.iloc[i, 1]
            y = part.iloc[i, 2]
            x_new = (y - y_start)*cos + (x - x_start)*sin
            y_new = -(y - y_start)*sin + (x - x_start)*cos
            dict_x.append(x_new)
            dict_y.append(y_new)

        # Вхождение высоты в конкретный интервал
        dict_ins = []
        for k in range(len_part - 1):
            if (h < 0 and ((h <= dict_y[k] and h >= dict_y[k+1])
                           or (h >= dict_y[k] and h <= dict_y[k+1]))):
                s = [k, k+1]
                dict_ins.append(s)
            elif (h > 0 and ((h >= dict_y[k] and h <= dict_y[k+1])
                             or (h <= dict_y[k] and h >= dict_y[k+1]))):

                s = [k, k+1]
                dict_ins.append(s)

        # Функция для определения пересечения высоты
        new_data1 = self.data[self.data.status.isnull()]
        variants = []
        for i, point in enumerate(dict_ins):
            x_k = dict_x[point[0]]
            y_k = dict_y[point[0]]
            x_k_1 = dict_x[point[1]]
            y_k_1 = dict_y[point[1]]
            x_h = (h - y_k)*(x_k_1 - x_k)/(y_k_1 - y_k) + x_k
            y_h_main = x_h*cos - h*sin + y_start
            x_h_main = x_h*sin + h*cos + x_start
            new_row = pd.DataFrame(
                [[status + i, x_h_main, y_h_main, 'new']], columns=self.data.columns)
            df = pd.concat([start_row, new_row, stop_row,
                            new_data1], ignore_index=True)
            variants.append(df)

        return variants

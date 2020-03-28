from os import path
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from .Polygon import MyPolygon
from .utils import (list_to_csv, transform_coords, read_polygon, split)


def main(filename, road_width):
    output_dir = "variants"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    data = read_polygon(filename)
    polygon = MyPolygon(data)
    variants = polygon.smooth(status=900)
    list_to_csv(variants, output_dir)

    new_output_dir = output_dir+"_2"
    file_smooth = path.join(new_output_dir, "file_31.csv")
    data_smoothed = read_polygon(file_smooth)
    polygon_smoothed = MyPolygon(data_smoothed)
    variants2 = polygon_smoothed.smooth(status=500)
    list_to_csv(variants2, new_output_dir)

    polygon_final = MyPolygon(variants2[0], inverse=True)
    polygon_new, start, stop = polygon_final.split()
    coords_new = transform_coords(polygon_new, start, stop)
    index_start = polygon_new.index(start)
    index_stop = polygon_new.index(stop)
    start_new = coords_new[index_start]
    stop_new = coords_new[index_stop]

    x_1 = stop_new[0]
    x_a, y_a = coords_new[index_start-1]
    x_b, y_b = coords_new[index_start+1]
    x_c, y_c = coords_new[index_stop-1]
    x_d, y_d = coords_new[index_stop+1]

    h = (((-2*x_1*y_a*y_b*y_c+2*x_1*y_a*y_b*y_d-24*x_a*y_b*y_c+24*x_a*y_b*y_d+2*x_c*y_a*y_b*y_d+24*x_c*y_a*y_b-2*x_d*y_a*y_b*y_c-24*x_d*y_a*y_b)**2
          - 4*(road_width*x_1*y_a*y_b*y_c-road_width*x_1*y_a*y_b*y_d+144*x_a*y_b*y_c-144*x_a*y_b*y_d-road_width*x_c*y_a*y_b*y_d-144*x_c*y_a*y_b+road_width*x_d*y_a*y_b*y_c
               + 144*x_d*y_a*y_b)*(x_a * y_b*y_c-x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))**0.5
         + 2*x_1*y_a*y_b*y_c-2*x_1*y_a*y_b*y_d+24*x_a*y_b*y_c-24*x_a*y_b*y_d-2*x_c*y_a*y_b*y_d-24*x_c*y_a*y_b+2*x_d*y_a*y_b*y_c+24*x_d*y_a*y_b)/(2*(x_a*y_b*y_c
                                                                                                                                                    - x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))
    h2 = (-((-2*x_1*y_a*y_b*y_c+2*x_1*y_a*y_b*y_d-24*x_a*y_b*y_c+24*x_a*y_b*y_d+2*x_c*y_a*y_b*y_d+24*x_c*y_a*y_b-2*x_d*y_a*y_b*y_c-24*x_d*y_a*y_b)**2
            - 4*(road_width*x_1*y_a*y_b*y_c-road_width*x_1*y_a*y_b*y_d+144*x_a*y_b*y_c-144*x_a*y_b*y_d-road_width*x_c*y_a*y_b*y_d-144*x_c*y_a*y_b+road_width*x_d*y_a*y_b*y_c
                 + 144*x_d*y_a*y_b)*(x_a * y_b*y_c-x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))**0.5
          + 2*x_1*y_a*y_b*y_c-2*x_1*y_a*y_b*y_d+24*x_a*y_b*y_c-24*x_a*y_b*y_d-2*x_c*y_a*y_b*y_d-24*x_c*y_a*y_b+2*x_d*y_a*y_b*y_c+24*x_d*y_a*y_b)/(2*(x_a*y_b*y_c
                                                                                                                                                     - x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))

    x_2 = h*x_b/y_b
    x_3 = (h-y_d)*(x_c-x_d)/(y_c-y_d)+x_d
    x_4 = (h-road_width-y_d)*(x_c-x_d)/(y_c-y_d)+x_d
    x_5 = (h-road_width)*x_a/y_a

    mid_top = (x_2+x_3)*0.5
    polygon_top = [[mid_top, h], [x_2, h], *
                   coords_new[index_start+1:index_stop], [x_3, h]]
    polygon_new_top, start_top, stop_top = split(polygon_top)
    polygon_new_top_1 = polygon_new_top[:polygon_new_top.index(
        stop_top)+1]
    polygon_new_top_2 = [*polygon_new_top[polygon_new_top.index(
        stop_top):], polygon_new_top[0]]

    mid_bottom = (x_5+x_4)/2
    polygon_bottom = [[mid_bottom, h-road_width], [x_4, h-road_width], *
                      coords_new[index_stop+1:], [x_5, h-road_width]]

    polygon_new_bottom, start_bottom, stop_bottom = split(
        polygon_bottom)

    polygon_new_bottom_1 = polygon_new_bottom[:polygon_new_bottom.index(
        stop_bottom)+1]

    polygon_new_bottom_2 = [*polygon_new_bottom[polygon_new_bottom.index(
        stop_bottom):], polygon_new_bottom[0]]

    road_top = [[x_3, h], stop_new,
                start_new, [x_2, h]]
    road_bottom = [stop_new, [x_4, h-road_width],
                   [x_5, h-road_width], start_new]

    polygons_result = [coords_new, polygon_new_top_1, polygon_new_top_2,
                       polygon_new_bottom_1, polygon_new_bottom_2, road_top, road_bottom]

    cut_points = [polygon_top[0], polygon_bottom[0],
                  stop_bottom, stop_top, [x_2, h], [x_3, h], [x_4, h-road_width], [x_5, h-road_width]]

    mpl.rcParams['patch.facecolor'] = 'none'

    fig, ax = plt.subplots(2)
    polygon = Polygon(polygon_new, ec="grey")
    ax[0].add_patch(polygon)
    ax[0].plot(*zip(start, stop), "--")
    ax[0].scatter(*zip(*polygon_new))

    patches = []
    for coords in polygons_result[:-2]:
        polygon = Polygon(coords)
        patches.append(polygon)
    colors = ["grey", "green", "red", "cyan", "magenta"]
    p = PatchCollection(patches, ec=colors)

    ax[1].add_collection(p)
    ax[1].plot(*zip(start_new, stop_new), "--")
    ax[1].scatter(*zip(*cut_points))
    plt.show()

from .utils import (get_coords, read_polygon, smooth, get_area,
                    split, transform_coords, dist, list_to_csv)
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from pathlib import Path
from os import path


def main(filename, road_width):
    output_dir = "variants"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    data = read_polygon(filename)
    variants = smooth(data=data, status=900)
    list_to_csv(variants, output_dir)

    new_output_dir = output_dir+"_2"
    smooth_file = path.join(new_output_dir, "file_31.csv")
    smoothed_polygon = read_polygon(smooth_file)
    variants2 = smooth(data=smoothed_polygon, status=500)
    list_to_csv(variants2, new_output_dir)

    final_polygon = variants2[0]
    coords = get_coords(final_polygon, inverse=True)
    new_polygon, start, stop = split(coords)
    new_coords = transform_coords(new_polygon, start, stop)
    start_index = new_polygon.index(start)
    stop_index = new_polygon.index(stop)
    new_start = new_coords[start_index]
    new_stop = new_coords[stop_index]

    x_1 = new_stop[0]
    x_a, y_a = new_coords[start_index-1]
    x_b, y_b = new_coords[start_index+1]
    x_c, y_c = new_coords[stop_index-1]
    x_d, y_d = new_coords[stop_index+1]

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
    top_polygon = [[mid_top, h], [x_2, h], *
                   new_coords[start_index+1:stop_index], [x_3, h]]
    new_polygon_top, start_top, stop_top = split(top_polygon)
    new_polygon_top_1 = new_polygon_top[:new_polygon_top.index(
        stop_top)+1]
    new_polygon_top_2 = [*new_polygon_top[new_polygon_top.index(
        stop_top):], new_polygon_top[0]]

    mid_bottom = (x_5+x_4)/2
    bottom_polygon = [[mid_bottom, h-road_width], [x_4, h-road_width], *
                      new_coords[stop_index+1:], [x_5, h-road_width]]

    new_polygon_bottom, start_bottom, stop_bottom = split(
        bottom_polygon)

    new_polygon_bottom_1 = new_polygon_bottom[:new_polygon_bottom.index(
        stop_bottom)+1]

    new_polygon_bottom_2 = [*new_polygon_bottom[new_polygon_bottom.index(
        stop_bottom):], new_polygon_bottom[0]]

    road_top = [[x_3, h], new_stop,
                new_start, [x_2, h]]
    road_bottom = [new_stop, [x_4, h-road_width],
                   [x_5, h-road_width], new_start]

    result_polygons = [new_coords, new_polygon_top_1, new_polygon_top_2,
                       new_polygon_bottom_1, new_polygon_bottom_2, road_top, road_bottom]

    cut_points = [top_polygon[0], bottom_polygon[0],
                  stop_bottom, stop_top, [x_2, h], [x_3, h], [x_4, h-road_width], [x_5, h-road_width]]

    fig, ax = plt.subplots(2)
    polygon = Polygon(new_polygon, fc="none", ec="grey")
    ax[0].add_patch(polygon)
    ax[0].plot(*zip(start, stop), "--")
    ax[0].scatter(*zip(*new_polygon))

    patches = []
    for coords in result_polygons[:-2]:
        polygon = Polygon(coords)
        patches.append(polygon)
    colors = ["grey", "green", "red", "cyan", "magenta"]
    p = PatchCollection(patches, fc="none", ec=colors)

    ax[1].add_collection(p)
    ax[1].plot(*zip(new_start, new_stop), "--")
    ax[1].scatter(*zip(*cut_points))
    plt.show()

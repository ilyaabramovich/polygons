from .utils import (get_polygon_coords, read_polygon_data, smooth_polygon, area_by_shoelace,
                    split_polygon, transform_coordinates, dist)
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from pathlib import Path
from os import path


def main(args):
    ROAD_WIDTH = 12
    output_dir = "variants"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    polygon = read_polygon_data(args)
    smooth_polygon(data=polygon, status=900, output_dir=output_dir)
    new_output_dir = output_dir+"_2"
    smooth_polygon_file = path.join(new_output_dir, "file_31.csv")
    smoothed_polygon = read_polygon_data(smooth_polygon_file)

    smooth_polygon(data=smoothed_polygon, status=500,
                   output_dir=new_output_dir)
    final_polygon = path.join(new_output_dir, "file_0.csv")

    dataframe = read_polygon_data(final_polygon)
    coords = get_polygon_coords(dataframe, inverse=True)
    new_polygon, split_line = split_polygon(coords)
    start, stop = split_line
    new_coords = transform_coordinates(new_polygon, start, stop)
    start_index = new_polygon.index(start)
    stop_index = new_polygon.index(stop)
    new_split_line = [new_coords[start_index],
                      new_coords[stop_index]]
    new_start, new_stop = new_split_line

    x_1 = new_stop[0]
    x_a, y_a = new_coords[start_index-1]
    x_b, y_b = new_coords[start_index+1]
    x_c, y_c = new_coords[stop_index-1]
    x_d, y_d = new_coords[stop_index+1]

    h = (((-2*x_1*y_a*y_b*y_c+2*x_1*y_a*y_b*y_d-24*x_a*y_b*y_c+24*x_a*y_b*y_d+2*x_c*y_a*y_b*y_d+24*x_c*y_a*y_b-2*x_d*y_a*y_b*y_c-24*x_d*y_a*y_b)**2
          - 4*(ROAD_WIDTH*x_1*y_a*y_b*y_c-ROAD_WIDTH*x_1*y_a*y_b*y_d+144*x_a*y_b*y_c-144*x_a*y_b*y_d-ROAD_WIDTH*x_c*y_a*y_b*y_d-144*x_c*y_a*y_b+ROAD_WIDTH*x_d*y_a*y_b*y_c
               + 144*x_d*y_a*y_b)*(x_a * y_b*y_c-x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))**0.5
         + 2*x_1*y_a*y_b*y_c-2*x_1*y_a*y_b*y_d+24*x_a*y_b*y_c-24*x_a*y_b*y_d-2*x_c*y_a*y_b*y_d-24*x_c*y_a*y_b+2*x_d*y_a*y_b*y_c+24*x_d*y_a*y_b)/(2*(x_a*y_b*y_c
                                                                                                                                                    - x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))
    h2 = (-((-2*x_1*y_a*y_b*y_c+2*x_1*y_a*y_b*y_d-24*x_a*y_b*y_c+24*x_a*y_b*y_d+2*x_c*y_a*y_b*y_d+24*x_c*y_a*y_b-2*x_d*y_a*y_b*y_c-24*x_d*y_a*y_b)**2
            - 4*(ROAD_WIDTH*x_1*y_a*y_b*y_c-ROAD_WIDTH*x_1*y_a*y_b*y_d+144*x_a*y_b*y_c-144*x_a*y_b*y_d-ROAD_WIDTH*x_c*y_a*y_b*y_d-144*x_c*y_a*y_b+ROAD_WIDTH*x_d*y_a*y_b*y_c
                 + 144*x_d*y_a*y_b)*(x_a * y_b*y_c-x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))**0.5
          + 2*x_1*y_a*y_b*y_c-2*x_1*y_a*y_b*y_d+24*x_a*y_b*y_c-24*x_a*y_b*y_d-2*x_c*y_a*y_b*y_d-24*x_c*y_a*y_b+2*x_d*y_a*y_b*y_c+24*x_d*y_a*y_b)/(2*(x_a*y_b*y_c
                                                                                                                                                     - x_a*y_b*y_d+x_b*y_a*y_c-x_b*y_a*y_d-2*x_c*y_a*y_b+2*x_d*y_a*y_b))

    x_2 = h*x_b/y_b
    x_3 = (h-y_d)*(x_c-x_d)/(y_c-y_d)+x_d
    x_4 = (h-ROAD_WIDTH-y_d)*(x_c-x_d)/(y_c-y_d)+x_d
    x_5 = (h-ROAD_WIDTH)*x_a/y_a

    mid_top = (x_3+x_2)/2
    top_polygon = [[mid_top, h], [x_2, h], *
                   new_coords[start_index+1:stop_index], [x_3, h]]
    new_polygon_top, split_line_top = split_polygon(top_polygon)
    new_polygon_top_1 = new_polygon_top[:new_polygon_top.index(
        split_line_top[1])+1]
    new_polygon_top_2 = [*new_polygon_top[new_polygon_top.index(
        split_line_top[1]):], new_polygon_top[0]]

    mid_bottom = (x_5+x_4)/2
    bottom_polygon = [[mid_bottom, h-ROAD_WIDTH], [x_4, h-ROAD_WIDTH], *
                      new_coords[stop_index+1:], [x_5, h-ROAD_WIDTH]]

    new_polygon_bottom, split_line_bottom = split_polygon(bottom_polygon)

    new_polygon_bottom_1 = new_polygon_bottom[:new_polygon_bottom.index(
        split_line_bottom[1])+1]

    new_polygon_bottom_2 = [*new_polygon_bottom[new_polygon_bottom.index(
        split_line_bottom[1]):], new_polygon_bottom[0]]

    road_top = [[x_3, h], new_stop,
                new_start, [x_2, h]]
    road_bottom = [new_stop, [x_4, h-ROAD_WIDTH],
                   [x_5, h-ROAD_WIDTH], new_start]

    result_polygons = [new_coords, new_polygon_top_1, new_polygon_top_2,
                       new_polygon_bottom_1, new_polygon_bottom_2, road_top, road_bottom]

    result_area = sum(
        map(lambda polygon: area_by_shoelace(polygon), result_polygons[1:]))
    print("initial total area: {}\nresult total area: {}".format(area_by_shoelace(coords), result_area)
          )

    cut_points = [top_polygon[0], bottom_polygon[0],
                  split_line_bottom[1], split_line_top[1], [x_2, h], [x_3, h], [x_4, h-ROAD_WIDTH], [x_5, h-ROAD_WIDTH]]

    fig, ax = plt.subplots(2)
    polygon = Polygon(new_polygon, fc="none", ec="grey")
    ax[0].add_patch(polygon)
    ax[0].plot(*zip(*split_line), "--")
    ax[0].scatter(*zip(*new_polygon))

    patches = []
    for coords in result_polygons[:-2]:
        polygon = Polygon(coords)
        patches.append(polygon)
    colors = ["grey", "green", "red", "cyan", "magenta"]
    p = PatchCollection(patches, fc="none", ec=colors)

    ax[1].add_collection(p)
    ax[1].plot(*zip(*new_split_line), "--")
    ax[1].scatter(*zip(*cut_points))
    plt.show()

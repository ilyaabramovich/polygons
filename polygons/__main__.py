from .core import main
import argparse


parser = argparse.ArgumentParser(description='Split polygons.')
parser.add_argument('filename', metavar="file.csv", type=argparse.FileType('r'),
                    help='Coordinates of polygon to split')

args = parser.parse_args()
main(args.filename)

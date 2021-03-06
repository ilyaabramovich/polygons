from .core import main
import argparse


parser = argparse.ArgumentParser(description='Split polygon into four equal parts considering road')
parser.add_argument('filename', metavar="file.csv", type=argparse.FileType('r'),
                    help='Coordinates of polygon to split')
parser.add_argument('--width', metavar="road_width", type=int,
                    help='Road width (default is 12)', default=12)
args = parser.parse_args()
main(args.filename, args.width)

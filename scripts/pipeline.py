import bpy, json, os, sys
from bpy import context
from copy import copy
from math import pi, cos, sin, degrees
from mathutils import Vector
import argparse


def sphericalCoords(s):
    try:
        if s == "":
            return 0, 0
        zenith, azimuth = map(int, s.split(','))
        return zenith, azimuth
    except:
        raise argparse.ArgumentTypeError("Coordinates must be zenith,azimuth")


parser = argparse.ArgumentParser(description='Blender pipeline.')
parser.add_argument('-o', '--operators', dest="operators", nargs='*', choices=['import', 'lod', 'render', 'convert'],
                    help='a list of operators to run in the pipeline (options: lod,render,export)')
parser.add_argument('-l', '--lods', dest="lods", nargs='*',
                    help='a list od level of details to use ont these operator (options: 0-100)')
parser.add_argument('-i', '--input', dest="input", help='path for the input file')
parser.add_argument('-od', '--outdir', dest="outdir", help='path for output dir')
parser.add_argument('-w', '--width', dest="width", help='render width')
parser.add_argument('-hg', '--height', dest="height", help='render height')
parser.add_argument('-c', '--coords', help="list of spherical coordinates for render", dest="coords",
                    type=sphericalCoords,
                    nargs='*')

args_to_parse = sys.argv[sys.argv.index('--') + 1:]
print(args_to_parse)
args = parser.parse_args(args_to_parse)
print("opeartors: ")
print(args)
if args.operators == None:
    sys.exit()

base_path = os.path.dirname(os.path.abspath(__file__)) + "/pipeline/"
base_lod = current_lod = calculated_lod = 100
for operator in args.operators:
    print("Running: " + operator)
    # turn all elements of the lods list into integers
    args.lods = [int(lod) for lod in args.lods]
    if operator == "lod" and args.lods and len(args.lods):
        # get the biggest lod value from the lods list
        current_lod = int(args.lods.pop(args.lods.index(max(args.lods))))
        calculated_lod = int((current_lod / base_lod) * 100)
        base_lod = current_lod
    if operator == "render" and args.coords and len(args.coords):
        coords = args.coords.pop()
    filename = base_path + operator + ".py"
    exec (compile(open(filename).read(), filename, 'exec'))

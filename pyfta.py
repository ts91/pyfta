from __future__ import annotations

import argparse

from viz import generate_viz

parser = argparse.ArgumentParser(
                    prog='pyfta',
                    description='Generates a Fault Tree Analysis (FTA) from a JSON file')

parser.add_argument('filename', help='the JSON description file to load')
parser.add_argument('-o', '--output', help='output directory', default='out')
parser.add_argument('-f', '--oformat', help='output format', default='pdf')

def main():
    args = parser.parse_args()
    generate_viz(args.filename, oformat=args.oformat, output=args.output)

main()
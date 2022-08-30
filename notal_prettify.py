import argparse
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)

args = parser.parse_args()

path = args.file


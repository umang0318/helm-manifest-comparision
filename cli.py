import argparse
import os
import sys

def is_dir(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory.")
    return path

parser = argparse.ArgumentParser(description="Pass two helm chart directory location")
parser.add_argument(
    "-p", "--path", nargs='*', default=[],
    metavar=('DIR1', 'DIR2'),
    help="Two directory paths to validate"
)

args = parser.parse_args()

# Validate only if exactly 2 paths are given
try:
    if len(args.path) != 2:
        raise ValueError(f"You must provide exactly two directory paths with --path.")
    args.path = [is_dir(path) for path in args.path]
except (ValueError, argparse.ArgumentTypeError) as e:
    print(e)
    sys.exit(1)

print(args.path)

import sys

import yaml
import pprint

def load_and_print_yaml(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    pprint.pprint(data)

def main():
    example_file = 'sample1.yaml'
    load_and_print_yaml(example_file)

if __name__ == '__main__':
    main()
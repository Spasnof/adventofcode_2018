import sys
from collections import namedtuple

class fabric_claims():
    def read_claim(self, line: str):
        claim_attr = namedtuple('claim_attr',['claim_id','x_start','x_end','y_start','y_end'])
        index, remainder = line.split('@')
        claim_attr.claim_id = index.replace('#','').strip()
        location, dimensions = remainder.split(':')
        x_cord, y_cord = location.split(',')
        x_width, y_height = dimensions.split('x')
        x_start, x_end = x_cord, x_cord + x_width
        y_start, y_end = y_cord, y_cord + y_height
        claim_attr.x_start = x_start
        claim_attr.x_end = x_end
        claim_attr.y_start = y_start
        claim_attr.y_end = y_end
        return claim_attr



if __name__ == '__main__':
    input_file = sys.argv[1]
    file_lines = []
    fc = fabric_claims()
    print('reading file for fabric claims: ', input_file)
    with open(input_file) as f:
        for line in f:
            print(fc.read_claim(line))


import sys
from collections import namedtuple

class fabric_claims():

    @staticmethod
    def claim_template():
        return namedtuple('claim_attr',['claim_id','x_start','x_end','y_start','y_end'])

    def read_claim(self, line: str):
        claim_attr = self.claim_template()
        index, remainder = line.split('@')
        claim_attr.claim_id = index.replace('#','').strip()
        location, dimensions = remainder.split(':')
        x_cord, y_cord = location.split(',')
        x_width, y_height = dimensions.split('x')
        x_start, x_end = int(x_cord), int(x_cord) + int(x_width)
        y_start, y_end = int(y_cord), int(y_cord) + int(y_height)
        claim_attr.x_start = x_start
        claim_attr.x_end = x_end
        claim_attr.y_start = y_start
        claim_attr.y_end = y_end
        return claim_attr

    def find_overlap(self, claim, claim_compare):
        '''
        1,3 vs 2,4
        :param claim:
        :param claim_compare:
        :return:
        '''
        def intersection(As, Ae, Bs, Be):
            if Bs > Ae or As > Be:
                return None
            else:
                Os = max(As, Bs)
                Oe = min(Ae, Be)
                return Os, Oe
        if not (claim and claim_compare):
            #  if either parameter is empty no point in comparing
            return None
        x_intersect = intersection(claim.x_start, claim.x_end, claim_compare.x_start, claim_compare.x_end)
        y_intersect = intersection(claim.y_start, claim.y_end, claim_compare.y_start, claim_compare.y_end)
        if x_intersect and y_intersect:
            i_claim = self.claim_template()
            i_claim.claim_id = claim.claim_id + '-' + claim_compare.claim_id
            i_claim.x_start, i_claim.x_end = x_intersect
            i_claim.y_start, i_claim.y_end = y_intersect
            return i_claim
        else:
            return None





if __name__ == '__main__':
    input_file = sys.argv[1]
    file_claims = []
    fc = fabric_claims()
    print('reading file for fabric claims: ', input_file)
    with open(input_file) as f:
        for line in f:
            file_claims.append(fc.read_claim(line))

    intersections = []
    line_index_ubound = len(file_claims) - 1
    # find all intersections in claims
    for i1 in range(0,line_index_ubound):
        for i2 in range(0,line_index_ubound):
            # ignore comparing lines to themselves
            if i1 != i2:
                overlap = fc.find_overlap(file_claims[i1], file_claims[i2])
                if overlap:
                    file_claims[i1] = None
                    file_claims[i2] = None


    # TODO ditch this idea of doing intersections, it is a cheap O(n) impelmentation but really hard to pull off.
    # TODO Do one pass with a dictionary like so {"(xycords)":[(array of claim ids)]
    # NOTE: that may be a fragile implementation if we end up needing to build out a 2d array representing all space
    #  but for a sparse number of options it should suffice for showing overlap.


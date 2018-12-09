import sys
from collections import namedtuple
from util.util import file_reader

class fabric_claims():

    claims = {}
    max_fabric_y = 0
    max_fabric_x = 0
    @staticmethod
    def claim_template():
        return namedtuple('claim_attr',['claim_id','x_start','x_end','y_start','y_end'])

    def __name_claim_index_id__(self,x,y):
        return f'{x},{y}'

    def add_claim(self, line: str):
        # parse the contents of the , claim_id, and dimensions, add it o the claim dictionary for each dimension
        index, remainder = line.split('@')
        claim_id = index.replace('#','').strip()
        location, dimensions = remainder.split(':')
        x_cord, y_cord = location.split(',')
        x_width, y_height = dimensions.split('x')
        x_start, x_end = int(x_cord), int(x_cord) + int(x_width)
        y_start, y_end = int(y_cord), int(y_cord) + int(y_height)
        # set the max fabric dimensions just as a housekeeping task
        self.max_fabric_x = max(self.max_fabric_x, x_end)
        self.max_fabric_y = max(self.max_fabric_y, y_end)
        # for the dimensions of the claim add to our dictionary
        for x in range(x_start,x_end):
            for y in range(y_start,y_end):
                index_key = self.__name_claim_index_id__(x,y)
                # initialize new values
                if not self.claims.get(index_key):
                    self.claims[index_key] = [claim_id]
                # for existing values just add more values to indicate "overlap"
                else:
                    self.claims[index_key].append(claim_id)


    def find_overlapping_tiles(self):
        total = 0
        for c in self.claims:
            if len(self.claims[c]) > 1 :
                total += 1
        return total

    def find_claim_id_not_intersecting_with_others_and_yeah_this_an_obnoxious_function_name(self):
        c_ids = {}
        for square in self.claims:
            # for each square, count the claims
            num_claims = len(self.claims[square])
            for c_id in self.claims[square]:
                # for each id count hte max number of overlap
                if c_id not in c_ids:
                    c_ids[c_id] = num_claims
                else:
                    c_ids[c_id] = max(num_claims, c_ids[c_id])
        results = []
        for id in c_ids:
            if c_ids[id] == 1:
                results.append(id)

        return  results


    def find_non_overlapping_tiles(self):
        '''
        this function isn't really needed but just keeping in case
        :return:
        '''
        results = []
        ix_fun = self.__name_claim_index_id__
        for x in range(0,self.max_fabric_x):
            for y in range(0,self.max_fabric_y):
                found_within_one = False
                directions_to_check = []
                left_b = min(x-1, 0)
                right_b = max(x+1, self.max_fabric_x)
                upper_b = min(y-1, 0)
                lower_b = max(y+1, self.max_fabric_y)
                directions_to_check.append(ix_fun(left_b, upper_b))
                directions_to_check.append(ix_fun(x, upper_b))
                directions_to_check.append(ix_fun(right_b, upper_b))
                directions_to_check.append(ix_fun(left_b, y))
                directions_to_check.append(ix_fun(x, y))
                directions_to_check.append(ix_fun(right_b, y))
                directions_to_check.append(ix_fun(left_b, lower_b))
                directions_to_check.append(ix_fun(x, lower_b))
                directions_to_check.append(ix_fun(right_b, lower_b))
                for dc in directions_to_check:
                    if dc in self.claims:
                        found_within_one = True
                if not found_within_one:
                    results.append(ix_fun(x, y))
        return results


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
            fc.add_claim(line)

    print(fc.find_overlapping_tiles())
    print(f'max x is {fc.max_fabric_x} max y is {fc.max_fabric_y}')
    print(fc.find_claim_id_not_intersecting_with_others_and_yeah_this_an_obnoxious_function_name())


    # TODO ditch this idea of doing intersections, it is a cheap O(n) impelmentation but really hard to pull off.
    # TODO Do one pass with a dictionary like so {"(xycords)":[(array of claim ids)]
    # NOTE: that may be a fragile implementation if we end up needing to build out a 2d array representing all space
    #  but for a sparse number of options it should suffice for showing overlap.

    fr = file_reader()

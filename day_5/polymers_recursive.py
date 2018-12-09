import util.util as u


class polymers():
    polymer_chain = None

    def read_input(self, line):
        self.polymer_chain = line

    def reduce_input(self, chain_to_check):
        chain = chain_to_check
        next_to_last_index = len(chain) - 2
        is_reduced = False
        while not is_reduced:
            found_reaction = False
            skip_chars = (None, None)
            for i in range(0, next_to_last_index):
                # compare the chars
                c1 = chain[i]
                c2 = chain[i + 1]
                is_equal = c1.upper() == c2.upper()
                is_reactive = (c1.isupper() and c2.islower()) \
                              or (c1.islower() and c2.isupper())
                if is_reactive and is_equal:
                    # if we find reactive combinations just don't add them
                    found_reaction = True
                    skip_chars = (i, i + 1)
                    break
            if found_reaction:
                new_chain = chain[:skip_chars[0]] + chain[skip_chars[1]:]
                # if we found a reaction in the comparision loop lets set the chain
                # print(f'length is now {len(new_chain)}')
                chain = new_chain
                next_to_last_index = len(chain) - 2
            else:
                is_reduced = True
        print('reduced chain length is ', len(chain))

    def optimize_chain(self):

        for c_U in set(self.polymer_chain.upper()):
            chain = self.polymer_chain
            c_l = c_U.lower()
            combo_id = c_U + ' and ' + c_l
            print(combo_id)
            chain = chain.replace(c_U, '').replace(c_l, '')
            self.reduce_input(chain)


if __name__ == '__main__':
    p = polymers()
    fr = u.file_reader(p.read_input)
    fr.read_file()
    # p.reduce_input(p.polymer_chain)
    p.optimize_chain()

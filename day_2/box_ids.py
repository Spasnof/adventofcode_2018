import sys

class box_ids():
    wordcount_results = []
    max_matching_chars = 0
    max_matching_results = (None,None)

    def diff_letters(self, original_str, compare_str, original_linenum, compare_linenum):
        '''
        compare two strings and line numbers,
        the comparision is done on a character by character basis.
        If the line numbers match more than what we have previously seen we will store the max_matching results.
        max matching results are stored int the (,) tuple self.max_matching_results
        :param original_str:
        :param compare_str:
        :param original_linenum:
        :param compare_linenum:
        :return:None
        '''
        if original_linenum == compare_linenum:
            # if we are comparing the same two lines do nothing
            return None
        matching_chars = len(original_str)
        index = 0
        for c in original_str:
            if c != compare_str[index]:
                matching_chars -= 1
            index += 1
        if matching_chars > self.max_matching_chars:
            # if we have the max number of matching strings lets go ahead and keep those results.
            self.max_matching_chars = matching_chars
            self.max_matching_results = (original_str, compare_str)

    def show_matching_letters(self):
        index = 0
        result1, result2 = self.max_matching_results
        index_ubound = len(result1) - 1
        matching = ''
        for i in range(0,index_ubound):
            if result1[i] == result2[i]:
                matching += result1[i]

        return matching

    def count_letters(self, input_str):
        '''
        store a dictionary containing the count of each letter
        so 'abcc' would contain {"a":day_1,"b":day_1,"c":day_2}
        :param input_str: Str
        :return: None
        '''
        char_count = {}
        for char in input_str:
            if not char_count.get(char):
            # init val
                char_count[char] = 1
            else:
                char_count[char] += 1

        self.wordcount_results.append(char_count)

    def return_num(self, num):
        '''
        with a given number see how many wordcount_results have numbers
        :param num: Int
        :return: Int
        '''
        num_count = 0
        for result in self.wordcount_results:
            found_in_result = False
            for char in result:
                if result[char] == num:
                    found_in_result = True
            if found_in_result:
                num_count += 1
        return num_count

if __name__ == '__main__':
    input_file = sys.argv[1]
    file_lines = []
    print('reading file for checksum: ', input_file)
    bi = box_ids()
    with open(input_file) as f:
        for line in f:
            file_lines.append(line)
            bi.count_letters(line)
    p2 = bi.return_num(2)
    p3 = bi.return_num(3)
    print(f'there are {p2} lines with 2 repeated characters')
    print(f'there are {p3} lines with 3 repeated characters')
    print('the product of both is ', p2 * p3)


    print('reading file again for closest matches')
    line_index_ubound = len(file_lines) -1
    for i1 in range(0,line_index_ubound):
        for i2 in range(0,line_index_ubound):
            current_line = file_lines[i1]
            compare_line = file_lines[i2]
            bi.diff_letters(current_line, compare_line, i1, i2)

    print(f'''the most matching line is {bi.max_matching_results}, with a difference of 
    {bi.max_matching_results[0]} vs
    {bi.max_matching_results[1]}
    ''')
    print(f'the matching chars are')
    print(bi.show_matching_letters())
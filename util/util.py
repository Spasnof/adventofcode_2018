import sys
class file_reader():
    input_file = sys.argv[1]
    lines = []
    line_function = None

    def __init__(self, *line_functions):
        self.line_function = line_functions


    def read_file(self):
        '''scan the file to memory can be accessed by the lines list or the lines collection'''
        with open(self.input_file) as f:
            for line in f:
                self.lines.append(line)
                for fun in self.line_function:
                    fun(line)



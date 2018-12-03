import sys


class Freqency():
    INIT_FREQNECY = 0
    resulting_frequency = INIT_FREQNECY
    frequency_count = {}

    def count_frequency(self,new_frequency):
        if not self.frequency_count.get(new_frequency):
            self.frequency_count[new_frequency] = 1
        else:
            self.frequency_count[new_frequency] += 1
        return self.frequency_count[new_frequency]

    def is_current_frequency_repeated(self):
        if self.frequency_count[self.resulting_frequency] == 2:
            return True
        else:
            return False


    def set_change(self, change_input):
        change_direction = change_input[0]
        change_value = int(change_input[1:])
        if change_direction == '-':
            self.resulting_frequency = self.resulting_frequency - change_value
        elif change_direction == '+':
            self.resulting_frequency = self.resulting_frequency + change_value
        else:
            raise NotImplemented
        if self.count_frequency(self.resulting_frequency) == 2:
            print(f'frequency {self.resulting_frequency} was reached twice')

    def print_freqency(self):
        print(f'freqency is :{self.resulting_frequency}')

frequency = Freqency()
input_file = sys.argv[1]
file_lines = []
print('reading file for final frequency: ', input_file)
with open(input_file,newline='\n') as f:
    for line in f:
        frequency.set_change(change_input=line)
        file_lines.append(line)

frequency.print_freqency()
while not frequency.is_current_frequency_repeated():
    for line in file_lines:
        frequency.set_change(change_input=line)
        if frequency.is_current_frequency_repeated():
            break








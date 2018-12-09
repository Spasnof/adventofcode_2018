from util.util import file_reader
import datetime as dt
import bisect


class guard_duty():
    entries = []
    guards = {}
    guards_min_asleep = {}
    guards_total_sleep = {}

    def _record_shifts_(self, guard_id, state, start: dt, end: dt):
        if not self.guards.get(guard_id):
            self.guards[guard_id] = []
        self.guards[guard_id].append((state, start, end))
        print('\t', state, guard_id, start, end)

    def _record_min_asleep_(self, guard_id, minute):
        print(f'guard_id {guard_id} sleeping at min {minute}')
        key = guard_id + '-' + str(minute)
        if not self.guards_min_asleep.get(key):
            self.guards_min_asleep[key] = 0
        self.guards_min_asleep[key] += 1

    def _find_most_sleeped_(self, guard_id):
        max_value = 0
        max_key = None
        for k in self.guards_min_asleep.keys():
            if guard_id + '-' in k:
                if self.guards_min_asleep[k] > max_value:
                    max_value = self.guards_min_asleep[k]
                    max_key = k
        return max_value, max_key

    def most_sleepy(self):
        if len(self.guards) == 0:
            raise IndexError('There are no guard_shifts, run record_guard_shifts() function first')
        for guard in self.guards:
            times_asleep = {}
            total_sleepytime = dt.timedelta()
            for shift in self.guards[guard]:
                if shift[0] == 'sleeps':
                    sleepytime = shift[2] - shift[1]
                    min_asleep = int(sleepytime.seconds / 60)
                    for i in range(min_asleep):
                        minute = (shift[1] + dt.timedelta(minutes=i)).minute
                        self._record_min_asleep_(guard, minute)
                    total_sleepytime += sleepytime
            self.guards_total_sleep[guard] = total_sleepytime

    def solve_most_sleepy(self):
        max_sleep = 0
        guard_id = None
        for k in self.guards_total_sleep:
            if self.guards_total_sleep[k].seconds / 60 > max_sleep:
                max_sleep = self.guards_total_sleep[k].seconds / 60
                guard_id = int(k)
        max_value, guardMinute_key = self._find_most_sleeped_(str(guard_id))

        print('solution to #1 is ', max_value * guard_id,
              ' with an id of ', guard_id
              , ' and a most sleeped minute of ', guardMinute_key)

    def record_guard_shifts(self):
        def __guard_id_parse__(entry: str):
            return entry.split('#')[1].split(' ')[0]

        if len(self.entries) == 0:
            raise IndexError('There are no guards, run line_parse() function first')
        current_guard = None
        for log in self.entries:
            # print(log)
            entry = log[1]
            time = log[0]
            # intitalize for first line and adjust for shift changes
            if current_guard == None and 'Guard' in entry:
                current_guard = __guard_id_parse__(entry)
                time_awake = time
            elif 'Guard' in entry:
                self._record_shifts_(current_guard, 'ends_shift', time_awake, time)
                current_guard = __guard_id_parse__(entry)
                time_awake = time
            # find the state of the guard
            if 'wake' in entry:
                time_awake = time
                self._record_shifts_(current_guard, 'sleeps', time_sleep, time - dt.timedelta(minutes=0))
            if 'asleep' in entry:
                time_sleep = time
                self._record_shifts_(current_guard, 'awake', time_awake, time - dt.timedelta(minutes=0))

    def line_parse(self, line: str):
        datetime, message = line.replace('[', '').split(']')
        datetime = dt.datetime.strptime(datetime, '%Y-%m-%d %H:%M')
        bisect.insort(self.entries, (datetime, str(message).replace('\n', '')))
        # date, time = datetime.split(' ')
        # year, month, day = [int(x) for x in date.split('-')]
        # foo = dt.date(year,month,day)
        # print(self.entries)

    def print_lines(self):
        for l in self.record_guard_shifts():
            print(l)


gd = guard_duty()
fr = file_reader(gd.line_parse)
fr.read_file()
gd.record_guard_shifts()
gd.most_sleepy()
guard_id, minutes = gd.solve_most_sleepy()

from datetime import datetime, timedelta


class Sports:
    def __init__(self, data, result_file_path):
        self.data = data
        self.result_file_path = result_file_path

        self.__calc_results()

    def __repr__(self):
        return str(self.data)

    def __calc_results(self):
        for k in self.data.keys():
            self.data[k]['final'] = self.data[k]['finish_time'] - self.data[k]['start_time']
            self.data[k]['final'] += timedelta(minutes=self.data[k]['foul_minutes'])

    def print_results(self):
        tmp_data = sorted(self.data.items(), key=lambda kv: (kv[1]['final'], kv[1]['name']))

        old_type = True

        with open(self.result_file_path, 'w') as f:
            f.write('Merginos\n')
            for d in sorted(tmp_data, key=lambda kv: kv[1]['is_girl'], reverse=True):
                if old_type != d[1]['is_girl']:
                    f.write('Vaikinai\n')
                    old_type = False

                hours = d[1]['final'].seconds // 3600
                minutes = (d[1]['final'].seconds % 3600) // 60
                seconds = d[1]['final'].seconds % 60

                f.write(' '.join([d[0], d[1]['name'].rjust(20, ' '), str(hours), str(minutes), str(seconds)]) + '\n')

    @classmethod
    def from_file(cls, input_file_path, result_file_path):
        with open(input_file_path, 'r') as f:
            data = {}

            no_start = int(f.readline())

            if no_start < 1 or no_start > 30:
                raise Exception('No of start value not valid.')

            for i in range(no_start):
                line = f.readline()
                name = line[:20]
                line = line[20:].split()
                unique_id = line[0]

                start_time = datetime.strptime('%s:%s:%s' % (line[1], line[2], line[3]), '%H:%M:%S')

                data[unique_id] = {
                    'name': name,
                    'start_time': start_time,
                    'is_girl': unique_id[0] == '1'
                }

            no_finish = int(f.readline())

            if no_finish < 1 or no_finish > 30:
                raise Exception('No of finish value not valid.')

            for i in range(no_finish):
                line = f.readline().split()
                unique_id = line[0]
                finish_time = datetime.strptime('%s:%s:%s' % (line[1], line[2], line[3]), '%H:%M:%S')

                data[unique_id]['finish_time'] = finish_time

                if data[unique_id]['is_girl']:
                    data[unique_id]['foul_minutes'] = 5 * 2 - (int(line[4]) + int(line[5]))
                else:
                    data[unique_id]['foul_minutes'] = 5 * 4 - (int(line[4]) + int(line[5]) + int(line[6]) + int(line[7]))

            data = {k:v for (k, v) in data.items() if v.get('finish_time', None) is not None}

            return cls(data=data, result_file_path=result_file_path)


if __name__ == '__main__':
    sports = Sports.from_file(input_file_path='data/U2_sample_3.txt', result_file_path='data/U2rez.txt')
    print(sports)
    sports.print_results()


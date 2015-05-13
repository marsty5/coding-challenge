class Parser:
    @classmethod
    def parse_line(cls, line):
        split_line = line.split()
        city_name, neighbour_pairs = split_line[0], split_line[1:]

        neighbours_dict = dict(pair.split('=') for pair in neighbour_pairs)

        output_dict = {
            'city_name': city_name,
            'neighbours': neighbours_dict
        }

        return output_dict
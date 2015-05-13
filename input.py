class Parser:
    @classmethod
    def parse_line(cls, line):
        split_line = line.split()
        city_name, neighbour_pairs = split_line[0], split_line[1:]
        output_dict = {
            'city_name': city_name,
        }

        for pair in neighbour_pairs:
            direction, name = pair.split('=')
            output_dict[direction] = name

        return output_dict
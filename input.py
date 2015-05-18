class Parser(object):
    @classmethod
    def _parse_line(cls, line):
        split_line = line.split()
        city_name, neighbour_pairs = split_line[0], split_line[1:]

        neighbours_dict = dict(pair.split('=') for pair in neighbour_pairs)

        output_dict = {
            'city_name': city_name,
            'neighbours': neighbours_dict
        }

        return output_dict

    @classmethod
    def _parse_lines(cls, lines):
        return [cls._parse_line(line) for line in lines]

    @classmethod
    def parse_file(cls, f):
        return cls._parse_lines(f.readlines())


class City(object):
    def __init__(self, name, neighbours=None):
        if neighbours is None:
            neighbours = {}

        self.name = name
        self.neighbours = neighbours

    def __eq__(self, other):
        if self.name != other.name:
            return False

        if self.neighbours.keys() != other.neighbours.keys():
            return False

        return all(self.neighbours[direction].name == other.neighbours[direction].name for direction in self.neighbours.keys())


class GraphBuilder(object):

    def __init__(self):
        self.cities = {}

    def _construct_and_add_city(self, city_dict):
        new_city = self._construct_city(city_dict)
        self.cities[new_city.name] = new_city
        return new_city

    def _construct_city(self, city_dict):
        city_name = city_dict['city_name']
        return City(city_name)

    def _add_neighbours(self, city_dict):
        source_city_name = city_dict['city_name']
        city_neighbours = city_dict['neighbours']

        source_city = self.cities[source_city_name]
        for direction, city_name in city_neighbours.iteritems():
            target_city = self.cities[city_name]
            source_city.neighbours[direction] = target_city

    @classmethod
    def build_graph(cls, city_dicts):
        graph_builder = cls()
        for city_dict in city_dicts:
            graph_builder._construct_and_add_city(city_dict)
        for city_dict in city_dicts:
            graph_builder._add_neighbours(city_dict)
        return graph_builder.cities

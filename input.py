from collections import defaultdict, namedtuple
import random
from sets import Set


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

    def has_neighbours(self):
        if self.neighbours:
            return True
        else:
            return False

class WorldBuilder(object):

    def __init__(self):
        self.world = World()

    def add_city(self, city_dict):
        city_name = city_dict['city_name']
        self.world.add_city(City(city_name))

    def add_neighbours(self, city_dict):
        source_city_name = city_dict['city_name']
        city_neighbours = city_dict['neighbours']

        for direction, city_name in city_neighbours.iteritems():
            target_city_name = self.world.cities[city_name].name
            self.world.make_neighbours(source_city_name, direction, target_city_name)

    @classmethod
    def build_world(cls, city_dicts):
        builder = cls()
        builder._add_cities(city_dicts)

        for city_dict in city_dicts:
            builder.add_neighbours(city_dict)

        return builder.world

    def _add_cities(self, city_dicts):
        for city_dict in city_dicts:
            self.add_city(city_dict)

    @classmethod
    def get_world(cls, city_graph, alien_count):
        world = World(city_graph)

        for alien in range(alien_count):
            random_city_name = random.choice(city_graph.keys())
            world.add_alien_to_city(random_city_name)

        return world


class World(object):

    directions = {
        'east': 'west',
        'west': 'east',
        'north': 'south',
        'south': 'north',
    }

    def __init__(self, cities=None):
        if cities is None:
            cities = {}
        self.cities = cities
        self.aliens = defaultdict(int)

    @property
    def city_names(self):
        return self.cities.keys()

    def add_city(self, city):
        self.cities[city.name] = city

    def make_neighbours(self, from_city_name, from_direction, to_city_name):
        from_city = self.cities[from_city_name]
        to_city = self.cities[to_city_name]
        from_city.neighbours[from_direction] = to_city
        to_direction = self.get_opposite_direction(from_direction)
        to_city.neighbours[to_direction] = from_city

    @classmethod
    def get_opposite_direction(cls, direction):
        return cls.directions[direction]

    def add_alien_to_city(self, city_name):
        if city_name not in self.cities:
            raise KeyError("{} doesn't exist".format(city_name))

        self.aliens[city_name] += 1

    def get_alien_count(self):
        return sum(self.aliens.values())

Move = namedtuple('Move', ['source', 'dest'])

class WorldSimulator(object):

    def __init__(self, world):
        self.world = world
        self.move_count = 0

    def add_aliens(self, alien_count):
        for alien_idx in range(alien_count):
            random_city = random.choice(self.world.city_names)
            self.world.add_alien_to_city(random_city)

    def perform_random_moves(self):
        move_list = self._get_move_list()
        self._apply_moves_to_world(move_list)

    """ Is there a better way to check if the city has neighbours? """
    def _get_move_list(self):
        move_spec = []
        empty_move = Move('', '')
        for city_name in self.world.city_names:
            city_alien_count = self.world.aliens[city_name]

            for alien_idx in range(city_alien_count):
                move = self._get_move(city_name)
                if move != empty_move:
                    move_spec.append(move)

        return move_spec

    def _get_move(self, city_name):
        neighbours = self.world.cities[city_name].neighbours

        if neighbours:
            dest_city = random.choice(neighbours.values())
            return Move(city_name, dest_city.name)
        else:
            return Move('', '')

    def _apply_moves_to_world(self, move_list):
        for move in move_list:
            self._apply_move(move)

    def _apply_move(self, move):
        self.world.aliens[move.dest] += 1
        self.world.aliens[move.source] -= 1

    def resolve_conflicts(self):
        for city_name in self.world.city_names:

            alien_count = self._get_alien_count(city_name)

            if alien_count > 1:
                print '{} has been destroyed by {} aliens!'.format(city_name, alien_count)
                self._delete_aliens(city_name)
                self._delete_neighbours(city_name)
                self._delete_city(city_name)

    def _get_alien_count(self, city_name):
        return self.world.aliens[city_name]

    def _delete_aliens(self, city_name):
        del self.world.aliens[city_name]

    def _delete_neighbours(self, city_name_to_be_deleted):
        neighbours = self.world.cities[city_name_to_be_deleted].neighbours
        for direction, neighbour in neighbours.iteritems():
            opposite_direction = self.world.get_opposite_direction(direction)

            del neighbour.neighbours[opposite_direction]

    def _delete_city(self, city_name):
        del self.world.cities[city_name]

    def run_simulation(self):
        allowed_moves = 10000
        zero_aliens = 0
        exit_message = 0

        while True:
            self.perform_random_moves()
            self.move_count += 1
            self.resolve_conflicts()

            if self.world.get_alien_count() == zero_aliens:
                print '\nNo aliens in the world. Exiting...'
                break

            if self.move_count == allowed_moves:
                print '\nMax moves reached. Exiting...'
                break

            occupied_cities_with_no_neighbours = self.get_occupied_cities_with_no_neighbours()
            if len(occupied_cities_with_no_neighbours) > 0:
                print '\nNo moves allowed. Exiting...'
                break

        return exit_message

    def get_occupied_cities_with_no_neighbours(self):

        occupied_city_names = self._get_occupied_cities()
        occupied_city_names_with_no_neighbours = self._get_city_names_with_no_neighbours(occupied_city_names)

        return occupied_city_names_with_no_neighbours

    def _get_occupied_cities(self):
        zero_aliens = 0
        occupied_city_names = Set()

        for city_name, alien_count in self.world.aliens.iteritems():
            if alien_count > zero_aliens:
                occupied_city_names.add(city_name)

        return occupied_city_names

    def _get_city_names_with_no_neighbours(self, city_names):
        cities_with_no_neighbours = Set()

        for city_name in city_names:
            if not self.world.cities[city_name].has_neighbours():
                cities_with_no_neighbours.add(city_name)

        return cities_with_no_neighbours
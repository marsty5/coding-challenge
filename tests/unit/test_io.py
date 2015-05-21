import unittest
from StringIO import StringIO
from input import Parser, City, World, WorldBuilder, WorldSimulator, Move


class TestParser(unittest.TestCase):
    def setUp(self):
        self.expected_output = [
            {
                'city_name': 'a',
                'neighbours':
                    {
                        'north': 'b',
                    }
            },
            {
                'city_name': 'b',
                'neighbours':
                    {
                        'south': 'a',
                    }
            },
        ]

    def test_parser_parse_line(self):
        line = 'test north=a south=b east=c west=d'
        expected = {
            'city_name': 'test',
            'neighbours': {
                'north': 'a',
                'south': 'b',
                'east': 'c',
                'west': 'd',
            }
        }

        parsed = Parser._parse_line(line)
        self.assertDictEqual(parsed, expected)

    def test_parser_parse_line_with_no_neighbours(self):
        line = 'test'
        expected = {
            'city_name': 'test',
            'neighbours': {},
        }

        parsed = Parser._parse_line(line)
        self.assertDictEqual(parsed, expected)

    def test_parser_parse_lines(self):
        lines = ['a north=b', 'b south=a']
        expected = self.expected_output

        parsed = Parser._parse_lines(lines)
        for e, p in zip(expected, parsed):
            self.assertDictEqual(e, p)

    def test_parser_parse_file(self):
        f = StringIO('a north=b\nb south=a')
        expected = self.expected_output

        parsed = Parser.parse_file(f)
        for e, p in zip(expected, parsed):
            self.assertDictEqual(e, p)


class TestWorld(unittest.TestCase):

    def test_empty_world(self):
        world = World()
        self.assertDictEqual(world.cities, {})

    def test_add_city(self):
        world = World()
        city = City('a')

        world.add_city(city)

        self.assertIn(city.name, world.city_names)

    def test_create_neighbours(self):
        city_a = City('a')
        city_b = City('b')
        city_c = City('c')
        world_dict = {
            'a': city_a,
            'b': city_b,
            'c': city_c,
        }

        world = World(world_dict)

        world.make_neighbours(city_a.name, 'east', city_b.name)
        world.make_neighbours(city_a.name, 'south', city_c.name)

        self.assertEqual(world.cities[city_a.name].neighbours['east'], city_b)
        self.assertEqual(world.cities[city_b.name].neighbours['west'], city_a)

        self.assertEqual(world.cities[city_a.name].neighbours['south'], city_c)
        self.assertEqual(world.cities[city_c.name].neighbours['north'], city_a)


class TestWorldBuilder(unittest.TestCase):

    def test_add_single_node(self):
        city_dict = {
            'city_name': 'a',
            'neighbours': {'south': 'b'}
        }

        builder = WorldBuilder()
        builder.add_city(city_dict)
        world = builder.world

        expected_city = City('a')

        self.assertEqual(world.cities['a'], expected_city)
        self.assertEqual(len(world.cities), 1)

    def test_add_neighbours(self):
        city_dicts = [
            {
                'city_name': 'a',
                'neighbours': {'south': 'b'}
            },
            {
                'city_name': 'b',
                'neighbours': {'north': 'a'}
            },
        ]

        world = World({
            'a': City('a'),
            'b': City('b'),
        })

        builder = WorldBuilder()
        builder.world = world

        for city_dict in city_dicts:
            builder.add_neighbours(city_dict)

        self.assertEqual(world.cities['b'], world.cities['a'].neighbours['south'])
        self.assertEqual(world.cities['a'], world.cities['b'].neighbours['north'])


class TestWorldSimulator(unittest.TestCase):

    def setUp(self):
        self.expected_world = self.get_expected_world()

    def get_expected_world(self):
        city_a = City('a')
        city_b = City('b')

        builder = WorldBuilder()
        builder.world.add_city(city_a)
        builder.world.add_city(city_b)
        builder.world.make_neighbours(city_a.name, 'south', city_b.name)

        return builder.world

    """ Do we need this test?
        The test after this makes more sense to me.
        Or shall I actually drop an alien to a specific city to test it correctly?
    """
    def test_world_construction(self):
        alien_count = 2
        self.expected_world.add_alien_to_city('a')
        self.expected_world.add_alien_to_city('b')
        self.assertEqual(self.expected_world.get_alien_count(), alien_count)

    def test_drop_aliens(self):
        alien_count = 10
        sim = WorldSimulator(self.expected_world)
        sim.add_aliens(alien_count)
        self.assertEqual(self.expected_world.get_alien_count(), alien_count)

    def test_world_raises(self):
        self.assertRaises(KeyError, self.expected_world.add_alien_to_city, 'z')

    def test_world_get_move_goes_to_valid_city(self):
        sim = WorldSimulator(self.expected_world)
        move = sim._get_move('a')
        valid_moves = [Move('a', city.name) for city in self.expected_world.cities['a'].neighbours.values()]

        self.assertIn(move, valid_moves)

    def test_world_length_of_get_move_list(self):
        alien_count = 10

        sim = WorldSimulator(self.expected_world)
        sim.add_aliens(alien_count)
        move_list = sim._get_move_list()

        self.assertEqual(len(move_list), alien_count)

    def test_world_applies_move_correctly(self):
        expected_world = self.get_expected_world()

        expected_world.add_alien_to_city('a')
        move = Move('a', 'c')

        sim = WorldSimulator(expected_world)
        sim._apply_move(move)

        self.assertEqual(expected_world.aliens['a'], 0)
        self.assertEqual(expected_world.aliens['c'], 1)

    def test_world_move_maintains_alien_count(self):
        alien_count = 2

        sim = WorldSimulator(self.expected_world)
        sim.add_aliens(alien_count)

        move_list = sim._get_move_list()
        sim._apply_moves_to_world(move_list)
        self.assertEqual(sim.world.get_alien_count(), alien_count)

    def test_resolve_conflicts_removes_city(self):
        alien_count = 2

        sim = WorldSimulator(self.expected_world)
        for alien_idx in range(alien_count):
            sim.world.add_alien_to_city('a')

        sim.resolve_conflicts()
        self.assertNotIn('a', sim.world.city_names)

        for city_name in sim.world.city_names:
            neighbours = sim.world.cities[city_name].neighbours.values()
            for neighbour in neighbours:
                self.assertNotEqual(neighbour.name, 'a')

    def test_resolve_conflicts_removes_aliens(self):
        alien_count = 2

        sim = WorldSimulator(self.expected_world)

        for alien_idx in range(alien_count):
            sim.world.add_alien_to_city('a')

        alien_count_initial = sim.world.get_alien_count()

        sim.resolve_conflicts()

        alien_count_final = alien_count_initial - alien_count

        self.assertEqual(sim.world.get_alien_count(), alien_count_final)
        self.assertNotIn('a', sim.world.aliens.keys())

    def test_run_simulation_till_zero_aliens(self):

        city_a = City('a')

        builder = WorldBuilder()
        builder.world.add_city(city_a)

        sim = WorldSimulator(builder.world)

        alien_count = 2
        for alien_idx in range(alien_count):
            sim.world.add_alien_to_city('a')

        sim.run_simulation()
        zero_aliens = 0
        self.assertEqual(sim.world.get_alien_count(), zero_aliens)

    def test_run_simulation_till_max_moves_reached(self):

        city_a = City('a')
        city_b = City('b')

        builder = WorldBuilder()
        builder.world.add_city(city_a)
        builder.world.add_city(city_b)
        builder.world.make_neighbours(city_a.name, 'south', city_b.name)

        sim = WorldSimulator(builder.world)
        sim.world.add_alien_to_city('a')
        sim.run_simulation()

        allowed_moves = 10000
        self.assertEqual(sim.move_count, allowed_moves)

    """
    It's like taking a picture of me holding an apple with my right hand
    And then taking a picture of me holding the same apple with my left hand
    And i'm comparing the two pictures
    """
    def test_run_simulation_till_no_moves_allowed(self):

        city_a = City('a')
        builder = WorldBuilder()
        builder.world.add_city(city_a)

        sim = WorldSimulator(builder.world)
        sim.world.add_alien_to_city('a')

        sim.run_simulation()
        occupied_cities_with_no_neighbours = sim.get_occupied_cities_with_no_neighbours()
        one_occupied_city_with_no_neighbours = 1
        self.assertEqual(len(occupied_cities_with_no_neighbours), one_occupied_city_with_no_neighbours )


if __name__ == '__main__':
    unittest.main()

import unittest
from StringIO import StringIO
from input import Parser, City
from input import GraphBuilder


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


class TestWorldBuilder(unittest.TestCase):
    def setUp(self):
        pass



class TestGraphBuilder(unittest.TestCase):
    def test_add_single_node(self):
        city_dict = {
            'city_name': 'a',
            'neighbours': {'south': 'b'}
        }

        builder = GraphBuilder()
        city = builder._construct_and_add_city(city_dict)

        self.assertEqual('a', city.name)

        self.assertDictEqual({}, city.neighbours)
        self.assertEqual(1, len(builder.cities))

    def test_add_multiple_nodes(self):
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

        builder = GraphBuilder()

        for city_dict in city_dicts:
            builder._construct_and_add_city(city_dict)

        self.assertEqual(2, len(builder.cities))

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

        builder = GraphBuilder()
        for city_dict in city_dicts:
            builder._construct_and_add_city(city_dict)

        for city_dict in city_dicts:
            builder._add_neighbours(city_dict)

        self.assertEqual(builder.cities['b'], builder.cities['a'].neighbours['south'])
        self.assertEqual(builder.cities['a'], builder.cities['b'].neighbours['north'])


if __name__ == '__main__':
    unittest.main()

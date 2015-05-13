import unittest
from input import Parser


class TestParser(unittest.TestCase):
    def test_parser_parse_line(self):
        line = 'test north=a south=b east=c west=d'
        expected = {
            'test': {
                'north': 'a',
                'south': 'b',
                'east': 'c',
                'west': 'd',
            }
        }

        parsed = Parser.parse_line(line)
        self.assertDictEqual(parsed, expected)

    def test_parser_parse_line_with_no_neighbours(self):
        line = 'test'
        expected = {
            'city_name': 'test',
        }

        parsed = Parser.parse_line(line)
        self.assertDictEqual(parsed, expected)

    def test_parser_parse_lines(self):
        lines = 'a north=b\nb south=a'




if __name__ == '__main__':
    unittest.main()

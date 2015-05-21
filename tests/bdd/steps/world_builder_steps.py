from behave import *
from input import City, WorldBuilder

from hamcrest import assert_that, equal_to

use_step_matcher("re")

@given("I have a list of city dicts")
def step_impl(context):
    context.city_dicts = [
        {
            'city_name': 'a',
            'neighbours': {'south': 'b'}
        },
        {
            'city_name': 'b',
            'neighbours': {'north': 'a'}
        },
    ]


@when("I build a world")
def step_impl(context):
    context.world = WorldBuilder.build_world(context.city_dicts)


@then("I should have the correct world")
def step_impl(context):
    city_a = City('a')
    city_b = City('b')

    city_a.neighbours = {'south': city_b}
    city_b.neighbours = {'north': city_a}

    expected_output = {
        'a': city_a,
        'b': city_b,
    }

    assert_that(context.world.cities, equal_to(expected_output))
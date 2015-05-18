from behave import *
from testtools.testcase import unittest
from input import GraphBuilder, City

from hamcrest import assert_that, equal_to, is_not

use_step_matcher("re")

@given("I have a list of city dicts")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
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


@when("I build a graph")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.graph = GraphBuilder.build_graph(context.city_dicts)


@then("I should have the correct graph")
def step_impl(context):
    """
    :type context behave.runner.Context
    """

    city_a = City('a')
    city_b = City('b')

    city_a.neighbours = {'south': city_b}
    city_b.neighbours = {'north': city_a}

    expected_output = {
        'a': city_a,
        'b': city_b,
    }

    assert_that(context.graph, equal_to(expected_output))
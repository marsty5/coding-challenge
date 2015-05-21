from behave import *
from hamcrest import assert_that, equal_to
from input import WorldBuilder, WorldSimulator, City, World

use_step_matcher("parse")

@given("I have a world")
def step_impl(context):
    """
    Is it correct to create the world directly from world?
    Or shall I create the world via WorldBuilder?
    My answer: the first one, because we are testing the WorldBuilder

    My answer to my answer:
    Wrong! We tested WorldBuilder in the world_builder BDD
    So I should be able to use WorldBuilder now

    Answer to answer to answer:
    World_Builder creates the world from file
    """
    world = World()

    city_a = City('a')
    city_b = City('b')

    world.add_city(city_a)
    world.add_city(city_b)
    world.make_neighbours(city_a.name, 'south', city_b.name)

    context.world = world


@step("I make a world simulation")
def step_impl(context):
    context.sim = WorldSimulator(context.world)


@step("I put {alien_count} aliens in the world")
def step_impl(context, alien_count):
    context.sim.add_aliens(int(alien_count))


@step("I move the aliens once")
def step_impl(context):
    context.sim.perform_random_moves()


@then("There are still {alien_count} aliens")
def step_impl(context, alien_count):
    assert_that(context.sim.world.get_alien_count(), equal_to(int(alien_count)))


@step("I have more than one aliens in a city")
def step_impl(context):
    alien_count = 2
    for alien_idx in range(alien_count):
        context.sim.world.add_alien_to_city('a')

    context.city_name_with_conflicts = 'a'
    context.alien_with_no_conflicts_count = alien_count - context.sim.world.aliens['a']


@when("I resolve conflicts")
def step_impl(context):
    context.sim.resolve_conflicts()


@then("The city is removed from the world")
def step_impl(context):
    assert_that(context.city_name_with_conflicts not in context.sim.world.city_names)
    cities = context.sim.world.cities

    for city in cities.values():
        assert_that(context.city_name_with_conflicts not in city.neighbours.keys())


@step("Those aliens are removed from the world")
def step_impl(context):
    #assert_that(len(context.sim.world.get_alien_count()), equal_to(0))
    assert_that(context.sim.world.get_alien_count(), equal_to(context.alien_with_no_conflicts_count))


@then("Stop Simulation")
def step_impl(context):

    pass


@when("I simulated 10,000 moves")
def step_impl(context):

    pass
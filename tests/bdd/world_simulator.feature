# Created by marsty5 at 18/05/15
Feature: World Simulator

  Scenario: Simulate a move
    Given I have a world
    When I make a world simulation
      And I put 10 aliens in the world
      And I move the aliens once
    Then There are still 10 aliens

  Scenario: Simulate a Conflict Resolution
    Given I have a world
      And I make a world simulation
      And I have more than one aliens in a city
    When I resolve conflicts
    Then The city is removed from the world
      And Those aliens are removed from the world

#  Scenario: Stop the simulation
#    Given I have a world
#      And I have 10 aliens
#      And I have a world simulation
#    When I have 0 aliens
#    Then Stop Simulation
#
#
#  Scenario: Stop the simulation
#    Given I have a world
#      And I have 10 aliens
#      And I have a world simulation
#    When I simulated 10,000 moves
#    Then Stop Simulation
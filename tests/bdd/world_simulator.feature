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

  Scenario: Simulation stops after all aliens die
    Given I have a world with one city
      And I make a world simulation
      And I put 2 aliens in the world
    When I run the simulation
    Then There are 0 aliens

  Scenario: Simulation stops after 10,000 moves
    Given I have a world
      And I make a world simulation
      And I put 1 aliens in the world
    When I run the simulation
    Then I simulated 10000 moves

  Scenario: Simulation stops after all aliens are trapped
    Given I have a world with one city
      And I make a world simulation
      And I put 1 aliens in the world
    When I run the simulation
    Then I simulated 0 moves
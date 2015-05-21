# Created by shaun at 18/05/15
Feature: World Building

  Scenario: Build a World
    Given I have a list of city dicts
    When I build a world
    Then I should have the correct world
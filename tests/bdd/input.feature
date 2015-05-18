# Created by shaun at 18/05/15
Feature: GraphBuilder

  Scenario: Build a Graph
    Given I have a list of city dicts
    When I build a graph
    Then I should have the correct graph
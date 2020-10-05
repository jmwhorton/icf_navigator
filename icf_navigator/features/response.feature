@wip
Feature: Response
  User responses to questions need to be saved and associated
  with the question that prompted them.
  There may be several pieces of information for each question.

  Scenario: A user responds to a yes no question
    Given A configured app
      And An authenticated user
      And On a yesnoquestion
      And The first form
    When User answers with yes
    Then The answer should be stored

  Scenario: A user responds to a text question
    Given A configured app
      And An authenticated user
      And On a text question
      And The first form
    When User answers with "some text"
    Then "some text" should be stored

  Scenario: A user responds to a multiselect question
    Given A configured app
      And An authenticated user
      And On a multiselect question
      And The first form
    When User selects "Children"
    Then "Children" should be selected

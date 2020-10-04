Feature: Response
  User responses to questions need to be saved and associated
  with the question that prompted them.
  There may be several pieces of information for each question.

  Scenario: A user responds to a question
    Given A configured app
      And An authenticated user
      And A yesnoquestion
      And The first form
    When User answers with yes
    Then The answer should be stored

@wip
Feature: Question
  There are many questions on the navigator which have multiple forms
  we need to be able to modify these and probably track their versioning
  information in some form...

  Scenario: A form can have multiple questions
    Given A configured app
    Then The form should have multiple questions

  Scenario: A question knows how to render itself
    Given A question with form
    When The first question is selected
    Then The question should have a form

  Scenario: A yes or no question
    Given A yesno question
    When The first question is selected
    Then The form should have radio buttons

  Scenario: A free text question
    Given A free text question
    When The first question is selected
    Then The form should have a text field

  Scenario: A checkbox question
    Given A multiselect question
    When The first question is selected
    Then The form should have multiple checkboxes

Feature: Form
  Users should be able to create multiple forms
  and share the rights to edit those with multiple
  users.

  Scenario: A user can create a new form
    Given An authenticated user
    When Vists the homepage
    Then They should see a form to create a new form

  Scenario: Only logged in users can create forms
    When Vists the homepage
    Then They should not be able to create a new form

  Scenario: Users can create multiple forms
    Given An authenticated user
    When Creates form "A"
      And Creates form "B"
      And Vists the homepage
    Then Should see "A"
      And Should see "B"

  Scenario: Users can see questions for a form
    Given A configured app
      And An authenticated user
    When Creates form "A"
    Then Should see multiple questions

@wip
Feature: Form
  Users should be able to create multiple forms
  and share the rights to edit those with multiple
  users.

  Scenario: A user can create a new form
    When An authenticated user
      And Vists the homepage
    Then They should see a form to create a new form

  Scenario: Only logged in users can create forms
    When Vists the homepage
    Then They should not be able to create a new form

Feature: Login
  Users should be able to login using their AD credentials

  Scenario: An AD user attempts to login
    When A user logs in with correct credentials
    Then Their username should appear on the page

  Scenario: A user should remain logged in
    When A user logs in with correct credentials
      And They reload the homepage
    Then Their username should appear on the page

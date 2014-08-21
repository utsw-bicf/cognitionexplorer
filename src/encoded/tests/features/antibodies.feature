@antibodies @usefixtures(workbook)
Feature: Antibodies

    Scenario: Table
        When I visit "/antibodies/"
        And I wait for the table to fully load

        When I fill in "q" with "musculus"
        Then I should see an element with the css selector "tr:not([hidden]) a[href='/antibodies/35cf08c4-72cf-4408-8552-231e3e35b279/']" within 1 seconds
        And I should see an element with the css selector "tr[hidden] a[href='/antibodies/c808814f-376f-41ee-b93e-ddd00294ca3d/']"
        And I should see exactly one element with the css selector ".table-count" containing the text "3"

    Scenario: Click through
        When I visit "/antibodies/"
        And I wait for the table to fully load
        When I click the link to "/antibodies/c808814f-376f-41ee-b93e-ddd00294ca3d/"
        Then I should see an element with the css selector "div.data-display"
        And I should see "Approval for ENCAB000AOF"

        When I go back
        And I wait for the table to fully load
        When I click the link to "/antibodies/35cf08c4-72cf-4408-8552-231e3e35b279/"
        And I should see an element with the css selector "div.data-display"
        And I should see "Approval for ENCAB000ANU"

    Scenario: Detail page
        When I visit "/antibodies/58b4df5b-ba21-4111-a715-3b5ba863b9b4/"
        Then I should see an element with the css selector "div.data-display"
        And I should see "eligible"
        And I should see an element with the css selector "div.characterizations"
        And I should see at least 1 elements with the css selector "section"
        And I should see at least 1 elements with the css selector "figure"
        And I should see at least 1 elements with the css selector "img.characterization-img"
        And I should see "Richard Myers, HAIB"
        And I should see "U54HG006998"

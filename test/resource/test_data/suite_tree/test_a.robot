*** Settings ***
Resource          resource_a.robot
Resource          common.robot

*** Variable ***
${TEST_A}         AAA

*** Test Cases ***
Test A Case A1
    Resource A Keyword 1    ${TEST_A}
    Common Keyword 1    ${TEST_A}
    Common Keyword 2
    test_a.Test A Keyword
    Really Long Keyword To Test With Jumping To Keyword Does Not Scroll The Visible Area To A Wrong Place Should There Be More Words

Test A Case A2
    [Documentation]    Given, When, Then tests.
    Given Common Keyword 2
    When Common Keyword 1
    Then Keyword

*** Keywords ***
Test A Keyword
    [Documentation]    Some Doc Here
    Log    Test A Here

Keyword
    [Documentation]    some doc
    Log    1
    resource_a.Resource A Keyword 1
    ...    kwa1
    Resource A Keyword 2
    LibNoClass.Library Keyword 1
    ...    ${EMPTY}
    Library Keyword 1
    ...    ${EMPTY}
    Other Name Here
    ...    ${True}
    LongName.Other Name Here
    ...    ${True}

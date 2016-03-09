*** Settings ***
Resource          resource_a.robot
Resource          common.robot

*** Variable ***
${TEST_A}         AAA

*** Test Cases ***
Test A Case A1
    Resource A Keyword 1    ${TEST_A}
    Common Keyword 1    ${TEST_A}
    test_a.Test A Keyword

*** Keywords ***
Test A Keyword
    [Documentation]    Some Doc Here
    Log    Test A Here

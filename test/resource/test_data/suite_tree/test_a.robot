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
    Really Long Keyword To Test With Jumping To Keyword Does Not Scroll The Visible Area To A Wrong Place Should There Be More Words

*** Keywords ***
Test A Keyword
    [Documentation]    Some Doc Here
    Log    Test A Here

Keyword
    [Documentation]    some doc
    Log    1

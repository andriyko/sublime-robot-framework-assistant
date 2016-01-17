*** Settings ***
Resource          resource_a.robot
Resource          common.robot

*** Variable ***
${TEST_A}         AAA

*** Test Cases ***
Test A Case A1
    Resource A Keyword 1    ${TEST_A}
    Common Keyword 1    ${TEST_A}


*** Settings ***
Resource          resource_b.robot
Resource          common.robot

*** Variable ***
${TEST_B}         AAA

*** Test Cases ***
Test A Case A1
    Resource B Keyword 1    ${TEST_A}
    Common Keyword 1    ${TEST_A}
    Embedding arg To Keyword Name
    Other arg1 and arg2 Too
    Log    My User name is "%{USER}"" in OS

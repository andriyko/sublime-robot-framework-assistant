*** Settings ***
Library           OperatingSystem

*** Variables ***
${RESOURCE_A}     A1A1A1A1A1

*** Keywords ***
Resource A Keyword 1
    [Arguments]    ${kwa1}
    Log    ${kwa1}

Resource A Keyword 2
    Log    ${RESOURCE_A}

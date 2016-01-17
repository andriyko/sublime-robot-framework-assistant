*** Settings ***
Library           Process

*** Variables ***
${RESOURCE_B}     B1B1B1B1B1


*** Keywords ***
Resource B Keyword 1
    [Arguments]    ${kwb1}
    Log    ${kwb1}

Resource B Keyword 2
    Log    ${RESOURCE_B}

*** Settings ***
Library           OperatingSystem
Library           LibNoClass.py

*** Variables ***
${RESOURCE_A}     A1A1A1A1A1
&{DICTIONARY}     a=1
...               b=2

*** Keywords ***
Resource A Keyword 1
    [Arguments]    ${kwa1}
    Log    ${kwa1}

Resource A Keyword 2
    Log    ${RESOURCE_A}
    Library Keyword 1    Some Text Here
    Log    %{USER}

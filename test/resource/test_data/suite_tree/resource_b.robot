*** Settings ***
Library           Process
Library           LibraryNameWhichIsLongerThan100CharactersButItSeemsThatItRequiresQuiteAlotLettersInTheFileNameAndIsNotGoodRealLifeExample.py    WITH NAME    OtherNameLib

*** Variables ***
${RESOURCE_B}     B1B1B1B1B1


*** Keywords ***
Resource B Keyword 1
    [Arguments]    ${kwb1}
    Log    ${kwb1}

Resource B Keyword 2
    Log    ${RESOURCE_B}

Embedding ${arg} To Keyword Name
    [Documentation]    Keyword with embedding arg to keyword name
    Log    ${arg}
    OtherNameLib.Keyword Which Also Has Really Long Name But Not As Long The Class Name By 1234 In Keyword

Resource B Keyword 3 Many Args
    [Arguments]    ${arg1}=${True}    ${arg2}=Text_here    ${arg3}=${False}
    Log    ${arg1}

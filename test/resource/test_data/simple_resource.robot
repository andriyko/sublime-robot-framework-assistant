*** Settings ***
Library           Selenium2Library
Documentation     foobar
Resource          simple_resrouce2.robot

*** Variable ***
${ARG}            1

*** Keywords ***
My Kw 1
    [Arguments]    ${arg1}=${False}    ${arg2}=${True}
    [Tags]    some_tag    other_tag
    [Documentation]    Some documentation
    ${some_return_value} =    Set Variable     123
    ${other_return_value} =    Set Variable     ${EMPTY}
    Log    ${arg1}
    [Return]    ${False}

My Kw 2
    [Arguments]    ${arg2}=${False}    ${arg2}=${True}
    [Documentation]    Some documentation.
    ...    In multi line
    Log    ${arg2}
    [Return]    ${arg2}
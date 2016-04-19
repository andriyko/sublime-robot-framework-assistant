*** Settings ***
Library           Selenium2Library    timeout=5.0    implicit_wait=0.0
Documentation     foobar
Resource          simple_resrouce2.robot
Variables         simple_variable_file.py    arg11    arg22

*** Variable ***
${VAR2}            1

*** Test Cases ***
Example Test
    Log    ${True}
    ${some_var} =    Set Variable    12345

*** Keywords ***
My Kw 1
    [Arguments]    ${arg1}=${False}    ${arg2}=${True}
    [Tags]    some_tag    other_tag
    [Documentation]    Some documentation
    ${other_return_value1}    ${some_return_value1} =    Set Variable     123
    ${other_return_value2} =    Set Variable     ${EMPTY}
    Log    ${arg1}
    [Return]    ${False}

My Kw 2
    [Arguments]    ${arg2}=${False}    ${arg4}
    [Tags]    tag1
    [Documentation]    Some documentation.
    ...    In multi line
    Log    ${arg2}
    [Return]    ${arg2}
*** Settings ***
Library           ../../src/dataparser/parser/TestDataParser.py
Library           Collections
Variables         variable_files/suite_parser_vars.py

*** Test Cases ***
Parser Should Be Able To Parse Resource File
    ${result} =    Parse Resource
    ...    ${CURDIR}${/}..${/}resource${/}test_data${/}simple_resource.robot
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_RESOURCE}

Parser Should Be Able To Parse Test Suite
    ${result} =    Parse Suite
    ...    ${CURDIR}${/}..${/}resource${/}test_data${/}simple_test.robot
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_TEST}

Parser Should Be Able To Parse Variable File
    ${list} =    Create List    arg11    arg22
    ${result} =    Parse Variable File
    ...    ${CURDIR}${/}..${/}resource${/}test_data${/}simple_variable_file.py
    ...    ${list}
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_VAR}

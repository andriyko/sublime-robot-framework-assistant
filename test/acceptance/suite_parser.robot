*** Settings ***
Library           ../../src/parser/TestDataParser.py
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
    ...    ${CURDIR}${/}..${/}resource${/}simple_test.robot
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_RESOURCE}

Parser Should Be Able To Parse Variable File
    ${result} =    Parse Variable File
    ...    ${CURDIR}${/}..${/}resource${/}simple_var.py
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_RESOURCE}
Parser Should Be Able To Parse Internal Library
    ${result} =    Parse Library
    ...    BuiltIn
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_RESOURCE}
Parser Should Be Able To Parse External Library From Python Path
    ${result} =    Parse Library
    ...    Selenium2Library
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_RESOURCE}

Parser Should Be Able To Parse External Library From File
    ${result} =    Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}utilities${/}json_to_dictionary.JsonParser
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${SIMPLE_RESOURCE}

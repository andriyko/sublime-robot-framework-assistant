*** Settings ***
Library           OperatingSystem
Library           String
Library           ../../scr/DataParser.py
Library           ../resource/utilities/json_to_dictionary.JsonParser

*** Test Cases ***
Parser Should Be Able To Parse Resource File
    ${result} =    DataParser.Parse Resource
    ...    ${CURDIR}${/}..${/}resource${/}simple_resource.robot
    ${result} =    Parse Json    ${result}
    Copy And Replace Path In File
    ...    ${CURDIR}${/}..${/}resource${/}simple_resource_as.json
    ...    ${OUTPUT_DIR}${/}simple_resource_as.json
    ...    REPLACE_PATH
    ...    ${OUTPUT_DIR}${/}

    ${expected} =    Parse Json From File
    ...    ${CURDIR}${/}..${/}resource${/}simple_resource_as.json
    Compare Dicts    ${result}    ${expected}

Parser Should Be Able To Parse Test Suite
    ${result} =    DataParser.Parse Suite
    ...    ${CURDIR}${/}..${/}resource${/}simple_test.robot
    ${result} =    Parse Json    ${result}
    ${expected} =    Parse Json From File
    ...    ${CURDIR}${/}..${/}resource${/}simple_test_as.json
    Compare Dicts    ${result}    ${expected}

Parser Should Be Able To Parse Variable File
    ${result} =    DataParser.Parse Variable File
    ...    ${CURDIR}${/}..${/}resource${/}simple_var.py
    ${result} =    Parse Json    ${result}
    ${expected} =    Parse Json From File
    ...    ${CURDIR}${/}..${/}resource${/}simple_var_as.json
    Compare Dicts    ${result}    ${expected}

Parser Should Be Able To Parse Internal Library
    ${result} =    DataParser.Parse Library
    ...    BuiltIn
    ${result} =    Parse Json    ${result}
    ${expected} =    Parse Json From File
    ...    ${CURDIR}${/}..${/}resource${/}builtint_as.json
    Compare Dicts    ${result}    ${expected}

Parser Should Be Able To Parse External Library From Python Path
    ${result} =    DataParser.Parse Library
    ...    Selenium2Library
    ${result} =    Parse Json    ${result}
    ${expected} =    Parse Json From File
    ...    ${CURDIR}${/}..${/}resource${/}s2l_as.json
    Compare Dicts    ${result}    ${expected}

Parser Should Be Able To Parse External Library From File
    ${result} =    DataParser.Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}utilities${/}json_to_dictionary.JsonParser
    ${result} =    Parse Json    ${result}
    ${expected} =    Parse Json From File
    ...    ${CURDIR}${/}..${/}resource${/}JsonParser_as.json
    Compare Dicts    ${result}    ${expected}

*** Keywords ***
Copy And Replace Path In File
    [Arguments]    ${source}    ${destination}    ${search_for}    ${replace_to}
    ${source} =    OperatingSystem.Normalize Path    ${source}
    ${destination} =    OperatingSystem.Normalize Path    ${destination}
    ${replace_to} =    OperatingSystem.Normalize Path    ${replace_to}
    ${data} =     OperatingSystem.Get File
    ...    path=${source}
    ${data} =    String.Replace String
    ...    ${data}
    ...    search_for=${search_for}
    ...    replace_with=${replace_to}${/}
    OperatingSystem.Create File
    ...    ${destination}
    ...    ${data}

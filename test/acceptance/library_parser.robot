*** Settings ***
Library           ../../src/dataparser/parser/TestDataParser.py
Library           Collections
Variables         variable_files/library_vars.py

*** Test Cases ***
Parser Should Be Able To Parse Internal Library
    ${result} =    Parse Library
    ...    Screenshot
    Verify Library Results
    ...    ${result}
    ...    ${SCREENSHOT_KW}

Parser Should Be Able To Parse External Library From Python Path
    ${result} =    Parse Library
    ...    Selenium2Library
    Verify Library Results
    ...    ${result}
    ...    ${SELENIUM2LIBRARY_KW}

Parser Should Be Able To Parse External Library From File
    ${result} =    Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}library${/}SwingLibrary-1.9.5.xml
    Verify Library Results
    ...    ${result}
    ...    ${SWINGLIBRARY_KW}

*** Keywords ***
Verify Library Results
    [Arguments]    ${result}    ${expected}
    ${result_keys} =    Get Dictionary Keys    ${result}
    ${screenshot_kw_keys} =    Get Dictionary Keys    ${SCREENSHOT_KW}
    Lists Should Be Equal
    ...    ${result_keys}
    ...    ${screenshot_kw_keys}
    ${result_kws} =    Get From Dictionary
    ...    ${result}
    ...    keywords
    ${expected_kws} =    Get From Dictionary
    ...    ${expected}
    ...    keywords
    ${expected_kws_keys} =    Get Dictionary Keys    ${expected_kws}
    ${result_kws_keys} =    Get Dictionary Keys    ${result_kws}
    Lists Should Be Equal
    ...    ${result_kws_keys}
    ...    ${expected_kws_keys}
    ${result_kws_values} =    Get Dictionary Values    ${result_kws}
    ${expected_kws_values} =    Get Dictionary Values    ${expected_kws}
    ${result_len} =    Get Length    ${result_kws_values}
    ${expected_len} =    Get Length    ${expected_kws_values}
    Should Be Equal As Numbers
    ...    ${result_len}
    ...    ${expected_len}
    :FOR    ${index}    IN RANGE    ${result_len}
    \    Verify Library Keyword
    \    ...    @{result_kws_values}[${index}]
    \    ...    @{expected_kws_values}[${index}]

Verify Library Keyword
    [Arguments]    ${result}    ${expected}
    ${result_keys} =    Get Dictionary Keys    ${result}
    ${expected_keys} =    Get Dictionary Keys    ${expected}
    Lists Should Be Equal
    ...    ${result_keys}
    ...    ${expected_keys}
    ${result_value} =    Get From Dictionary
    ...    ${result}
    ...    keyword_name
    ${expected_value} =    Get From Dictionary
    ...    ${expected}
    ...    keyword_name
    Should Be Equal
    ...    ${result_value}
    ...    ${expected_value}
    ${result_value} =    Get From Dictionary
    ...    ${result}
    ...    tags
    ${expected_value} =    Get From Dictionary
    ...    ${expected}
    ...    tags
    Lists Should Be Equal
    ...    ${result_value}
    ...    ${expected_value}
    ${result_value} =    Get From Dictionary
    ...    ${result}
    ...    documentation
    ${expected_value} =    Get From Dictionary
    ...    ${expected}
    ...    documentation
    Should Start With
    ...    ${result_value}
    ...    ${expected_value}
    ${result_value} =    Get From Dictionary
    ...    ${result}
    ...    keyword_arguments
    ${expected_value} =    Get From Dictionary
    ...    ${expected}
    ...    keyword_arguments
    Lists Should Be Equal
    ...    ${result_value}
    ...    ${expected_value}

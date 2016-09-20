*** Settings ***
Library           data_parser.data_parser.DataParser
Library           Collections
Library           OperatingSystem
Library           String
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
    ${result_keys} =    Get Dictionary Keys    ${result}
    Lists Should Be Equal
    ...    ${result_keys}
    ...    ${SELENIUM2LIBRARY_KEYS_LIST}
    ${keywords} =    Get From Dictionary
    ...    ${result}
    ...    keywords
    ${one_kw} =    Get From Dictionary
    ...    ${keywords}
    ...    add_cookie
    ${one_kw_keys} =    Get Dictionary Keys    ${one_kw}
    Sort List    ${one_kw_keys}
    Sort List    ${ADDCOOKIE_KEYS_LILST}
    Lists Should Be Equal
    ...    ${one_kw_keys}
    ...    ${ADDCOOKIE_KEYS_LILST}

Parser Should Be Able To Parse External Library From Module
    ${result} =    Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}test_data${/}suite_tree${/}LibNoClass.py
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${LIB_FROM_MODULE}

Parser Should Be Able To Parse Library With Robot API Keyword Decorator
    ${lib_path} =    OperatingSystem.Normalize Path    ${CURDIR}${/}..${/}resource${/}test_data${/}suite_tree${/}LibraryWithReallyTooLongName.py
    ${result} =    Parse Library    ${lib_path}
    ${kws} =    Set Variable    &{result}[keywords]
    ${kw_with_deco} =    Set Variable    &{kws}[other_name_here]
    ${lib_path} =    String.Convert To Lowercase    ${lib_path}
    ${lib_path_from_parser} =    String.Convert To Lowercase    &{kw_with_deco}[keyword_file]
    Should Be Equal As Strings
    ...    ${lib_path_from_parser}
    ...    ${lib_path}

Parser Should Be Able To Parse External Library From Custom Location
    ${result} =    Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}library${/}MyLibrary.py
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${MYLIBRARY_KW}

Parser Should Be Able To Parse External Library With Arguments From Custom Location
    @{args} =   Create List    arg111    arg222
    ${result} =    Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}library${/}OtherMyLibrary.py
    ...    ${args}
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${OTHERMYLIBRARY_KW}

Parser Should Be Able To Parse External Library From XML File
    ${result} =    Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}library${/}MyLibrary.xml
    Dictionaries Should Be Equal
    ...    ${result}
    ...    ${MYLIBRARY_XML}

Parser Should Be Not Able To Parse Resource File From XML File
    Run Keyword And Expect Error
    ...    ValueError: XML file is not library: simple_resource
    ...    Parse Library
    ...    ${CURDIR}${/}..${/}resource${/}library${/}simple_resource.xml

*** Keywords ***
Simple Library Results Verifier
    [Arguments]    ${result}    ${expected}
    ${result_keys} =    Get Dictionary Keys    ${result}
    ${expected_kw_keys} =    Get Dictionary Keys    ${expected}
    Lists Should Be Equal
    ...    ${result_keys}
    ...    ${expected_kw_keys}
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
    [Return]    ${result_kws}    ${expected_kws}

Verify Library Results
    [Arguments]    ${result}    ${expected}
    ${result_kws}    ${expected_kws} =    Simple Library Results Verifier
    ...    ${result}
    ...    ${expected}
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

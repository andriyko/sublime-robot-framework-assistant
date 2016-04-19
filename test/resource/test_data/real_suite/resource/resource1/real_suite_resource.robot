*** Settings ***
Library           ../../libs/SuiteLib.py    2
Library           Process
Resource          ../../reosurce2/real_suite_resource.robot
Variables         ../var_file/variables.py    some_arg

*** Variables ***
${REAL_SUITE_VAR}    2

*** Keywords ***
Real Suite User Keyword 1
    Log    1

Real Suite User Keyword 2
    Sl Kw 2
    Log    ${REAL_SUITE_VAR}
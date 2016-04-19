*** Settings ***
Library           com.company.library.CompanyLibrary
Library           ../../libs/SuiteLib.py    1
Library           Selenium2Library    timeout=15.0    run_on_failure=Real Suite User Keyword 4

*** Variables ***
# Comment
${OTHER_REAL_SUITE_VAR}    2

${VAR_AFTER_NEW_LINE}    Tidii

*** Keywords ***
Real Suite User Keyword 3
    Log    1

Real Suite User Keyword 4
    Sl Kw 1
    Log    ${OTHER_REAL_SUITE_VAR}

*** Settings ***
Library           Selenium2Library    timeout=5.0    run_on_failure=Common Keyword 1
Variables         common_variables.py    one    two

*** Keywords ***
Common Keyword 1
    Log    1
    # This is a comment

Common Keyword 2
    Log    2

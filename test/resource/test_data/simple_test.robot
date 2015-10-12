*** Settings ***
Resource          simple_resource.robot

*** Variable ***
${ARG}            1

*** Test Cases ***
Example Test
    My Kw
    Other Kw

*** Keywords ***
Other Kw
    Log    1

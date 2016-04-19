*** Settings ***
Library           OperatingSystem
Library           Process

*** Variables ***
${OTHER_VAR}      1

*** Test Cases ***
Test Case One
    Process.Run Process
    ...    foo
    ...    1

Test Case Two
    OperatingSystem.Count Files In Directory
    ...    /not/hare

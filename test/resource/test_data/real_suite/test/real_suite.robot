*** Settings ***
Resource          ../resource/resource1/real_suite_resource.robot
Resource          ../resource/reosurce2/real_suite_resource.robot
Test Setup        Real Suite User Keyword 3

*** Test Cases ***
Test 1
    Real Suite User Keyword 1
    Real Suite User Keyword 2

Test 2
    Real Suite User Keyword 3
    Real Suite User Keyword 4

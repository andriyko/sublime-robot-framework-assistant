[![Build Status](https://travis-ci.org/aaltat/robotframework-from-sublime.svg?branch=master)]
(https://travis-ci.org/aaltat/robotframework-from-sublime)

Robot Framework Data Editor
==========================
Robot Framework Data Editor provides IDE features to edit
[Robot Framework](http://robotframework.org/) test data in the
[Sublime Text 3](https://www.sublimetext.com/3).

Installation
============
To be done

Configuration
=============
Before yo can start using the Robot Framework Data Editor, you must
at least configure the settings in the
[User package](http://docs.sublimetext.info/en/latest/customization/settings.html)
`RobotFrameworkDataEditor.sublime-settings` file. To Open the file
navigate to: **Preferences | Package settings**
**| Robot Framework Data Editor | Settings - User |**
The default settings can be found from the **Preferences | Package settings**
**| Robot Framework Data Editor | Settings - Default |**

robot_framework_workspace
-------------------------
Before the Robot Framework Data Editor can provide the keyword and
variable completion features, it needs to create a database from the test
suite and resource files. The argument defines the root folder where
scanning of robot data is performed.

Must point to a folder and pointing to a file is not allowed. When
the command `Robot Framework: Create database` is executed,
the scanning of Robot Framework test data is performed based
on this setting.

In windows ow write double backslash to write literal backslash.

robot_framework_extension
-------------------------
File extension defines which types of files the Robot Framework
Data Editor plugin will search from the folder defined
in the robot_framework_workspace option.

This setting affects the plugin commands and features but the theme
definition in this plugin is not affected by this option.

If there library or variable file imports in the Robot Framework data,
those imports are automatically parser and included in the scanning.

path_to_python
-------------
In order the creating the database of keywords and variables to
work, path to Python binary must be defined. It must be the same
Python binary where the Robot Framework is installed.

In Linux like environments this could be like: /usr/bin/python
and in Windows this could be like: C:\\Python27\\python.exe

robot_framework_module_search_path
----------------------------------
Module search path defines a list of paths where the Robot Framework
libraries are searched. Example if you have imported
a library with the library name, then module search path must
contain the folder where the library can be located.

The Robot Framework Data Editor uses the Robot Framework API to parse
the test data and libraries. All changes, which are not system
wide, to locate the libraries, must also be added in the
module search path in the Robot Framework Data Editor

More details how libraries is searched in Robot Framework can be
found from be the
[Robot Framework User guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#module-search-path)

robot_framework_builtin_variables
---------------------------------
Robot Framework comes by default some predefined and builtin variables.
These variables names may change between different Robot Framework
versions. Use this setting to define a list of the Robot Framework BuiltIn
variables. The easiest way to see the list of the variables is to run
Robot Framework with following test case:

| *** Test Cases *** |   |
| --- |--- |
| Log All BuiltIn Vars |
|   | Log Variables |

Note: At least on Robot Framework 2.9.2 version, the following command
did not list the empty variables, like ${EMPTY}.

Syntax definitions
==================

By default this plugin will be used with files which extension is
`.robot` and plugin will use four spaces as cell separator. The
settings can be changed by user, but consult the
[Sublime unofficial documentation](http://docs.sublimetext.info/en/latest/customization/customization.html)
where the user settings should be saved.

Change the file extension
-------------------------
The file extension is defined in the
`RobotFrameworkDataEditor.tmLanguage` file. To change file extension,
navigate to the
[User package](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-packages-directory)
folder and open the `RobotFrameworkDataEditor.tmLanguage` file.

Look for the lines containing:
```xml
<key>fileTypes</key>
    <array>
        <string>robot</string>
    </array>
```
The `<string>` element contains the file type definition.

Change the cell separator
-------------------------
The cell separator is defined in the
`RobotFrameworkDataEditor.tmPreferences` file. To change the cell separator,
navigate to the
[User package](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-packages-directory)
folder and open the `RobotFrameworkDataEditor.tmPreferences` file.

Look for the line containing `<string><![CDATA[    ]]></string>` XML tag. There are four
spaces inside of the `[    ]` characters and those four spaces defines the cell separator which is
user by the plugin. The cell separator is example used by the for loop
[snippets](http://docs.sublimetext.info/en/latest/extensibility/snippets.html?highlight=snippets)
to align and display snipped correctly.

Hotkeys
=======
* Pressing `Alt + Enter` or `Alt + Click` with mouse, on top of the keyword
will go to the keyword source. Source of the keyword can locate in
Robot Framework test data or in a Python library. Go to does not work
on libraries written in other programming languages.
* Pressing `Ctrl + Alt + Enter`or `Ctrl + Alt + Clicl` with mouse
will display the keyword documentation.

Snippets
========
[Snippets](http://docs.sublimetext.info/en/latest/extensibility/snippets.html?highlight=snippets)
are a Sublime Text feature to provide commonly used text templates
and in this plugin, snippets offers quick access to
the commonly used settings in the Robot Framework data. To gain access
to the snippets write the required character combination and then
press the `Tab` key to see the snippets completion list. The snippets
can be accessed with following key combinations:
* Write `:f` to access Robot Framework for loops. There currently
are available the following snippets:
[normal](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#normal-for-loop),
[enumerate](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#for-in-enumerate-loop),
[range](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#for-in-range-loop)
and [zip](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#for-in-zip-loop)
loops types.
* Write `*k` to access `*** Keywords ***` table snippet.
* Write `*s` to acess `*** Settings ***` table and it settings. There
currently are available the following snippets:
`Default Tags`, `Documentation`, `Library`, `Resource`,
`*** Settings ***`, `Test Setup`, `Test Teardown`, `Test Template`
and `Test Timeout`.
* Write `*t` to access `*** Test Cases ***` table snippet.
* Write `:`to access
[Keyword](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#id331)
and
[Test Case](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#test-case-table)
settings. There currently are available the following snippets::
`[Arguments]`, `[Documentation]`, `[Return]` `[Tags]`, `[Teardown]`
and `[Timeout]`.
* Write `*v` to access `*** Variables ***` snippet.

The different for loop snippets uses the
[fields](http://docs.sublimetext.info/en/latest/extensibility/snippets.html?highlight=snippets#fields)
feature from the snippets. After completing the for loop snippry, the different
for loops fields can be accessed by pressing the `tab` key.

Please note that plugin does not prevent the user to place snippets
in invalid places in the test data.
Please refer to the Robot Framework
[User Guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
to locate the correct usage of the different available snippets.

Creating a database
=====================

Log file
--------

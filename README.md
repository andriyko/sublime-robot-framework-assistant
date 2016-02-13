[![Build Status](https://travis-ci.org/aaltat/robotframework-from-sublime.svg?branch=master)]
(https://travis-ci.org/aaltat/robotframework-from-sublime)

Robot Framework Data Editor
==========================
Robot Framework Data Editor provides IDE features to edit
[Robot Framework](http://robotframework.org/) data.

Configuration
=============
Before yo can start using the Robot Framework Data Editor, you must
at least configure the settings in the
[User package](http://docs.sublimetext.info/en/latest/customization/settings.html)
`RobotFrameworkDataEditor.sublime-settings` file. To Open the file
navigate to: **Preferences | Package settings**
**| Robot Framework Data Editor | Settings - User |**

robot_framework_workspace
-------------------------
Before the Robot Framework Data Editor can provide the keyword and
variable completion features, it needs to scan and index the test
suite and resource files. The argument defines the root folder where
scanning of robot data is performed.

Must point to a folder, pointing to a file is not allowed. When the command
`Robot Framework: Scan and Index` is executed, the scanning is performed
based on this setting.

In windows ow write double backslash to write literal backslash.

robot_frameowrk_extension
-------------------------
File extension defines which types of files the Robot Framework
Data Editor plugin will search and index from the folder defined
in the robot_framework_workspace option.

This only affects the `Robot Framework: Scan and Index` command,
other options, like theme definition, in this plugin are not affected by
this option.

If there library or variable imports in the Robot Framework data,
those imports are automatically parser and included in the scanning.

path_to_python
-------------
In order the scanning and indexing of keywords and variables to
work, path to python binary must be defined. It must be the same
Python binary where the Robot Framework is installed.

In Linux like environments this could be like: /usr/bin/python
and in Windows this could be like: C:\Python27\python.exe

robot_framework_module_search_path
----------------------------------
Module search path defines a list of paths where the Robot Framework libraries
are searched. Example if you have imported
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
versions. Use this setting to define a list of the Robot Framework BuiltIn variables.
The easiest way to see the listof  the variables is to run Robot Framework with following
test case:

| *** Test Cases *** |   |
| --- |--- |
| Log All BuiltIn Vars |
|   | Log Variables |

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
The `<string>` element contains the filetype defintion.

Change the cell separator
-------------------------
The cell separator is defined in the
`RobotFrameworkDataEditor.tmPreferences` file. To change the cell separator,
navigate to the
[User package](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-packages-directory)
folder and open the `RobotFrameworkDataEditor.tmPreferences` file.

Look for the line containing `<string><![CDATA[    ]]></string>` XML tag. There are four
spaces inside of the `[    ]` characters and those four spaces defines the cell separator which is
user by the pluging. The cell separator is example used by the for loop
[snippets](http://docs.sublimetext.info/en/latest/extensibility/snippets.html?highlight=snippets)
to align and display snipped correctly.

Scanning and indexing
=====================

Log file
--------


Hotkeys
=======

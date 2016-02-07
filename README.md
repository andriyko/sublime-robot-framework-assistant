[![Build Status](https://travis-ci.org/aaltat/robotframework-from-sublime.svg?branch=master)]
(https://travis-ci.org/aaltat/robotframework-from-sublime)

Robot Framework Data Editor
==========================
Robot Framework Data Editor provides IDE features to edit
[Robot Framework](http://robotframework.org/).

Configuration
=============
Before yo can start using the Robot Framework Data Editor, you must configure
the pluging.

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


Scanning and indexing
=====================

Log file
--------


Hotkeys
=======

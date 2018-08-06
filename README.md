[![Build Status](https://travis-ci.org/andriyko/sublime-robot-framework-assistant.svg?branch=master)](https://travis-ci.org/andriyko/sublime-robot-framework-assistant)

# Robot Framework Assistant
Robot Framework Assistant provides IDE features to edit
[Robot Framework](http://robotframework.org/) test data in the
[Sublime Text 3](https://www.sublimetext.com/3).

From release 3.0.0 onwards plugin is not anymore compatible with
Sublime Text 2. The releases made before the 3.0.0 will serve
the Sublime Text 2 users. The documentation for Sublime Text 2 user
can be found from st2-maintenance branch
[README](https://github.com/andriyko/sublime-robot-framework-assistant/blob/st2-maintenance/README.md)

This project is currently looking for a maintainer.

# Installation
The easiest way to install is to use
[Package Control](https://packagecontrol.io/) and search for:
`Robot Framework Assistant`.

## Alternative installation methods
Download the plugin as a zip. Open Sublime Text and click
**| Preferences | Browse Packages |** to open the packages directory.
Then create a directory named `Robot Framework Assistant` and
unzip the plugin to the directory.

# Configuration
Before yo can start using the Robot Framework Assistant, you must
at least configure the settings in the
[User package](http://docs.sublimetext.info/en/latest/customization/settings.html)
`Robot.sublime-settings` file. To Open the file
navigate to: **Preferences | Package settings**
**| Robot Framework Assistant | Settings - User |**
The default settings can be found from the **Preferences | Package settings**
**| Robot Framework Assistant | Settings - Default |**

The only mandatory settings which user needs to define are the
[robot_framework_workspace](https://github.com/andriyko/sublime-robot-framework-assistant#robot_framework_workspace)
and the
[path_to_python](https://github.com/andriyko/sublime-robot-framework-assistant#path_to_python).
The rest of the parameters can be safely left in their default values,
when trying out the plugin.

## robot_framework_workspace
Before the Robot Framework Assistant can provide the keyword and
variable completion features, it needs to create a database from the test
suite and resource files. The argument defines the root folder where
scanning of robot data is performed.

Must point to a folder and pointing to a file is not allowed. When
the command `Robot Framework: Create database` is executed,
the scanning of Robot Framework test data is performed based
on this setting.

In windows ow write double backslash to write literal backslash.

## robot_framework_keyword_argument_format
Defines how keyword argument are formatted when keyword
completion is used. When set to false, each argument is
formatted to individual lines. If set to true keyword
and arguments are returned in single line.

## robot_framework_extension
File extension defines which types of files the Robot Framework
Assistant plugin will search from the folder defined
in the robot_framework_workspace option.

This setting affects the plugin commands and features but the theme
definition in this plugin is not affected by this option.

If there library or variable file imports in the Robot Framework data,
those imports are automatically parser and included in the scanning.

## path_to_python
In order the creating the database of keywords and variables to
work, path to Python binary must be defined. It must be the same
Python binary where the Robot Framework is installed.

In Linux like environments this could be like: /usr/bin/python
and in Windows this could be like: C:\\Python27\\python.exe

## robot_framework_module_search_path
Module search path defines a list of paths where the Robot Framework
libraries are searched. Example if you have imported
a library with the library name, then module search path must
contain the folder where the library can be located.

The Robot Framework Assistant uses the Robot Framework API to parse
the test data and libraries. All changes, which are not system
wide, to locate the libraries, must also be added in the
module search path in the Robot Framework Assistant

More details how libraries is searched in Robot Framework can be
found from be the
[Robot Framework User guide](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#module-search-path)

## robot_framework_automatic_database_table
The robot_framework_automatic_database_table setting controls the
internal database updating. If the set to true, the internal
database tables are created after a Robot Framework test data
file is saved. If set to false, the internal database tables are
only updated when the `Create Database`, `Create Database Tables` or
`Update Internal Database For Active Tab` commands are run.

The setting only controls the Robot Framework test data. If a
libraries or a variable files are updated, then `Create Database`
or `Create Database Tables` commands must be run to update the
internal database.

## robot_framework_library_in_xml
When a library is not available during parsing time,
example if library is imported with Remote library interface or
it is not written in Python like the
[SwingLibrary](https://github.com/robotframework/SwingLibrary)
Then this setting can be used to import libraries in
[libdoc](http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#library-documentation-tool-libdoc)
XML format.

Libraries found from the this path are globally available, like the
BuiltIn library. Example the keyword completion will work although
the library may not imported for that particular resource or test suite.

## robot_framework_builtin_variables
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

## robot_framework_database_path
By default internal database is created in plugin installation
directory, in database folder. Sometimes it could be useful to
change the default database location.

Example if the robot_framework_workspace is defined in the
Sublime workspace file and user wants to change between
different projects. Then it is useful to define
robot_framework_database_path setting also be project specific.
When the internal database is project specific, user does not
recreate the database when the project is changed.

The robot_framework_database_path must be a path to a folder.
If the setting is not path to a folder, then the database
is created in the plugin installation directory.

## robot_framework_log_commands
Setting controls will the `Robot Framework: Command Logging`
command enable or disable the Sublime Text log_commands API call.
If the robot_framework_log_commands setting evaluates as Python
True, then log_commands API call is enabled. If setting
evaluates as Python False, log_commands API call is disabled.

If log_commands API call is enabled. all commands run from key
bindings and the menu will be logged to the console.

To enabled the logging, set the `robot_framework_log_commands` to value
`true`. Then run the `Robot Framework: Command Logging` command
from command palette.

## robot_framework_keyword_prefixes
Prefixes that are ignored in `jump to keyword` command.

When writing testcases in Gherkin keywords have prefixes like `given`, `when` and `then`.
Such prefixes are testcase specific and must be ignored when looking up a keyword.

Configuration for typical Gherkin stories:
"robot_framework_keyword_prefixes" : ["Given","When","Then","And","But"]

# Syntax definitions
By default this plugin will be used with files which extension is
`.robot` and plugin will use four spaces as cell separator. The
settings can be changed by user, but consult the
[Sublime unofficial documentation](http://docs.sublimetext.info/en/latest/customization/customization.html)
where the user settings should be saved.

## Change the file extension
The file extension is defined in the
`Robot.tmLanguage` file. To change file extension,
navigate to the
[User package](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-packages-directory)
folder and copy the `Robot.tmLanguage` file in to the
user settings folder.

In the `Robot.tmLanguage` file in user settings,  look for the lines containing:
```xml
<key>fileTypes</key>
    <array>
        <string>robot</string>
    </array>
```
The `<string>` element contains the file type definition.

## Change the cell separator
The cell separator is defined in the
`Robot.tmPreferences` file. To change the cell separator,
navigate to the
[User package](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-packages-directory)
folder and open the `Robot.tmPreferences` file.

Look for the line containing `<string><![CDATA[    ]]></string>` XML tag. There are four
spaces inside of the `[    ]` characters and those four spaces defines the cell separator which is
user by the plugin. The cell separator is example used by the for loop
[snippets](http://docs.sublimetext.info/en/latest/extensibility/snippets.html?highlight=snippets)
to align and display snipped correctly.

# Hotkeys
* Pressing `Alt + Enter` or `Alt + Click` with mouse, on top of the keyword
will go to the keyword source. Source of the keyword can locate in
Robot Framework test data or in a Python library. Go to does not work
on libraries written in other programming languages.
* Pressing `Alt + Enter` or `Alt + Click` with mouse, on top of the resource
or library import will open the imported resource or library file.
* Pressing `Ctrl + Alt + Enter`or `Ctrl + Alt + Clicl` with mouse
will display the keyword documentation.
* Pressing `Ctrl + /` or `Ctrl + Shift + /` will togle comment on and off
* Pressing `Ctrl + Alt + a` will run the `Robot Framework: Create Database` command
* Pressing `Ctrl + Alt + s` will run the `Robot Framework: Create Database Tables` command
* Pressing `Ctrl + Alt + i` will run the `Robot Framework: Update Internal Database For Active Tab` command
* Pressing `Ctrl + Alt + r` will show available library, resource or variables imports in a popup menu. The popup
menu is only displayed if cursor is in settings table and line contains `Libraries`, `Resource` or `Variables` setting.

The usage of the `Ctrl + Alt + a/s/i` commands is explained in the
[Internal database for keywords and variables](https://github.com/andriyko/sublime-robot-framework-assistant/wiki/Internal-database-for-keywords-and-variables) wiki page

# Snippets
[Snippets](http://docs.sublimetext.info/en/latest/extensibility/snippets.html?highlight=snippets)
are a Sublime Text feature to provide commonly used text templates
and in this plugin, snippets offers quick access to
the commonly used settings in the Robot Framework data. To gain access
to the snippets write the required character combination. If the snippet
is not displayed press the `Tab` key to see the snippets completion list.
The snippets can be accessed with following key combinations:
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
`[Arguments]`, `[Documentation]`, `[Return]`, `[Setup]`, `[Tags]`, `[Template]`, `[Teardown]`
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

# Go To Keyword
Alternatively, use Sublime Text's
[Go To Symbol](http://docs.sublimetext.info/en/latest/file_management/file_management.html#fm-goto-symbol)
to go to the source of a keyword or a variable.

Please note that `Go To Symbol` only works for keywords and variables
within the same file. It is not possible to use `Go To Symbol` to
jump a keyword or a variable in other resource files or in libraries.

# Creating a database
Once the plugin configuration is done, the plugin needs to scan the
test data to create a internal database to the package directory.
The database will contain table for each test case, resource and
library. Once the tables has been created, plugin will create a
index for each test case, resource and library. Index will contain
all keywords and variables, what the test case or resource has imported
in the test data. Indexing allows plugin to provide completion
to only those keyword or variables which has been imported for
the currently opened test or resource file.

The plugin will automatically update the pointer to the index in the
database, when user will change between different tabs in the Sublime.

More detailed description how to update the internal database can
be found from the
[Internal database for keywords and variables](https://github.com/andriyko/sublime-robot-framework-assistant/wiki/Internal-database-for-keywords-and-variables)
wiki page.

## Error investigation for database creation
When creating the database, plugin will write a log file
to the package installation directory: `database/scan_index.log`
file. If there are errors when the database is created,
please check the log and correct possible errors.

# Project specific settings
It is also possible to use project specific setting when configuring
the Robot Framework Assistant.

Open the project setting and add `robot_framework_assistant` dictionary
to the settings file:
```
"robot_framework_assistant":
    {

    }

```
Example if configuring project specific workspace and database paths,
the `robot_framework_assistant` dictionary should look like this:

```
"robot_framework_assistant":
    {
        "robot_framework_workspace": "/path/to/folder/containing/robot/data",
        "robot_framework_database_path": "/path/to/project/database"
    }

```

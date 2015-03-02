sublime-robot-framework-assistant
=================================

*Robot Framework Assistant* - is a plugin for [Sublime Text 2](http://www.sublimetext.com/2) / [Sublime Text3](http://www.sublimetext.com/3) that provides some conveniences for working with [Robot Framework](http://robotframework.org/) test files (.txt and .robot).

Optionally, can work with [http://rfdocs.org/](http://rfdocs.org/).

- [Installation](#installation)
    - [Alternative installation methods](#alternative-installation-methods)
        - [From github](#from-github)
        - [Manually](#manually)
- [Features](#features)
- [Configuration](#configuration)
	- [Edit Settings](#edit-settings)
	- [Edit Scanners](#edit-scanners)
- [Usage](#usage)
	- [Settings](#settings)
	- [Scanners](#scanners)
	- [Set Syntax](#set-syntax)
	- [Scan](#scan)
	- [Reindex data](#reindex-data)
    - [RFDocs](#rfdocs)
        - [Download Manifest](#download-manifest)
        - [Download Packages](#download-packages)
        - [Show manifest](#show-manifest)
        - [Show packages](#show-packages)
        - [Validate packages](#validate-packages)
- [Rflint](#rflint)
- [Screenshots](#screenshots)

Installation
------------

The easiest way to install is to use [Package Control](http://wbond.net/sublime_packages/package_control) and search for `Robot Framework Assistant`.

### Alternative installation methods

Otherwise, open Sublime Text and click `Preferences -> Browse Packages` to open the packages directory. Then create a directory named **Robot Framework Assistant** containing the contents of this repository.

#### From github

To get the contents of this repository:

    git clone git://github.com/andriyko/sublime-robot-framework-assistant.git

#### Manually

[Download](https://github.com/andriyko/sublime-robot-framework-assistant/archive/master.zip)
the plugin as a zip. Copy the content of the downloaded archive into **Robot Framework Assistant** directory (see previous section).

Features
--------
**Note:** term *item* means either *Python Library*, *Resource File*, *Keyword* (from *Python Library* or *Resource File*) or *Variable*.

* Syntax highlighting/automatic detection/activation for Robot Framework '.txt' and '.robot' files;
* `Alt+Enter` or `Alt+Click` to go to source of item at caret (either *Library*, *Resource*, *Keyword* or *Variable*);
* `Ctrl+Alt+Enter` or `Ctrl+Alt+Click` on item to log *Keyword* documentation or value of *Variable* into output panel.
* `Ctrl+Space` to auto complete library/resource name, keywords (can start with any part/word of keyword). Using of '.' after library/resource name is also supported (limits keywords to given library/resource);
* Autocomplete gives *Keyword* with its *arguments* formatted according to Robot Framework syntax. Jump through arguments with `TAB` key.
* `$` or `@` for autocomplete of *Built-in* and *Resource* variables (NOTE: as for now reading of *Variables files* is not supported);
* `:` and then `TAB` to get list of special Robot Framework syntax elements (like *[Arguments]*, *[Return]* etc);
* `:f` and then `TAB` to insert *:FOR* loop template;
* `*k`, `*s`, `*v` and then `TAB` to insert tables hedings templates (*\*\*\* Keywords \*\*\**, *\*\*\* Settings \*\*\**, *\*\*\* Variables \*\*\**)
* Toggle comments with `Cmd+/`;
* `Cmd+B` to run *pybot* with current file;
* Separate `Robot Framework` menu in Sublime Text main menu.
* `Robot Framework` context menu which allows to run *pybot* with current file, scan libraries/resources, insert snippets etc.

Depending on your OS, you may have another key binding for autocomplete. For example in order to have autocomplete bound to `Ctrl+Space` on Linux, add these lines to User key bindings (`Preferences > Key Bindings - User`):

```
[
	{ "keys": ["ctrl+space"], "command": "auto_complete" },
	{ "keys": ["ctrl+space"], "command": "replace_completion_with_auto_complete", "context":
	    [
	        { "key": "last_command", "operator": "equal", "operand": "insert_best_completion" },
	        { "key": "auto_complete_visible", "operator": "equal", "operand": false },
	        { "key": "setting.tab_completion", "operator": "equal", "operand": true }
	    ]
	}
]
```

Configuration
-------------

### Edit Settings
(`Robot Framework > Settings` or use command palette).
***You have to define `python_interpreter` option manually. Should point to Python installation with *Robot Framework* packages.***. An example of settings:

```
{
	"associated_file_extensions":
	[
		".txt",
		".robot"
	],
	"log_level": "error",
	"python_interpreter": "python",
	"rfdocs_update_url": "http://rfdocs.org/dataset/download?",
	"separator":
	{
		"between_args": "...  ",
		"between_kw_and_args": "  ",
		"kw_and_args_one_line": false
	},
	"show_version_in_autocomplete_box": true
}
```
By defaults autocomplete formats keyword and arguments as below:

```
Call Method
...  object
...  method_name
...  *args
```
To have keyword and arguments all in one line change `separator` options:

```
"separator":
{
    "between_args": "    ",
	"between_kw_and_args": "    ",
	"kw_and_args_one_line": true
}
```
results to

```
Call Method    object    method_name    *args
```
or

```
"separator":
{
    "between_args": " | ",
	"between_kw_and_args": "  ",
	"kw_and_args_one_line": true
}
```
gives:

```
Call Method | object | method_name | *args
```

Ensure that `python_interpreter` option is correct:

```
$ /Users/username/.virtualenvs/robotframework/bin/python
>>> import robot
>>> robot.__version__
'2.8.3'
```

### Edit Scanners
(`Robot Framework > Scanners` or use command palette)

Basically you will need to define only `path` option for `resource_scanners` setting. Set `is_active` to *false* if you need to disable parser.

`paths` (optional) - defines list of paths to append with *sys.path.append*.

`pylib_scanners` - defines what `parser` to use for `libraries` from `package`.

First dictionary from example is equivalent to:

```
>>> from robot.libraries import BuiltIn, OperatingSystem, Collections, Telnet, XML, Dialogs, String, Process, Screenshot, Remote
```
Second is equivalent to:

```
>>> import SeleniumLibrary, SSHLibrary, Selenium2Library
```

`resource_scanners` - set `path` option that points to your *Robot Framework* resources directory.

`testcase_scanner` - defines parser to use for currently opened '.txt' or '.robot' file.

An example of scanners configuration:

```
{
    "paths":
        [
        ],

    "pylib_scanners": [
            {
                "parser": "scanners.standard.PythonLibsScannerStandard",
                "libraries": ["BuiltIn", "OperatingSystem", "Collections",
                              "Telnet", "XML", "Dialogs",
                              "String", "Process", "Screenshot", "Remote"],
                "is_active": true,
                "package": "robot.libraries"
            },
            {
                "parser": "user_scanners.external.PythonLibsScannerExternal",
                "libraries": ["SeleniumLibrary", "SSHLibrary", "Selenium2Library"],
                "is_active": false,
                "package": ""
            }
        ],
    "resource_scanners": [
        {
            "parser": "scanners.standard.ResourceFilesScannerStandard",
            "path": "/path/to/resources/directory/or/file",
            "is_active": false
        }
    ],
    "testcase_scanner":
        {
            "parser": "scanners.standard.TestCaseFilesScannerStandard",
            "is_active": true
        }
}
```

You can configure scanning of your own libraries in the same way as shown above. Or prepare customized scanner and put it under `user scanners` module.
After changes made - either rescan and reindex data files or restart Sublime Text.

Usage
-----
There are several ways to execute certain command:

* *command palette* (`Tools > Command Palette` menu item or use keys binding `Ctrl+Shift+P`, type **Robot Framework Assistant**);
* `Robot Framework` main menu;
* `Robot Framework` menu item from context menu (right mouse click).


### Settings
Edit main settings.

### Scanners
Edit scanners file.

### Set Syntax
Set Robot Framework syntax highlighting (works for *.txt* and *.robot* files).

### Scan
Scan *Python libraries*, *Resource files* and *current test file*.
In order to have *User Keywords* and *Variables* data from current file, first scan current file (`Robot Framework > Scan > Current file` or `Ctrl+Alt+S`) and then `Save File`.

### Reindex data
(Re)index all files under `robot_data` directory. Indexing of files is done automatically on plugin load (if current view is Robot Framework test file). Invoke this command manually if you need to update data for features like autocomplete.

### RFDocs (optional)

##### Download Manifest
Download file that contains list of packages (libraries) from `rfdocs_update_url` URL.

##### Download Packages
Download packages (libraries) according to downloaded manifest file.

##### Show manifest
Shows manifest file that is currently used when downloading packages(libraries).

##### Show packages
Opens directory that contains files (*.json*) downloaded from rfdocs.org.

##### Validate packages
Compares data from manifest file to actual downloaded and extracted data (ensures that *zip* files were unpacked without errors).

Rflint
------------
It is also possible to run [rflint](https://github.com/boakley/robotframework-lint) directly from Sublime Text. For details about installation and configuration of the rflint see the [rflint wiki](https://github.com/boakley/robotframework-lint/wiki) and the rflint [readme file](https://github.com/boakley/robotframework-lint/blob/master/README.md).

This plugin provides to different ways to use rflint:

* There git integration which as two different options.
    * Run rflint against changed and staged files in the git working space.
    * Run rflint against the changed, staged and new files in the git working space.
* It is possible to run rflint against the currently opened file.

### Rflint specific configuration
To install rflint, please refer to the rflint [readme file](https://github.com/boakley/robotframework-lint/blob/master/README.md).

#### Git integration
To be able to use the git integration, git must be available from the command line. In windows it is not enough to be able run git from the Git Bash, it must be able to run git from the command prompt.

Also user must configure the path to the git repository (folder where the .git folder is located). To open the configuration file, select: `Robot Framework > Rflint > Rflint Settings` or use the command palette (`Ctrl + p` and type: `rflint settings`) to open the rflint settings file.

In the file configure a path to your git repository where the robot framework test date is version controlled. Example:
```
{
    "git_repo": "/path/to/git_repo"
}
```

Screenshots
-----------
<a href="http://imgur.com/n5pNimh"><img src="http://i.imgur.com/n5pNimh.png" title="sublime-robot-framework-assistant screenshot" /></a>

Some features in action.
<a href="http://imgur.com/ebIk1Pk"><img src="http://i.imgur.com/ebIk1Pk.gif" title="sublime-robot-framework-assistant in action" /></a>

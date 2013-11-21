sublime-robot-framework-assistant
=================================

*Robot Framework Assistant* - is a plugin for [Sublime Text 2](http://www.sublimetext.com/2) / [Sublime Text3](http://www.sublimetext.com/3) that provides some conveniences for working with [Robot Framework](http://robotframework.org/) test files (.txt and .robot).

By default this plugin is configured to work with [http://rfdocs.org/](http://rfdocs.org/).

- [Installation](#installation)
    - [Alternative installation methods](#alternative-installation-methods)
        - [From github](#from-github)
        - [Manually](#manually)
- [Features](#features)
- [Usage](#usage)
    - [The list of available commands](#the-list-of-available-commands)
        - [Manage](#manage)
        - [Download Manifest](#download-manifest)
        - [Download Packages](#download-packages)
        - [Reindex packages](#reindex-packages)
        - [Show manifest](#show-manifest)
        - [Show packages](#show-packages)
        - [Validate packages](#validate-packages)
        - [Set Syntax](#set-syntax)
- [Other](#other)
- [Screenshots](#screenshots)

Installation
------------

The easiest way to install is to use [Package Control](http://wbond.net/sublime_packages/package_control) and search for `Robot Framework Assistant`.

### Alternative installation methods

Otherwise, open Sublime Text and click `Preferences -> Browse Packages` to open the packages directory. Then create a directory named **RobotFrameworkAssistant** containing the contents of this repository.

#### From github

To get the contents of this repository:

    git clone git://github.com/andriyko/sublime-robot-framework-assistant.git

#### Manually

[Download](https://github.com/andriyko/sublime-robot-framework-assistant/archive/master.zip)
the plugin as a zip. Copy the **RobotFrameworkAssistant** directory to its location
(see prior section).

Features
--------

* Syntax highlighting/automatic detection/activation for Robot Framework '.txt' and '.robot' files;
* `Alt+Enter` or `Alt+Click` to go to documentation of keyword at caret (opens browser);
* `Ctrl+Alt+Enter` or `Ctrl+Alt+Click` to fecth *Keyword's* documentation into current view. The documentation is converted from HTML into Plain Text with formating preserved;
* `Ctrl+Space` to auto complete keywords (can start with any part/word of keyword);
* Autocomplete gives *Keyword* with its *arguments* formatted according to Robot Framework syntax;
* Toggle Comments with `Cmd+/`.

**Note:** Depending on your OS, you may have another key binding for autocomplete. For example in order to have autocomplete bound to `Ctrl+Space` on Linux, add these lines to User key bindings (`Preferences > Key Bindings - User`):

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

Usage
-----
Note: to invoke a *command pallete* use `Tools > Command Palette` menu item or use keys binding `Ctrl+Shift+P`. Next type **Robot Framework Assistant** to get list of commadns for this plugin.

### The list of available commands

#### Manage
This is an example of base default settings:

```
{
"libs_dir": "/Users/username/Library/Application Support/Sublime Text 3/Packages/RobotFrameworkAssistant/robot_data/libs",
	"libs_manifest": "/Users/username/Library/Application Support/Sublime Text 3/Packages/RobotFrameworkAssistant/robot_data/libs_manifest.json",
	"libs_update_url": "http://rfdocs.org/dataset/download?",
	"show_library_before_version": true,
	"show_version_in_autocomplete_box": true
}
```

A `libs_update_url` option can be something like this: *http://rfdocs.org/dataset/download?version=Robot+2.6.3*, allows to limit packages to 'Robot 2.6.3' only.

#### Download Manifest
Download file that contains list of packages(libraries) from `libs_update_url` URL.
The snippet of such file:

```
[
    {
        "url": "http://rfdocs.org/media/libraries/archive/robot-2.7.7.zip", 
        "content": [
            {
                "url": "http://rfdocs.org/media/libraries/json/robot-2.7.7/seleniumlibrary.json", 
                "file": "seleniumlibrary.json", 
                "md5": "cf2f24292464146ca574e2916e07da1c"
            }, 
            {
                "url": "http://rfdocs.org/media/libraries/json/robot-2.7.7/string.json", 
                "file": "string.json", 
                "md5": "769f75203581fbb81b02ded7e35f2e86"
            }
        ], 
        "name": "Robot 2.7.7"
    } 
]
```

#### Download Packages
Download packages (libraries) according to `libs_manifest` file contents.

#### Reindex packages
(Re)index all files under `libs_dir` directory. Indexing of files is done automatically on plugin load (if current view is Robot Framework test file). Invoke this command manually if you need to update data for features like autocomplete.

#### Show manifest
Shows manifest `libs_manifest` file which is currently used when downloading packages(libraries) files.

#### Show packages
Opens `libs_dir` directory that contains Libraries files (*.json*).

#### Validate packages
Compares data from manifest `libs_manifest` file to actual data which is present under `libs_dir` directory (ensures that *zip* files were unpacked without errors).

#### Set Syntax
Set Robot Framework syntax highlighting (works for *.txt* and *.robot* files).

Other
-----
Some suggestions on Sublime Text environment settings. Put these lines into your 'User' settings file (`Preferences > Settings - User`)

```
{
	"draw_white_space": "all",
	"trim_trailing_white_space_on_save": true,
	"ensure_newline_at_eof_on_save": true
}
```

Screenshots
-----------
<a href="http://imgur.com/g46Mq1P"><img src="http://i.imgur.com/g46Mq1Pl.png" title="sublime-robot-framework-assistant screenshot"/></a>

An example of autocomplete and auto-foramting, inline and external documentation etc.
<a href="http://imgur.com/UDs43N1"><img src="http://i.imgur.com/UDs43N1.gif" title="sublime-robot-framework-assistant screenshot"/></a>
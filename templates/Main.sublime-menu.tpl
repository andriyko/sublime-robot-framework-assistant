[
    {

        "id": "preferences",
        "children":
        [
            {
                "caption": "Package Settings",
                "mnemonic": "P",
                "id": "package-settings",
                "children":
                [
                    {
                        "caption": "Robot Framework Assistant",
                        "children":
                        [
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/$package_folder/Robot.sublime-settings"},
                                "caption": "Settings - Default"
                            },
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/User/Robot.sublime-settings"},
                                "caption": "Settings – User"
                            },
                            { "caption": "-" },
                            {
                                "command": "scan_index",
                                "caption": "Create Database"
                            },
                            {
                                "command": "scan",
                                "caption": "Create Database Tables"
                            },
                            {
                                "command": "scan_and_index_open_tab",
                                "caption": "Update Internal Database For Active Tab"
                            },
                            { "caption": "-" },
                            {
                                "command": "setting_importer",
                                "caption": "Setting Importer"
                            },
                            { "caption": "-" },
                            {
                                "caption": "Edit Build Configuration",
                                "command": "open_file",
                                "args":
                                    {
                                        "file": "${packages}/$package_folder/Robot.sublime-build"
                                    }
                            },
                            { "caption": "-" },
                            {
                                "command": "log_commands",
                                "caption": "Command Logging"
                            },
                            {
                                "command": "open_log_file",
                                "caption": "Open Log File"
                            },
                        ]
                    }
                ]
            }
        ]
    }
]
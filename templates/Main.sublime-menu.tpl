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
                        "caption": "Robot Framework Data Editor",
                        "children":
                        [
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/$package_folder/RobotFrameworkDataEditor.sublime-settings"},
                                "caption": "Settings - Default"
                            },
                            {
                                "command": "open_file",
                                "args": {"file": "${packages}/User/RobotFrameworkDataEditor.sublime-settings"},
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
                                "command": "scan_open_tab",
                                "caption": "Create Database Table From Active Tab"
                            }

                        ]
                    }
                ]
            }
        ]
    }
]
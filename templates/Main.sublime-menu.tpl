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
                                "caption": "Scan and index all Robot data from worksace"
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
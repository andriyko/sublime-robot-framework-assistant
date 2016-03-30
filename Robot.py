"""
Robot Framework from sublime is a autocompletion plugin for Sublime Text 3
"""
import sys
import os
from string import Template
from .commands import *

if sys.version_info < (3, 3):
    raise RuntimeError('Plugin only works with Sublime Text 3')


def plugin_loaded():
    package_folder = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(package_folder, 'Main.sublime-menu')):
        template_file = os.path.join(
            package_folder, 'templates', 'Main.sublime-menu.tpl'
        )
        with open(template_file, 'r', encoding='utf8') as tplfile:
            template = Template(tplfile.read())

        menu_file = os.path.join(package_folder, 'Main.sublime-menu')
        with open(menu_file, 'w', encoding='utf8') as menu:
            menu.write(template.safe_substitute({
                'package_folder': os.path.basename(package_folder)
            }))

#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

import os
import sys
import inspect
import imp
import importlib


class Module:
    """Module to add commands/functionality to the bot."""

    def commands(self):
        command_list = {}
        if 'commands' not in self.events:
            return command_list

        for command in self.events['commands']:
            command_list[command] = self.events['commands'][command]

        return command_list


class Modules:
    """Manages goshubot's modules."""

    def __init__(self, bot):
        self.bot = bot
        self.modules = {}
        self.paths = []

    def add_path(self, path):
        if not path in sys.path:
            self.paths.append(path)
            sys.path.insert(0, path)

    def modules_from_path(self, path):
        modules = []
        for(dirpath, dirs, files) in os.walk(path):
            for file in files:
                (name, ext) = os.path.splitext(file)
                if ext == os.extsep + 'py':
                    modules.append(name)
        return modules

    def load_init(self, path):
        self.add_path(path)
        modules = self.modules_from_path(path)
        output = 'modules '
        for module in modules:
            loaded_module = self.load(module)
            if loaded_module is not None:
                output += loaded_module.name + ', '
            else:
                output += module + '[FAILED], '
        output = output[:-2]
        output += ' loaded'
        self.bot.curses.pad_addline(output)

    def load(self, name):
        whole_module = importlib.import_module(name)
        imp.reload(whole_module)  # so reloading works

        # find the actual goshu Module we wanna load from the whole module
        module = None
        for item in inspect.getmembers(whole_module):
            if item[1] in Module.__subclasses__():
                module = item[1]()
                break
        if module is None:
            return None

        if module.name in self.modules:
            return None

        self.modules[module.name] = module
        for direction in ['in', 'out', 'commands', '*']:
            if direction not in module.events:
                module.events[direction] = {}
        module.folder_path = 'modules' + os.sep + module.name
        module.bot = self.bot
        return module

    def unload(self, name):
        if name not in self.modules:
            self.bot.curses.pad_addline('module', name, 'not in', self.modules)
            return False

        del self.modules[name]
        return True

    def handle(self, event):
        called = []
        for module in sorted(self.modules):
            for search_direction in ['*', event.direction]:
                for search_type in ['*', event.type]:
                    if search_type in self.modules[module].events[search_direction]:
                        for h in self.modules[module].events[search_direction][search_type]:
                            if h[1] not in called:
                                called.append(h[1])
                                h[1](event)
        if event.type == 'privmsg' or event.type == 'pubmsg' and event.direction == 'in':
            self.handle_command(event)

    def handle_command(self, event):
        if self.bot.settings.store['prefix'] in event.arguments[0] and event.arguments[0].split(self.bot.settings.store['prefix'])[0] == '':
            if len(event.arguments[0].split(self.bot.settings.store['prefix'])[1].strip()) < 1:
                return  # empty
            elif len(event.arguments[0].split(self.bot.settings.store['prefix'])[1].split()[0]) < 1:
                return  # no command
            command_name = event.arguments[0][1:].split()[0].lower()
            try:
                command_args = event.arguments[0][1:].split(' ', 1)[1]
            except IndexError:
                command_args = ''

            useraccount = self.bot.accounts.account(event.source, event.server)
            if useraccount:
                userlevel = self.bot.accounts.access_level(useraccount)
            else:
                userlevel = 0

            called = []
            for module in sorted(self.modules):
                if 'commands' in self.modules[module].events:
                    for search_command in ['*', command_name]:
                        if search_command in self.modules[module].events['commands']:
                            if userlevel >= self.modules[module].events['commands'][search_command][2]:
                                if self.modules[module].events['commands'][search_command][0] not in called:
                                    called.append(self.modules[module].events['commands'][search_command][0])
                                    self.modules[module].events['commands'][search_command][0](event, Command(command_name, command_args))
                            else:
                                self.bot.curses.pad_addline('no privs mang')


class Command:
    """Command from a client."""

    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments

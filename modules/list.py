#!/usr/bin/env python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <danneh@danneh.net> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return Daniel Oakley
# ----------------------------------------------------------------------------
# Goshubot IRC Bot    -    http://danneh.net/goshu

from gbot.modules import Module

class list(Module):
    name = "list"

    def __init__(self):
        self.events = {
            'commands' : {
                'list' : [self.list, "[command] --- list all commands; if command is present, display info on that command instead~", 0],
            },
        }

    def list(self, event, command):
        bot_commands = []

        for module in self.bot.modules.modules:
            module_commands = self.bot.modules.modules[module].commands()
            for command_name in module_commands:
                if command_name == '*':
                    continue
                command_description = module_commands[command_name][1]
                command_permission = module_commands[command_name][2]
                if len(module_commands[command_name]) >= 4:
                    command_view_permission = module_commands[command_name][3]
                else:
                    command_view_permission = command_permission
                if self.bot.accounts.access_level(event) >= command_view_permission:
                    bot_commands.append([command_name, command_description, command_permission])
        bot_commands = sorted(bot_commands)

        if command.arguments:
            # single command info
            for bot_command in bot_commands:
                if bot_command[0] == command.arguments.split()[0]:
                    command_permission = bot_command[2]
                    if len(bot_command) >= 4:
                        command_view_permission = bot_command[3]
                    else:
                        command_view_permission = command_permission
                    if self.bot.accounts.access_level(event) >= command_view_permission:
                        output = '*** Command:  '
                        output += bot_command[0] + ' '
                        output += bot_command[1]

                        self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], output)

        else:
            # list commands
            output = ['*** Commands: ', '    ']
            limit = int(len(bot_commands) / 2)
            for bot_command in bot_commands[:limit]:
                output[0] += bot_command[0] + ', '
            output[0] = output[0][:-2] # remove last ', '
            for bot_command in bot_commands[limit:]:
                output[1] += bot_command[0] + ', '
            output[1] = output[1][:-2] # remove last ', '

            output.append('Note: to display information on a specific command, use /ilist <command>/i. eg: /ilist 8ball');

            for line in output:
                self.bot.irc.servers[event.server].privmsg(event.source.split('!')[0], line)

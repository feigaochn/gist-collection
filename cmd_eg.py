#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cmd


class HelloWorld(cmd.Cmd):
    def do_hi(self, line):
        """hi [person]
        greeting"""
        # ugly line indent
        print('hello,', line)

    def help_hi(self):
        """live help"""
        print('\n'.join(['help', 'hi', 'person']))

    def complete_hi(self, text, line, begidx, endidx):
        FRIENDS = ['Alice', 'Adam', 'Barbara', 'Bob']
        if not text:
            completions = FRIENDS[:]
        else:
            completions = [f for f in FRIENDS if f.startswith(text)]
        return completions

    # start override
    def cmdloop(self, intro=None):
        print('cmdloop({})'.format(intro))
        return cmd.Cmd.cmdloop(self, intro)

    def preloop(self):
        print('preloop()')

    def precmd(self, line):
        print('precmd({})'.format(line))
        return cmd.Cmd.precmd(self, line)

    def onecmd(self, line):
        print('onecmd({})'.format(line))
        return cmd.Cmd.onecmd(self, line)

    def parseline(self, line):
        print('parseline({}) =>'.format(line))
        ret = cmd.Cmd.parseline(self, line)
        print(ret)
        return ret

    def emptyline(self):
        # if the line is empty, default implementation runs previous command again
        print('emptyline()')
        return cmd.Cmd.emptyline(self)

    def default(self, line):
        # If command is not found, default() is called instead.
        print('default({})'.format(line))
        return cmd.Cmd.default(self, line)

    def do_EOF(self, line):
        print('EOF')
        return True

    def postcmd(self, stop, line):
        print('postcmd({}, {})'.format(stop, line))
        return cmd.Cmd.postcmd(self, stop, line)

    def postloop(self):
        print('postloop()')

    # ending override
    # doc
    prompt = 'i am my prompt: '
    intro = 'i am welcome message.'
    doc_header = 'i am doc_header'
    misc_header = 'i am misc_header'
    undoc_header = 'i am undoc_header'
    ruler = 'i am ruler'

    def do_prompt(self, line):
        # change the interactive prompt
        self.prompt = line + ': '


def main():
    HelloWorld().cmdloop('illustrating methods of cmd.Cmd')


if __name__ == '__main__':
    main()

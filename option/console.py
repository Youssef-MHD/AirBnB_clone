#!/usr/bin/python3
"""Command Line Interpreter"""

import cmd
import json
import re
import sys

from models import *
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def do_EOF(self, *args):
        """Exits the program"""
        print()
        return True

    def do_quit(self, *args):
        """Exits the program"""
        return True

    def do_create(self, line):
        """Creates an instance of the class"""
        if not line:
            print("** class name missing **")
            return

        class_name = line.split()[0]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        instance = storage.classes()[class_name]()
        instance.save()
        print(instance.id)

    def do_show(self, line):
        """Shows the instance details of the class"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        class_name, instance_id = args[:2]

        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes the instance of the class"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        class_name, instance_id = args[:2]

        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, line):
        """Prints the string representation of all instances"""
        if not line:
            instances = [str(obj) for obj in storage.all().values()]
        else:
            class_name = line.split()[0]
            if class_name not in storage.classes():
                print("** class doesn't exist **")
                return

            instances = [str(obj) for key, obj in storage.all().items() if key.startswith(f"{class_name}.")]

        print(instances)

    def do_update(self, line):
        """Updates the instance of the class"""
        args = line.split()
        if len(args) < 2:
            print("** class name missing **")
            return
        class_name, instance_id = args[:2]

        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        if "{" in line and "}" in line:
            update_dict = json.loads(re.search(r"{(.+?)}", line).group(0))
            for attr, value in update_dict.items():
                setattr(storage.all()[key], attr, value)
        elif len(args) < 4:
            print("** attribute name missing **")
            return
        elif len(args) < 5:
            print("** value missing **")
            return
        else:
            setattr(storage.all()[key], args[3], eval(args[4]))
        storage.all()[key].save()

    def emptyline(self):
        pass

    def precmd(self, line):
        # Handle non-interactive mode
        if not sys.stdin.isatty():
            print()
            return ''

        match = re.match(r"^(\w+)\.(\w+)(?:\(([^)]*)\))?$", line)
        if match:
            class_name, command, args = match.groups()
            if args:
                args_match = re.match(r'^"([^"]*)"(?:, "(.*)")?$', args)
                if args_match:
                    args = args_match.groups()
                else:
                    args = (args,)
                line = f"{command} {class_name} {' '.join(args)}"
            else:
                line = f"{command} {class_name}"
        return line

    def do_count(self, line):
        """Counts all the instances of the class"""
        class_name = line.split()[0] if line else None
        if not class_name:
            print("** class name missing **")
            return

        count = sum(1 for key in storage.all() if key.startswith(f"{class_name}."))
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()


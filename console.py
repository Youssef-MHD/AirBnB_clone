#!/usr/bin/python3
""" Module for the command interpreter's entry point. """

import cmd
import re
import json
from models.base_model import BaseModel
from models import storage

class HBNBCommand(cmd.Cmd):
    """ Class for the command-line interpreter. """
    prompt = "(hbnb) "

    def default(self, line):
        """Catch all commands that are not explicitly defined."""
        self._process_custom_command(line)

    def _process_custom_command(self, line):
        """Process commands in class.method(args) format."""
        match = re.match(r"^(\w+)\.(\w+)\((.*)\)$", line)
        if match:
            class_name, method_name, args = match.groups()
            uid, attr_or_value = self._parse_args(args)
            command = f"{method_name} {class_name} {uid} {attr_or_value}"
            self.onecmd(command)
        else:
            return line

    def _parse_args(self, args):
        """Parse arguments for the command."""
        match = re.match(r'^"([^"]+)"(?:, (.*))?$', args)
        if match:
            uid, attr_or_value = match.groups()
            return uid, attr_or_value or ""
        return args, ""

    def update_dict(self, class_name, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        try:
            attr_dict = json.loads(s)
        except json.JSONDecodeError:
            print("** invalid dictionary format **")
            return

        if not self._validate_class(class_name):
            return
        key = f"{class_name}.{uid}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return

        for attr, value in attr_dict.items():
            self._set_attribute(instance, class_name, attr, value)
        instance.save()

    def _validate_class(self, class_name):
        """Validate if a class exists in storage."""
        if not class_name:
            print("** class name missing **")
            return False
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return False
        return True

    def _set_attribute(self, instance, class_name, attr, value):
        """Set attribute for an instance, casting as necessary."""
        attributes = storage.attributes().get(class_name, {})
        if attr in attributes:
            value = attributes[attr](value)
        else:
            value = self._cast_value(value)
        setattr(instance, attr, value)

    def _cast_value(self, value):
        """Cast value to appropriate type."""
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value.strip('"')

    def do_EOF(self, line):
        """Handle the end-of-file character."""
        print()
        return True

    def do_quit(self, line):
        """Exit the program."""
        return True

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_create(self, line):
        """Create an instance of a class."""
        if not self._validate_class(line):
            return
        new_instance = storage.classes()[line]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """Show the string representation of an instance."""
        args = line.split()
        if len(args) < 1 or not self._validate_class(args[0]):
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
        else:
            print(instance)

    def do_destroy(self, line):
        """Delete an instance of a class."""
        args = line.split()
        if len(args) < 1 or not self._validate_class(args[0]):
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        """Show all instances, optionally filtered by class."""
        args = line.split()
        if args and not self._validate_class(args[0]):
            return
        instances = storage.all().values()
        if args:
            class_name = args[0]
            instances = [str(instance) for instance in instances if instance.__class__.__name__ == class_name]
        else:
            instances = [str(instance) for instance in instances]
        print(instances)

    def do_count(self, line):
        """Count the instances of a class."""
        args = line.split()
        if not args or not self._validate_class(args[0]):
            return
        class_name = args[0]
        count = sum(1 for key in storage.all() if key.startswith(f"{class_name}."))
        print(count)

    def do_update(self, line):
        """Update an instance's attributes."""
        args = line.split(maxsplit=3)
        if len(args) < 1 or not self._validate_class(args[0]):
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        class_name, uid = args[0], args[1]
        key = f"{class_name}.{uid}"
        instance = storage.all().get(key)
        if not instance:
            print("** no instance found **")
            return
        if len(args) == 3:
            try:
                attr_dict = json.loads(args[2].replace("'", '"'))
                self.update_dict(class_name, uid, attr_dict)
            except json.JSONDecodeError:
                print("** invalid dictionary format **")
        elif len(args) < 4:
            print("** attribute name or value missing **")
        else:
            attr_name, attr_value = args[2], args[3]
            self._set_attribute(instance, class_name, attr_name, attr_value)
            instance.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()


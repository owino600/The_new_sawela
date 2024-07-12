#!/usr/bin/python3
"""
CLI for the Store Management System
"""

import sys
import cmd
from models import storage
from models.base_model import BaseModel

class StoreMgmtCommand(cmd.Cmd):
    """Command interpreter for the Store Management System"""

    prompt = '(store_mgmt) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_create(self, arg):
        """Create a new BaseModel instance"""
        if arg == "BaseModel":
            new_instance = BaseModel()
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Show an instance based on class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        else:
            key = args[0] + "." + args[1]
            obj = storage.all().get(key)
            if obj is None:
                print("** no instance found **")
            else:
                print(obj)

    def do_destroy(self, arg):
        """Destroy an instance based on class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        else:
            key = args[0] + "." + args[1]
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """Show all instances of a class"""
        if arg == "":
            print([str(obj) for obj in storage.all().values()])
        elif arg == "BaseModel":
            print([str(obj) for obj in storage.all().values() if type(obj).__name__ == "BaseModel"])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Update an instance based on class name and id"""
        args = arg.split()
        if len(args) < 4:
            print("** not enough arguments **")
            return

        class_name, obj_id, attr_name, attr_value = args[0], args[1], args[2], args[3]
        if class_name != "BaseModel":
            print("** class doesn't exist **")
            return

        key = class_name + "." + obj_id
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return

        setattr(obj, attr_name, attr_value)
        obj.save()

if __name__ == '__main__':
    StoreMgmtCommand().cmdloop()
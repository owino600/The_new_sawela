#!/usr/bin/python3
"""
CLI for the Store Management System
"""

import cmd
from models import storage
from models.stock_received import StockReceived
from models.stock_issued import StockIssued
from models.inventory import Inventory


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
        if arg == "Inventory":
            item = input("Item: ")
            quantity = int(input("Quantity: "))
            unit_price = float(input("Unit Price: "))
            supplier = input("Supplier: ")
            date_received = input("Date Received: ")
            expiration_date = input("Expiration Date: ")
            new_instance = Inventory(
                item=item, 
                quantity=quantity, 
                unit_price=unit_price,
                supplier=supplier,
                date_received=date_received,
                expiration_date=expiration_date
            )
            new_instance.save()
            print(new_instance.id)
        elif arg == "StockReceived":
            item = input("Item: ")
            quantity = int(input("Quantity: "))
            received_date = input("Received Date: ")
            new_instance = StockReceived(item=item, quantity=quantity, received_date=received_date)
            new_instance.save()
            self.update_inventory(item, quantity, add=True)
            print(new_instance.id)
        elif arg == "StockIssued":
            item = input("Item: ")
            quantity = int(input("Quantity: "))
            issued_date = input("Issued Date: ")
            new_instance = StockIssued(item=item, quantity=quantity, issued_date=issued_date)
            new_instance.save()
            self.update_inventory(item, quantity, add=False)
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def update_inventory(self, item, quantity, add=True):
        """Update inventory based on stock received or issued"""
        all_inventory = storage.all()
        for key, obj in all_inventory.items():
            if isinstance(obj, Inventory) and obj.item == item:
                if add:
                    obj.quantity += quantity
                else:
                    obj.quantity -= quantity
                obj.save()
                return
        if add:
            new_inventory = Inventory(item=item, quantity=quantity)
            new_inventory.save()

    def do_show(self, arg):
        """Show an instance based on class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif args[0] not in ["Inventory", "StockReceived", "StockIssued"]:
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
        elif args[0] not in ["Inventory", "StockReceived", "StockIssued"]:
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
        elif arg in ["Inventory", "StockReceived", "StockIssued"]:
            print([str(obj) for obj in storage.all().values() if type(obj).__name__ == arg])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Update an instance based on class name and id"""
        args = arg.split()
        if len(args) < 4:
            print("** not enough arguments **")
            return

        class_name, obj_id, attr_name, attr_value = args[0], args[1], args[2], args[3]
        if class_name not in ["Inventory", "StockReceived", "StockIssued"]:
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
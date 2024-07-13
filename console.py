#!/usr/bin/python3
"""Entry point of the command interpreter."""
import cmd
from models import storage
from models.inventory import Inventory
from models.stock_received import StockReceived
from models.stock_issued import StockIssued
from datetime import datetime 

class StoreMgmtCommand(cmd.Cmd):
    prompt = "(store_mgmt) "

    def do_create(self, args):
        """Create a new record in the specified table."""
        args = args.split()
        if len(args) < 1:
            print("** Table name missing **")
            return
        
        table_name = args[0]
        if table_name not in ["Inventory", "StockReceived", "StockIssued"]:
            print("** Invalid table name **")
            return

        if table_name == "StockReceived":
            item = input("Item: ")
            quantity = int(input("Quantity: "))
            received_date = input("Received Date (YYYY-MM-DD): ")
            received_date = datetime.strptime(received_date, "%Y-%m-%d")

            new_entry = StockReceived(item=item, quantity=quantity, received_date=received_date)
            storage.new(new_entry)
            storage.save()

        elif table_name == "StockIssued":
            item = input("Item: ")
            quantity = int(input("Quantity: "))
            issued_date = input("Issued Date (YYYY-MM-DD): ")
            issued_date = datetime.strptime(issued_date, "%Y-%m-%d")

            new_entry = StockIssued(item=item, quantity=quantity, issued_date=issued_date)
            storage.new(new_entry)
            storage.save()

        elif table_name == "Inventory":
            product_name = input("Product Name: ")
            category = input("Category: ")
            description = input("Description: ")
            quantity = int(input("Quantity: "))
            unit_price = float(input("Unit Price: "))
            supplier = input("Supplier: ")
            date_received = input("Date Received (YYYY-MM-DD): ")
            date_received = datetime.strptime(date_received, "%Y-%m-%d")
            expiration_date = input("Expiration Date (YYYY-MM-DD): ")
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")

            new_entry = Inventory(
                Product_name=product_name,
                Category=category,
                Description=description,
                quantity=quantity,
                unit_price=unit_price,
                supplier=supplier,
                date_received=date_received,
                Expiration_date=expiration_date
            )
            storage.new(new_entry)
            storage.save()

    def do_all(self, args):
        """Display all records of a table."""
        args = args.split()
        if len(args) < 1:
            print("** Table name missing **")
            return

        table_name = args[0]
        if table_name not in ["Inventory", "StockReceived", "StockIssued"]:
            print("** Invalid table name **")
            return

        if table_name == "Inventory":
            records = storage.all(Inventory)
        elif table_name == "StockReceived":
            records = storage.all(StockReceived)
        elif table_name == "StockIssued":
            records = storage.all(StockIssued)

        for key, value in records.items():
            print(value.to_dict())

    def do_quit(self, args):
        """Quit the command line."""
        return True

    def do_EOF(self, args):
        """Handle the EOF command."""
        print("")
        return True

    def emptyline(self):
        """Override the emptyline method to do nothing."""
        pass

if __name__ == "__main__":
    StoreMgmtCommand().cmdloop()
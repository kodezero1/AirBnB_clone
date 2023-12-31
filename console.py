#!/usr/bin/python3
"""
This file defines the console class which will
serve as the entry point of the entire project
"""
from cmd import Cmd
from models import storage
from models.engine.errors import *
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

# Global variable of registered models
model_classes = storage.models

class MyCommandInterpreter(Cmd):
    """
    The Console based driver of the AirBnb Clone
    All interactions with the system are done via
    this class
    """

    prompt = "(hbnb) "

    """Commands"""
    def do_EOF(self, args):
        """Exit the program in non-interactive mode"""
        return True

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_create(self, args):
        """Create an instance of Model given its name e.g.
        $ create ModelName
        Throws an Error if ModelName is missing or doesn't exist
        """
        args, arg_count = parse(args)

        if not arg_count:
            print("** class name missing **")
        elif args[0] not in model_classes:
            print("** class doesn't exist **")
        elif arg_count == 1:
            new_instance = eval(args[0])()
            print(new_instance.id)
            new_instance.save()
        else:
            print("** Too many arguments for create **")

    def do_show(self, args):
        """Show an instance of Model based on its ModelName and id e.g.
        $ show MyModel instance_id
        Print an error message if either MyModel or instance_id is missing
        Print an error message for wrong MyModel or instance_id
        """
        args, arg_count = parse(args)

        if not arg_count:
            print("** class name missing **")
        elif arg_count == 1:
            print("** instance id missing **")
        elif arg_count == 2:
            try:
                instance = storage.find_by_id(*args)
                print(instance)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many arguments for show **")

    def do_destroy(self, args):
        """Deletes an instance of Model based on its ModelName and id."""
        args, arg_count = parse(args)

        if not arg_count:
            print("** class name missing **")
        elif arg_count == 1:
            print("** instance id missing **")
        elif arg_count == 2:
            try:
                storage.delete_by_id(*args)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many arguments for destroy **")

    def do_all(self, args):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        args, arg_count = parse(args)

        if arg_count < 2:
            try:
                print(storage.find_all(*args))
            except ModelNotFoundError:
                print("** class doesn't exist **")
        else:
            print("** Too many arguments for all **")

    def do_update(self, args):
        """Updates an instance based on its id e.g.
        $ update Model id field value
        Throws errors for missing arguments
        """
        args, arg_count = parse(args)
        if not arg_count:
            print("** class name missing **")
        elif arg_count == 1:
            print("** instance id missing **")
        elif arg_count == 2:
            print("** attribute name missing **")
        elif arg_count == 3:
            print("** value missing **")
        else:
            try:
                storage.update_one(*args[0:4])
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")

    def do_models(self, args):
        """Print all registered Models"""
        print(*model_classes)

    def handle_class_methods(self, args):
        """Handle Class Methods
        <cls>.all(), <cls>.show() etc
        """
        printable = ("all(", "show(", "count(", "create(")
        try:
            result = eval(args)
            for x in printable:
                if x in args:
                    print(result)
                    break
            return
        except AttributeError:
            print("** invalid method **")
        except InstanceNotFoundError:
            print("** no instance found **")
        except TypeError as te:
            field = te.args[0].split()[-1].replace("_", " ")
            field = field.strip("'")
            print(f"** {field} missing **")
        except Exception as e:
            print("** invalid syntax **")

    def default(self, args):
        """Override default method to handle class methods"""
        if '.' in args and args[-1] == ')':
            if args.split('.')[0] not in model_classes:
                print("** class doesn't exist **")
                return
            return self.handle_class_methods(args)
        return Cmd.default(self, args)

    def emptyline(self):
        """Override empty line to do nothing"""
        return

def parse(line: str):
    """Splits a line by spaces"""
    args = shlex.split(line)
    return args, len(args)

if __name__ == "__main__":
    MyCommandInterpreter().cmdloop()

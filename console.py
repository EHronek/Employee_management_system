#!/usr/bin/python3
"""Console for my application"""
import shlex
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.attendance import Attendance
from models.department import Department
from models.employee import Employee
from models.leave_request import LeaveRequest
from models.payroll import Payroll
from models.position import Position
from models.attendance import Attendance
from models.benefits import Benefits
from models.company_asset import CompanyAssets
from models.performance_review import PerformanceReview
from models.overtime import Overtime
from models.training import Training

classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Attendance": Attendance,
            "Department": Department,
            "Employee" : Employee,
            "LeaveRequest": LeaveRequest,
            "Payroll": Payroll,
            "Position": Position,
            "Attendance": Attendance,
            "Benefits": Benefits,
            "CompanyAssets": CompanyAssets,
            "PerformanceReview": PerformanceReview,
            "Overtime": Overtime,
            "Training": Training
        }


class EMSCommand(cmd.Cmd):
    """EMS Console"""
    prompt = '(EMS $) '

    def do_EOF(self, arg):
        """Exits the console"""
        return True
    
    def emptyline(self):
        """Overwriting the empty line method"""
        return False
    
    def do_quit(self, arg):
        """QUit command to exit the console"""
        return True
    
    def _key_value_parser(self, args):
        """creates a dictionary from a list of sstrings"""
        new_dict = {}
        for arg in args:
            if "=" in args:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value.startswith('"') and value.endswith('"'):
                    value = value[1: -1].replace("_", " ")
                    """ if value[0] == value[1] == '"':
                            value = shlex.split(value)[0].replace('_', ' ') """
                
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            continue
                new_dict[key] = value
        return new_dict
    
    """ def do_create(self, arg):
        '''Creates a new instance of a class'''
        args = arg.split()
        if len(args) == 0:
            print("** class missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
            print(instance.id)
            instance.save()
        else:
            print("** class doesn't exist **")
            return False
        
        # print(instance.id)
        # instance.save() """
    


    def do_create(self, arg):
        """
        Creates a new instance of a given class, sets attributes if provided,
        saves the instance, and prints the instance ID.

        Usage:
            create ClassName key1=value1 key2="value with spaces" ...
        """
        if not arg:
            print("** class name missing **")
            return

        args = shlex.split(arg)  # Properly split the input while respecting quotes
        class_name = args[0]

        if class_name not in classes:
            print("** class doesn't exist **")
            return

        new_instance = classes[class_name]()  # Create an instance

        # Set attributes from arguments
        for param in args[1:]:
            if "=" in param:
                key, value = param.split("=", 1)

                # Attempt to cast value to int or float, otherwise keep as string
                if value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        value = value.replace("_", " ")  # Replace underscores with spaces

                setattr(new_instance, key, value)  # Dynamically set attributes

        new_instance.save()  # Save the instance
        print(new_instance.id)



    """ def do_show(self, arg):
        '''Prints an instance as a string based on the class and Id'''
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** Instance id missing **")
        else:
            print("** class doesn't exist **") """
    
    """ def do_show(self, arg):
        ''' Prints an instance as a string based on the class and ID.'''
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False

        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        obj_id = args[1]
        key = f"{class_name}.{obj_id}"

        if key in models.storage.all():
            print(models.storage.all()[key])
        else:
            print("** no instance found **")
        

            obj_id = args[1]
            key = f"{class_name}.{obj_id}"

            if key in models.storage.all():
                print(models.storage.all()[key])
            else:
                print("** no instance found **") """
    

    def do_show(self, arg):
        """Prints an instance as a string based on the class and ID."""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False

        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        obj_id = args[1]
        obj = models.storage.get(classes[class_name], obj_id)

        if obj:
            print(obj)
        else:
            print("** no instance found **")




    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """prints a string representation of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end='')
        print(", ".join(obj_list), end='')
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attractive & value"""
        args = shlex.split(arg)
        integers = []
        floats = ["salary", "salary_range", "basic_salary",
                  "deductions", "net_pay", "overtime_pay","bonuses"]
        if len(args) == 0:
            print("** class missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] in classes:
                                if args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except: 
                                        args[3] = 0.0
                                elif args[2] in integers:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[key], args[2], args[3])
                            models.storage.all()[key].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == "__main__":
    EMSCommand().cmdloop()


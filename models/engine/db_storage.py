#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from models.base_model import Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
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




class DBStorage:
    """interact with the mysql database"""
    classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Attendance": Attendance,
            "Department": Department,
            "Employee" : Employee,
            "LeaveRequest": LeaveRequest,
            "Payroll": Payroll,
            "Position": Position,
            "Benefits": Benefits,
            "CompanyAssets": CompanyAssets,
            "PerformanceReview": PerformanceReview,
            "Overtime": Overtime,
            "Training": Training
        }
    
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        EMS_MYSQL_USER = getenv("EMS_MYSQL_USER")
        EMS_MYSQL_PWD = getenv("EMS_MYSQL_PWD")
        EMS_MYSQL_HOST = getenv("EMS_MYSQL_HOST")
        EMS_MYSQL_DB = getenv("EMS_MYSQL_DB")
        EMS_ENV = getenv("EMS_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(EMS_MYSQL_USER,
                                             EMS_MYSQL_PWD,
                                             EMS_MYSQL_HOST,
                                             EMS_MYSQL_DB), pool_pre_ping=True)
        
        if EMS_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        data = {}
        if cls:
            if isinstance(cls, str):
                cls = self.classes.get(cls)
                if cls is None:
                    raise ValueError(f"Class {cls} is not a valid model")
            
            if cls not in self.classes.values():
                raise ValueError(f"Class {cls} is not a valid model")
            
            if cls not in self.classes.values():
                raise ValueError(f"{cls} is not recognized")
            
            class_obj = self.__session.query(cls).all()
            for obj in class_obj:
                key = f"{obj.__class__.__name__}.{obj.id}"
                data[key] = obj

        else:
            for clas in  self.classes.values():
                class_objs = self.__session.query(clas).all()
                for obj in class_objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    data[key] = obj

        return data


    
    """ def all(self, cls=None):
        '''query on the current database session'''
        new_dict = {}
        for clas in classes:
            if cls is None or cls is classes[clas] or cls is clas:
                objs = self.__session.query(classes[cls]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict """
    
    """ def all(self, cls=None):
        '''query on the current database session'''
        objs = {}
        if cls:
            cls_name = cls.__name__
            if cls_name in classes:
                query_result = self.__session.query(classes[cls_name]).all()
                objs = {f"{cls_name}.{obj.id}" for obj in query_result}
        else:
            for cls_name, cls_obj in classes.items():
                query_result = self.__session.query(cls_obj).all()
                objs.update({f"{cls_name}.{obj.id}" for obj in query_result})

        return objs """
    

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()


    def get(self, cls, id):
        """Returns objects based on the class and its ID or None not found"""
        all_classes = self.all(cls)

        for obj in all_classes.values():
            if id == str(obj.id):
                return obj
        return None

    def count(self, cls=None):
        """Count of how many instancex of a class"""
        return len(self.all(cls))
    
    def find(self, cls=None, username=None):
        """Finds a user in the db and returns a bolean"""
        if cls is not None or username is not None:
            all_classes = self.all(cls).values()

            for user in all_classes:
                if user.username == username:
                    return True
            return False

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
#!/usr/bin/python3
"""
This module defines the BaseModel class, the foundation for all models.
"""

from uuid import uuid4
from datetime import datetime
import models

class BaseModel:
    """
    Base class for all models.

    Attributes:
        id (str): Unique identifier for each instance.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.

    Methods:
        __init__(*args, **kwargs): Initializes or deserializes an instance.
        __str__(): Returns a string representation of the instance.
        save(): Updates the modification time and saves the instance.
        to_dict(): Converts the instance to a serializable dictionary.
        all(cls): Retrieves all instances of the class.
        count(cls): Returns the number of class instances.
        create(cls, *args, **kwargs): Creates a new instance and returns its ID.
        show(cls, instance_id): Retrieves an instance by ID.
        destroy(cls, instance_id): Deletes an instance by ID.
        update(cls, instance_id, *args): Updates an instance's attributes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes or deserializes an instance.
        """

        if not kwargs:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            models.storage.new(self)
        else:
            for key, val in kwargs.items():
                if key == '__class__':
                    continue
                self.__dict__[key] = val
            if 'created_at' in kwargs:
                self.created_at = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' in kwargs:
                self.updated_at = datetime.strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

    def __str__(self):
        """
        Returns a string representation of the instance.
        """
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the modification time and saves the instance.
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """
        Converts the instance to a serializable dictionary.
        """
        data = {**self.__dict__}
        data['__class__'] = type(self).__name__
        data['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        data['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return data

    @classmethod
    def all(cls):
        """
        Retrieves all instances of the class.
        """
        return models.storage.find_all(cls.__name__)

    @classmethod
    def count(cls):
        """
        Returns the number of class instances.
        """
        return len(models.storage.find_all(cls.__name__))

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new instance and returns its ID.
        """
        new_instance = cls(*args, **kwargs)
        return new_instance.id

    @classmethod
    def show(cls, instance_id):
        """
        Retrieves an instance by ID.
        """
        return models.storage.find_by_id(cls.__name__, instance_id)

    @classmethod
    def destroy(cls, instance_id):
        """
        Deletes an instance by ID.
        """
        return models.storage.delete_by_id(cls.__name__, instance_id)

    @classmethod
    def update(cls, instance_id, *args):
        """
        Updates an instance's attributes.
        """
        if not args:
            print("** attribute name missing **")
            return
        if len(args) == 1 and isinstance(args[0], dict):
            args = args[0].items()
        else:
            args = [args[:2]]
        for arg in args:
            models.storage.update_one(cls.__name__, instance_id, *arg)

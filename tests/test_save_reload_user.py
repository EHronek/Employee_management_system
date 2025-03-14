#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User

all_objs = storage.all()
print("-- Reloaded objects --")
print()
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User 1 --")
my_user = User()
my_user.username = "John Doe"
my_user.password_hash = my_user._hash_password("john123")
my_user.role = "Hr"
my_user.save()
print(my_user)


print("-- Create a new User 2--")
my_user2 = User()
my_user2.username = "John Doe"
my_user2.password_hash = my_user2._hash_password("john123")
my_user2.role = "Hr"
my_user2.save()
print(my_user2)
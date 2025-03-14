#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel

# Reload objects from file (if it exists)
print("-- Reloaded objects --")
all_objs = storage.all()
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

# Create a new object and save it
print("-- Create a new object --")
my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89
my_model.save()  # This should create/update file.json

# Print the new object
print(my_model)

# Verify that the file was created
print("-- Verifying file creation --")
try:
    with open("file.json", "r") as f:
        print("file.json contents:")
        print(f.read())
except FileNotFoundError:
    print("file.json not found")
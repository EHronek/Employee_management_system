#!/usr/bin/python3
"""Initializes a blueprint instance and loads all the routes from index"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.departments import *
from api.v1.views.employees import *
from api.v1.views.positions import *
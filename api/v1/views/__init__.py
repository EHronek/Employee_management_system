#!/usr/bin/python3
"""Initializes a blueprint instance and loads all the routes from index"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.departments import *
from api.v1.views.employees import *
from api.v1.views.positions import *
from api.v1.views.users import *
from api.v1.views.attendance import *
from api.v1.views.leave_requests import *
from api.v1.views.company_assets import *
from api.v1.views.benefits import *
from api.v1.views.payrolls import *
from api.v1.views.performance_reviews import *
from api.v1.views.overtime import *
from api.v1.views.training import *

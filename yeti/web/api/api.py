"""API endpionts for Yeti."""

from flask import Blueprint
from .observable import Observable

blueprint = Blueprint("api", __name__)

Observable.register(blueprint)

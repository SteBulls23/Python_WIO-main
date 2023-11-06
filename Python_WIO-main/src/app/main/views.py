from flask import Blueprint
from http import HTTPStatus

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def ciao():
    return [
        {"message" : "Ciao"}, {"message" : "Buongiorno"}, HTTPStatus.CREATED
    ]

@main.route("/welcome", methods=["GET"]) #@main.get("/welcome")
def welcome():
    return "welcome"

@main.route("/login", methods=["GET"]) 
def login():
    return "login"
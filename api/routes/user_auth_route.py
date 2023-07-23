from controllers.user_auth_controller import (
    set_register,
    set_login,
    set_active,
    validate_token,
    forgot_password,
    recover_password,
)
from flask import Flask, request, Blueprint, jsonify
from flask_bcrypt import Bcrypt


user_auth = Blueprint("user_auth", __name__)


@user_auth.route("/register", methods=["POST"])
def user_register():
    return set_register()


@user_auth.route("/login", methods=["POST"])
def user_login():
    return set_login()


@user_auth.route("/active/<token>", methods=["GET"])
def user_active(token):
    set_active(token)
    return "Cuenta activada"


@user_auth.route("/forgot-password", methods=["POST"])
def user_forgot_password():
    return forgot_password()


@user_auth.route("/recover-password/<token>", methods=["GET"])
def user_forgot_password(token):
    recover_password(token)
    return "Contraseña actualizada"


@user_auth.route("/validate-token", methods=["GET"])
def validate_route():
    return validate_token()

import config
import flask
from flask import request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import secrets


server = flask.Flask(__name__)
server.secret_key = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(server)


class User(UserMixin):
    def __init__(self, user_id=0):
        self.id = user_id

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_loader(user_id):
    user = User()
    return user


@server.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@server.route("/dashboard")
@login_required
def dashboard():
    return "Dashboard"


@server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == config.USERNAME and password == config.PASSWORD:
            user = User()
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("login.html")


@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

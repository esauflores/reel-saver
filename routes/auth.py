from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from helpers import users
from helpers.login import AppUser

auth_bp = Blueprint("auth", __name__)


class UserSignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Submit")


class UserSignInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


@auth_bp.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    sign_in_form: UserSignInForm = UserSignInForm()

    if request.method == "POST":
        if not sign_in_form.validate():
            flash(str(sign_in_form.errors), "error")
            return redirect(
                url_for(
                    "auth.sign_in",
                    form=sign_in_form,
                    _method="GET",
                )
            )

        username = sign_in_form.username.data
        password = sign_in_form.password.data

        user = users.validate_user(username, password)

        if user is not None:
            app_user = AppUser(user.id, user.username)
            login_user(app_user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home.home"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("auth.sign_in", _method="GET"))

    if request.method == "GET":
        return render_template("auth/sign_in.html", form=sign_in_form)


@auth_bp.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    sign_up_form: UserSignUpForm = UserSignUpForm()

    if request.method == "POST":
        if not sign_up_form.validate():
            flash(str(sign_up_form.errors), "error")
            return redirect(
                url_for(
                    "auth.sign_up",
                    form=sign_up_form,
                    _method="GET",
                )
            )

        username = sign_up_form.username.data
        password = sign_up_form.password.data

        created_user = users.create_user(username, password)

        if created_user:
            return redirect(url_for("auth.sign_in", _method="GET"))
        else:
            return redirect(url_for("auth.sign_up", _method="GET"))

    if request.method == "GET":
        return render_template("auth/sign_up.html", form=sign_up_form)


@auth_bp.route("/sign_out", methods=["POST"])
@login_required
def sign_out():
    logout_user()
    return redirect(url_for("home.home"))

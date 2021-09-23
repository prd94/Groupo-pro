from flask import *
from LoginRadius import LoginRadius as LR

auth = Blueprint('auth', __name__)

LR.API_KEY = "7849536a-5604-40cd-b9e9-190c4d09e010"
LR.API_SECRET = "1a58c6ee-3aea-495f-80be-d3ccc553b500"
loginradius = LR()
LR_AUTH_PAGE = "https://grouppro.hub.loginradius.com/auth.aspx?action={}&return_url={}"


@auth.route("/register/")
def register():
    return redirect(LR_AUTH_PAGE.format("register", request.host_url))


@auth.route('/login/')
def login():
    access_token = request.args.get("token")
    if access_token is None:
        # redirect the user to our LoginRadius login URL if no access token is provided
        return redirect(LR_AUTH_PAGE.format("login", request.base_url))

    # fetch the user profile details with their access tokens
    result = loginradius.authentication.get_profile_by_access_token(
        access_token)

    if result.get("ErrorCode") is not None:
        # redirect the user to our login URL if there was an error
        return redirect(url_for("login"))

    session["user_access_token"] = access_token

    return redirect(url_for("auth.dashboard"))


@auth.route("/dashboard/")
def dashboard():
    access_token = session.get("user_access_token")
    if access_token is None:
        return redirect(url_for("login"))

    # fetch the user profile details with their access tokens
    result = loginradius.authentication.get_profile_by_access_token(
        access_token)

    if result.get("ErrorCode") is not None:
        # redirect the user to our login URL if there was an error
        return redirect(url_for("login"))

    return jsonify(result)


@auth.route("/logout/")
def logout():
    access_token = session.get("user_access_token")
    if access_token is None:
        return redirect(url_for("login"))

    # invalidate the access token with LoginRadius API
    loginradius.authentication.auth_in_validate_access_token(access_token)
    session.clear()

    return flash("You have successfully logged out!")
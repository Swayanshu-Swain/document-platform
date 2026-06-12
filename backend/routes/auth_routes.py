from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from auth.auth_service import (
    authenticate_user
)

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = authenticate_user(
            username,
            password
        )

        if user:

            session["username"] = (
                user["username"]
            )

            session["role"] = (
                user["role"]
            )

            return redirect(
                "/dashboard"
            )

        return "Invalid Credentials"

    return render_template(
        "login.html"
    )

from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect
)

from auth.decorators import login_required

from services.dynamodb_service import (
    get_all_users
)

from auth.user_registration import (
    register_user
)

admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route("/users")
@login_required
def users():

    if session["role"] != "admin":
        return "Unauthorized", 403

    users = get_all_users()

    return render_template(
        "users.html",
        users=users
    )
@admin_bp.route(
    "/users/create",
    methods=["GET", "POST"]
)
@login_required
def create_user():

    if session["role"] != "admin":
        return "Unauthorized", 403

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        role = request.form["role"]

        success, message = register_user(
            username,
            password,
            role
        )

        if success:
            return redirect("/users")

        return message

    return render_template(
        "create_user.html"
    )

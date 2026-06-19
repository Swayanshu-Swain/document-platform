from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect
)

from auth.decorators import login_required

from services.dynamodb_service import (
    get_all_users,
    disable_user,
    enable_user,
    reset_password,
    get_audit_logs
)

from auth.user_registration import (
    register_user
)

from services.audit_service import (
    log_event
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
            try:

                log_event(
                    username=session["username"],
                    action="CREATE_USER",
                    file_id="-",
                    file_name="-",
                    department=role,
                    details=f"Created user {username}"
                 )
            except Exception as e:

                print(
                    f"Audit log failed: {e}"
                )
            return redirect("/users")

        return message

    return render_template(
        "create_user.html"
    )
@admin_bp.route(
    "/users/disable/<username>"
)
@login_required
def disable_user_route(username):

    if session["role"] != "admin":
        return "Unauthorized", 403

    disable_user(username)
    try:
        log_event(
            username=session["username"],
            action="DISABLE_USER",
            file_id="-",
            file_name="-",
            department="-",
            details=f"Disabled {username}"
            )
    except Exception as e:

        print(
            f"Audit log failed: {e}"
        )
    return redirect("/users")
@admin_bp.route(
    "/users/enable/<username>"
)
@login_required
def enable_user_route(username):

    if session["role"] != "admin":
        return "Unauthorized", 403

    enable_user(username)
    try:
        log_event(
            username=session["username"],
            action="ENABLE_USER",
            file_id="-",
            file_name="-",
            department="-",
            details=f"Enabled {username}"
        )
    except Exception as e:

        print(
            f"Audit log failed: {e}"
        )
    return redirect("/users")
@admin_bp.route(
    "/users/reset/<username>",
    methods=["GET", "POST"]
)
@login_required
def reset_user_password(username):

    if session["role"] != "admin":
        return "Unauthorized", 403

    if request.method == "POST":

        password = request.form[
            "password"
        ]

        reset_password(
            username,
            password
        )
        try:
            log_event(
                username=session["username"],
                action="RESET_PASSWORD",
                file_id="-",
                file_name="-",
                department="-",
                details=f"Reset password for {username}"
             )
        except Exception as e:

            print(
                f"Audit log failed: {e}"
         )
        return redirect(
            "/users"
        )

    return render_template(
        "reset_password.html",
        username=username
    )
@admin_bp.route("/audit")
@login_required
def audit_logs():

    if session["role"] != "admin":
        return "Unauthorized", 403

    logs = get_audit_logs()

    return render_template(
        "audit_logs.html",
        logs=logs
    )

from flask import (
    Blueprint,
    session
)

from auth.decorators import (
    login_required
)

from services.file_service import (
    get_files_by_department,
    get_files_shared_with_user,
    get_owned_files,
    get_shared_files,
    get_deleted_files
)

from flask import render_template

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    username = session["username"]
    role = session["role"]

    department_files = (
       get_files_by_department(
          role
       )
    )

    shared_files = (
       get_files_shared_with_user(
          username
       )
    )

    owned_files = (
        get_owned_files(
            username
        )
    )

    shared_files = (
        get_shared_files(
           username
        ) 
    )
    deleted_files = (
        get_deleted_files(
            username
        )
    )

    return render_template(
    "dashboard.html",
    username=username,
    role=role,
    owned_files=owned_files,
    shared_files=shared_files,
    deleted_files=deleted_files
)
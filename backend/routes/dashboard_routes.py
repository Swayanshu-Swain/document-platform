from flask import (
    Blueprint,
    session
)

from auth.decorators import (
    login_required
)

from services.dynamodb_service import (
    get_all_users
)

from services.file_service import (
    get_files_by_department,
    get_files_shared_with_user,
    get_owned_files,
    get_shared_files,
    get_deleted_files,
    get_total_documents,
    get_total_shared,
)

from services.audit_service import (
    get_total_audit_events,
    get_recent_audit_events
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

    audit_events = (
        get_recent_audit_events()
    )

    total_users = len(get_all_users())

    total_documents = (
        get_total_documents()
    )

    total_shared = (
        get_total_shared()
    )

    total_audit_events = (
        get_total_audit_events()
    )

    return render_template(
    "dashboard.html",
    username=username,
    role=role,

    owned_files=owned_files,
    shared_files=shared_files,
    deleted_files=deleted_files,

    total_users=total_users,
    total_documents=total_documents,
    total_shared=total_shared,
    total_audit_events=total_audit_events,

    recent_documents=owned_files,
    audit_events=audit_events
)
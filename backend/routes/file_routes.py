import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    abort
)

from auth.decorators import login_required

from auth.auth_service import (
    get_all_users,
    get_shareable_users
)

from services.file_service import (
    create_file_metadata,
    get_file_by_id,
    share_file,
    soft_delete_file,
    remove_shared_access,
    restore_file
)

from services.s3_service import (
    upload_file_to_s3,
    generate_presigned_url
)

from services.audit_service import (
    log_event
)

file_bp = Blueprint(
    "file",
    __name__
)

@file_bp.route(
    "/upload",
    methods=["GET", "POST"]
)
@login_required
def upload_file():

    if request.method == "GET":

        return render_template(
            "upload.html"
        )

    file = request.files["file"]

    file_id = str(
        uuid.uuid4()
    )

    department = (
        session["role"]
    )

    username = (
        session["username"]
    )

    s3_key = (
        f"{department}/{file_id}"
    )

    file.seek(0, 2)

    file_size = file.tell()

    file.seek(0)

    upload_file_to_s3(
        file,
        s3_key
    )
    create_file_metadata(

        file_id=file_id,

        filename=file.filename,

        department=department,

        uploaded_by=username,

        s3_key=s3_key,

        file_size=file_size,

        content_type=file.content_type
    )
    try:

      log_event(

        username=username,

        action="UPLOAD",

        file_id=file_id,

        file_name=file.filename,

        department=department,

        details="Uploaded file"
      )

    except Exception as e:

        print(
            f"Audit log failed: {e}"
        )

    return (
        f"Uploaded "
        f"{file.filename}"
    )
@file_bp.route(
    "/file/<file_id>"
)
@login_required
def view_file(
    file_id
):

    file = get_file_by_id(
        file_id
    )

    if not file:

        abort(404)

    username = session[
        "username"
    ]

    role = session[
        "role"
    ]

    allowed = (

        role ==
        file["department"]

        or

        username in
        file["shared_with"]
    )

    if not allowed:

        abort(403)

    url = generate_presigned_url(
        file["s3_key"]
    )

    return redirect(url)

@file_bp.route(
    "/share/<file_id>",
    methods=["GET", "POST"]
)
@login_required
def share_file_route(
    file_id
):

    file = get_file_by_id(
        file_id
    )

    if not file:
        abort(404)

    role = session["role"]

    if role != file["department"]:
        abort(403)

    if request.method == "GET":

        users = get_all_users()

        users = get_shareable_users(
            file,
            users
        )

        return render_template(
            "share.html",
            file=file,
            users=users
        )

    username = request.form[
        "username"
    ]

    share_file(
        file_id,
        username
    )

    try:

        log_event(

            username=session[
                "username"
            ],

            action="SHARE",

            file_id=file_id,

            file_name=file[
                "display_name"
            ],

            department=file[
                "department"
            ],

            details=(
                f"Shared with "
                f"{username}"
               )
            )

    except Exception as e:

        print(
           f"Audit log failed: {e}"
        )

    return redirect(
        "/dashboard"
    )
@file_bp.route(
    "/delete/<file_id>"
)
@login_required
def delete_file(
    file_id
):

    file = get_file_by_id(
        file_id
    )

    if not file:

        abort(404)

    if (
        file.get("status")
        != "ACTIVE"
    ):

        abort(404)

    username = session[
        "username"
    ]

    role = session[
        "role"
    ]

    allowed = (

        role ==
        file["department"]

        or

        username in
        file.get(
            "shared_with",
            []
        )
    )

    if not allowed:

        abort(403)

    # Owner Delete
    if role == file["department"]:

        soft_delete_file(

            file_id,

            username
        )

        try:

            log_event(

                username=username,

                action="DELETE",

                file_id=file_id,

                file_name=file[
                    "display_name"
                ],

                department=file[
                    "department"
                ],

                details=(
                    f"Soft deleted "
                    f"{file['display_name']}"
                )
            )

        except Exception as e:

            print(
                f"Audit log failed: {e}"
            )

    # Shared User Remove
    else:

        remove_shared_access(

            file_id,

            username
        )

        try:

            log_event(

                username=username,

                action="REMOVE_ACCESS",

                file_id=file_id,

                file_name=file[
                    "display_name"
                ],

                department=file[
                    "department"
                ],

                details=(
                    f"Removed access to "
                    f"{file['display_name']}"
                )
            )

        except Exception as e:

            print(
                f"Audit log failed: {e}"
            )

    return redirect(
        "/dashboard"
    )
@file_bp.route(
    "/restore/<file_id>"
)
@login_required
def restore_deleted_file(
    file_id
):

    file = get_file_by_id(
        file_id
    )

    if not file:

        abort(404)

    username = session[
        "username"
    ]

    if (
        file["uploaded_by"]
        != username
    ):

        abort(403)

    if (
        file.get("status")
        != "DELETED"
    ):

        abort(400)

    restore_file(
        file_id
    )

    try:

        log_event(

            username=username,

            action="RESTORE",

            file_id=file_id,

            file_name=file[
                "display_name"
            ],

            department=file[
                "department"
            ],

            details=(
                f"Restored "
                f"{file['display_name']}"
            )
        )

    except Exception as e:

        print(
            f"Audit log failed: {e}"
        )

    return redirect(
        "/dashboard"
    )

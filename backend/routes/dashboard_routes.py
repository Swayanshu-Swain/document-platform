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

    html = f"""
    <h2>
        Welcome {username}
        ({role})
    </h2>"""

    if role == "admin":

	 html += """
	    <p>
	        <a href="/users">
	            Manage Users
	        </a>
	    </p>"""

    html+=f"""<a href="/upload">
        Upload File
    </a>

    <hr>

    <h3>Owned Files</h3>
    """

    for file in owned_files:

	    html += f"""
	    <p>

	        <a href="/file/{file['file_id']}">
	            {file['display_name']}
	        </a>

	        |

	        <a href="/share/{file['file_id']}">
	            Share
	        </a>
		|

		<a href="/delete/{file['file_id']}">
		    Delete
		</a>
	    </p>
	    """
    html += """
	<hr>

	<h3>
	Shared With Me
	</h3>
	"""
    for file in shared_files:

	    html += f"""
	    <p>

	        <a href="/file/{file['file_id']}">
	            {file['display_name']}
	        </a>
		|

		<a href="/delete/{file['file_id']}">
		    Remove
		</a>
	    </p>
	    """
    html += """
	<hr>

	<h3>
	Deleted Files
	</h3>
	"""
    for file in deleted_files:

	    html += f"""
	    <p>

	        {file['display_name']}

	        |

	        <a href="/restore/{file['file_id']}">
	            Restore
	        </a>

	    </p>
	    """

    return html

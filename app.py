from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

# Ensures user is logged in before accessing protected pages
def ensure_logged_in():
    """
    Ensures a user is logged in by checking if the user ID is in the Flask
    session cookie. If not, they are redirected to the login page.
    """
    if "user_id" not in session:
        return redirect(url_for("login"))
    return None

# -----------------------------------------------------------------------
# A1: Authentication
# -----------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    """
    Displays the login page (GET) and processes login forms (POST) through username
    and password authentication.
    """

    # If the user submitted the login form ("POST" request)...
    if request.method == "POST":

        # Set username and password variables to submitted form values
        username = request.form["username"]
        password = request.form["password"]

        # Connect to company database with PostgreSQL...
        with get_db_connection() as connection:
            with connection.cursor() as cursor:

                """
                Gets the id and password_hash of the row corresponding to the submitted
                username. It will either be a row containing (id, password_hash) if it
                finds a matching row, or None if no matches are found.

                SQL injection (malicious/dangerous SQL inserted into a form field) is
                prevented by using parameterized SQL. Since a placeholder %s is used,
                the value of username is passed separately in a tuple containing
                parameters (which is (username,) in this case), so PostgreSQL correctly
                treats the username as data and not SQL code that can harm the system.

                """
                cursor.execute("SELECT id, password_hash FROM app_user WHERE username = %s", (username,))

                # Fetches the row containing (id, password_hash) or None
                row = cursor.fetchone()

        # If a row was found and the password matches the stored hash...
        if row and check_password_hash(row[1], password):

            # Store user ID in Flask session cookie to mark them as logged in
            session["user_id"] = row[0]

            # Automatically redirect to home page (A2)
            return redirect(url_for("home"))
        
        # Else if user was not found or password is incorrect, flash error
        else:
            flash("Invalid username or password.")

    # When the request is GET (not POST) or login fails, show the login form
    return render_template("login.html")

@app.route("/logout")
def logout():

    # Clear the Flask session cookie
    session.clear()

    # Redirect to login page
    return redirect(url_for("login"))

# -----------------------------------------------------------------------
# A2: Home - Employee Overview
# -----------------------------------------------------------------------
@app.route("/")
@app.route("/home")
def home():

    # Redirect to login page if user is not authenticated
    login_redirect = ensure_logged_in()
    if login_redirect: return login_redirect

    # Get filters based on URL
    name_filter = request.args.get("search", "").strip()
    dept_filter = request.args.get("dept", "").strip()
    dept_filter = dept_filter if dept_filter != "" else None
    sort = request.args.get("sort", "name_asc")

    # Whitelisted sorting options (prevents SQL injection)
    sort_options = {
        "name_asc":     "E.Lname ASC, E.Fname ASC",
        "name_desc":    "E.Lname DESC, E.Fname DESC",
        "hours_asc":    "total_hours ASC",
        "hours_desc":   "total_hours DESC"
    }
    order = sort_options.get(sort, "E.Lname ASC")

    """
    Main employee overview query.
    Required columns:
    1. Employee full name
    2. Department name (from Department)
    3. Number of dependents (LEFT JOIN for those with 0 dependents)
    4. Number of projects (LEFT JOIN for those with 0 projects)
    5. Total hours (LEFT JOIN for those with 0 hours)
    COALESCE is used for requirements 3-5 so that the counts and sums still show up as 0.
    """

    sql = """
        SELECT 
            E.Ssn,

            -- Build full name from first name, middle initial, and last name
            E.Fname || ' ' || COALESCE(E.Minit || ' ', '') || E.Lname AS full_name,

            D.Dname AS department_name,
            COALESCE(dep.dependent_count, 0) AS dependent_count,
            COALESCE(w.project_count, 0) AS project_count,
            COALESCE(w.total_hours, 0) AS total_hours
        FROM Employee E
        LEFT JOIN Department D 
            ON E.Dno = D.Dnumber

        -- Count dependents per employee and left join to table
        LEFT JOIN (
            SELECT Essn, COUNT(*) AS dependent_count
            FROM Dependent
            GROUP BY Essn
        ) dep 
            ON dep.Essn = E.Ssn

        -- Count projects + sum hours per employee and left join to table
        LEFT JOIN (
            SELECT Essn, COUNT(*) AS project_count, SUM(Hours) AS total_hours
            FROM Works_On
            GROUP BY Essn
        ) w
            ON w.Essn = E.Ssn

        /* 
        Applies department filter and case insensitive match on employee name.

        string = '' is used for when no option is selected/no name is inputted so that the
        condition always evaluates to true and selects everything. For name, it uses
        ILIKE to match partial case-insensitive on a combined string of first and last
        name. For department, it just matches the employee department number.
        */
        WHERE (%s = '' OR (E.Fname || ' ' || E.Lname) ILIKE %s)
          AND (%s::integer IS NULL OR E.Dno = %s::integer)

        -- Orders by selected order type
        ORDER BY
    """
    sql += order + ";"

    """
    In matching for ILIKE, since SQL treats % as a wildcard meaning any sequence of
    characters, name pattern is set to start and end with %.
    """
    name_pattern = f"%{name_filter}%"

    # Connect to company database with PostgreSQL...
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            
            # Execute the SQL with the correct parameters for the filters
            cursor.execute(sql, (name_filter, name_pattern, dept_filter, dept_filter)) # type: ignore[arg-type]

            # Fetch the matched employee list with relevant information as defined in the SQL
            employees = cursor.fetchall()

            # Get department list
            cursor.execute("SELECT Dnumber, Dname FROM Department ORDER BY Dname;")
            departments = cursor.fetchall()

    return render_template(
        "home.html",
        employees=employees,
        departments=departments,
        search=name_filter,
        dept_filter=dept_filter,
        sort=sort
    )

# -----------------------------------------------------------------------
# A3: Projects - Portfolio Summary
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# A4: Project Detials & Assignment "Upsert"
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# A5: Employee Managment (CRUD)
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# A6: Managers Overview
# -----------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
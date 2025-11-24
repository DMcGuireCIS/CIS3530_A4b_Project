# 1. Setup environment

------------------------------------------------------------------
Create virtual environment for every new machine (must run once):

python -m venv .venv

OR

python3 -m venv .venv

------------------------------------------------------------------
Each time you continue working:

Linux/macOS: 
source .venv/bin/activate

Windows (PowerShell):
.venv\Scripts\Activate.ps1

Windows (cmd):
.venv\Scripts\activate.bat

Windows (Git Bash):
source .venv/Scripts/activate

*If PowerShell says running scripts is disabled, run once:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

------------------------------------------------------------------
Install required packages:
pip install -r requirements.txt

# 2. Environment Variables

Before running the app, you must define a SECRET_KEY.

The application loads it from:
    app.secret_key = os.environ["SECRET_KEY"]

Generate a secure key:
python  
>>> import secrets  
>>> secrets.token_hex(32)  

Copy output key

------------------------------------------------------------------
Option A - Set it as an environment variable:

Linux/macOS/Git Bash:  
export SECRET_KEY="secret_key_here"

Windows (PowerShell):  
$env:SECRET_KEY="secret_key_here"  

------------------------------------------------------------------
Option B - Use a .env file:

Create a file named .env in the project root, containing:

SECRET_KEY=secret_key_here

(Flask loads .env automatically because load_dotenv() is used in app.py)

# 3. Setup database (example)

createdb -U postgres cis3530_teamdb  

Linux/macOS/Git Bash:  
export DATABASE_URL="postgresql://postgres:yourpassword@localhost/cis3530_teamdb" 

Windows (PowerShell):  
$env:DATABASE_URL="postgresql://postgres:yourpassword@localhost/cis3530_teamdb"   

# 4. Load schema and your additions

Linux/macOS/Git Bash:  
psql -d "$env:DATABASE_URL" -f company_v3.02.sql  
psql -d "$env:DATABASE_URL" -f team_setup.sql  

Windows (PowerShell):  
psql -d $DATABASE_URL -f company_v3.02.sql  
psql -d $DATABASE_URL -f team_setup.sql  

Note: On consequent runs of these lines, you may need to drop and recreate the database if you see many "transactions" aborted messages:  
dropdb -U postgres cis3530_teamdb  
createdb -U postgres cis3530_teamdb  

# 5. Run the app

flask run

# 6. Login as admin or viewer for RBAC

Admin:
    Username: admin  
    Password: somepassword  

Viewer:
    Username: viewer   
    Password: apassword  

### Bonus Implementations

All bonus implementations are implemented.
That means:
- RBAC where only admin can see and use Add/Edit/Delete options
- CSV "Export" button on Home and Projects page for currently filtered list
- Excel import button for .xlsx files to insert new rows into chosen table (only available for admin role)

### Other notes

Password hashes were generated correctly from command line by running:

python  
>>> from werkzeug.security import generate_password_hash  
>>> print(generate_password_hash("somepassword"))  

Then, the generated hash was inputted into the app_user table.
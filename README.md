### 1. Setup environment

------------------------------------------------------------------
Create virtual environment for every new machine (must run once):

python -m venv .venv

OR

python3 -m venv .venv

------------------------------------------------------------------
Each time you continue working:

Linux/Mac: 
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

# 2. Setup database (example)

createdb -U postgres cis3530_teamdb

Linux/Mac:
export DATABASE_URL="postgresql://user:pass@localhost/cis3530_teamdb"

Windows (PowerShell):
$env:DATABASE_URL="postgresql://postgres:yourpassword@localhost/cis3530_teamdb"

Windows (Git Bash):
export DATABASE_URL="postgresql://postgres:yourpassword@localhost/cis3530_teamdb"

# 3. Load schema and your additions

psql -d $DATABASE_URL -f company_v3.02.sql
psql -d $DATABASE_URL -f team_setup.sql

OR

psql -d "$env:DATABASE_URL" -f company_v3.02.sql
psql -d "$env:DATABASE_URL" -f team_setup.sql

# 4. Run the app
flask run

# 5. Login as admin
Username: admin
Password: somepassword

### For group members

Follow this readme to get your program up running and check that it works by copy pasting the URL after flask run to your browser. You should be able to login as admin which was defined in team_setup.sql. I generated the password_hash by running this from terminal...

python
from werkzeug.security import generate_password_hash
print(generate_password_hash("somepassword"))

Then, I copy pasted the hash to put as a parameter for password_hash. In this way, you can create your own users in team_setup.sql for your own testing (just follow the format I use). Right now we just have an admin user, but you can create your own "viewer" user with another password.
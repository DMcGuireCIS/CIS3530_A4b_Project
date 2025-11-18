import os
import psycopg

def get_db_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])
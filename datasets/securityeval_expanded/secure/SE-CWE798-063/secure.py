import mysql.connector
import os
from pathlib import Path

def getDBConnection():
    '''
    Return a MySQL database connection.
    '''
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_database = os.environ.get('DB_DATABASE')
    
    if not all([db_user, db_password, db_host, db_database]):
        raise ValueError("Database credentials must be provided via environment variables: DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE")
    
    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_database
    )
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host="127.0.0.1",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    auth_plugin='mysql_native_password'
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS flights_users")
cursor.execute("USE flights_users")


import sqlite3 as sql
import bcrypt as bcrypt


# Retrieve the salt for given a username
def retrieve_salt(username):
    # Connect to the database and establish a cursor
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Grab the salt from the database
    salt = cur.execute("SELECT salt FROM users WHERE username = (?)", (username,))
    salt = salt.fetchone()

    # As the salt is returned as a tuple, get the 'blob' only
    salt = salt[0]

    return salt


# Hash the password, given a username and password
def hash_pass(username, password):
    # First salt is predetermined
    salt1 = b"$2b$12$sXtl2UlBRwnpIxyoJEPcmu"

    # Second salt is from the database
    salt2 = retrieve_salt(username)

    # Encode the password so that python can handle it
    encoded = password.encode()

    # Hash twice, each with the separate salts
    hashed = bcrypt.hashpw(password=encoded, salt=salt1)
    doubleHashed = bcrypt.hashpw(password=hashed, salt=salt2)

    return doubleHashed

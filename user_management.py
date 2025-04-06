import sqlite3 as sql
import time
import random
from password_hashing import hashPass
import bcrypt
from data_handler import make_web_safe


def insertUser(username, password, DoB):
    # Connect to the database and establish a cursor
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Make the inputs safe
    safe_user = make_web_safe(username)
    safe_pass = make_web_safe(password)
    safe_DoB = make_web_safe(DoB)

    # Generate a salt to go with the user
    salt = bcrypt.gensalt()

    hashedpw = hashPass(safe_user, safe_pass, salt)

    # Insert the users details into the database
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth,salt) VALUES (?,?,?,?)",
        (
            safe_user,
            hashedpw,
            safe_DoB,
            salt,
        ),
    )

    # Commit the changes and close the connection
    con.commit()
    con.close()


def manageBackend():
    # Plain text log of visitor count as requested by Unsecure PWA management
    with open("visitor_log.txt", "r") as file:
        number = int(file.read().strip())
        number += 1
    with open("visitor_log.txt", "w") as file:
        file.write(str(number))
    # Simulate response time of heavy app for testing purposes
    time.sleep(random.randint(80, 90) / 1000)


def retrieveUsers(username, password):
    # Establish a connection to the database
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Make the inputs safe
    safe_user = make_web_safe(username)
    safe_pass = make_web_safe(password)

    # Select the user with the specified username
    cur.execute("SELECT * FROM users WHERE username = (?)", (safe_user,))

    # If the specified username is not in the database
    if cur.fetchone() is None:
        # Return false and close the connection to the database
        con.close()
        return False

    # If this point is reached, the user exists
    else:
        hashedpw = hashPass(safe_user, safe_pass, None)
        cur.execute("SELECT * FROM users WHERE password = (?)", (hashedpw,))

        manageBackend()

        if cur.fetchone() is None:
            con.close()
            return False
        else:
            con.close()
            return True


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Make the feedback safe
    safe_feedback = make_web_safe(feedback)
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (safe_feedback,))
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()

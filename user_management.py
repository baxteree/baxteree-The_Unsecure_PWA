import sqlite3 as sql
import time
import random
from password_hashing import hashPass
import bcrypt


def insertUser(username, password, DoB):
    # Connect to the database and establish a cursor
    con = sql.connect("database_files/database.db")
    cur = con.cursor()

    # Generate a salt to go with the user
    salt = bcrypt.gensalt()

    hashedpw = hashPass(username, password, salt)

    # Insert the users details into the database
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth,salt) VALUES (?,?,?,?)",
        (
            username,
            hashedpw,
            DoB,
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

    # Select the user with the specified username
    cur.execute("SELECT * FROM users WHERE username = (?)", (username,))

    # If the specified username is not in the database
    if cur.fetchone() is None:
        # Return false and close the connection to the database
        con.close()
        return False

    # If this point is reached, the user exists
    else:
        hashedpw = hashPass(username, password, None)
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
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
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

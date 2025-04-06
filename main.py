from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from data_handler import checkpw_2
import user_management as dbHandler
import logging

logger = logging.getLogger(__name__)

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)


@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]

        try:
            # Check if the user entered a valid password
            strong_password = checkpw_2(password)
        except TypeError:
            logger.error(f"Type errors for password: {password}")
            print("TypeError has been logged")
            return render_template("/signup.html")

        except ValueError as inst:
            # If not, return an error message explaining why it was invalid
            print(f"Not a valid password because it {inst.args}.")
            
            # Reload the signup page, with the form cleared
            return render_template("/signup.html")
        except Exception as inst:
            print(f"Log as a {type(inst)}")
            return render_template("/signup.html")
        else:
            # Otherwise if the password is valid, 
            # insert the user into the database
            dbHandler.insertUser(username, strong_password, DoB)

        return render_template("/index.html")

    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=8080)

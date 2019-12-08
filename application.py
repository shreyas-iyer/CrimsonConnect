# Large parts of the code are copied from CS50 Finance source code provided

import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///interests.db")

# Homepage where users sees the list of classes they're enrolled in and add classes
@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT * FROM classes WHERE username=:username ORDER BY subject", username=session["username"])

    # If the user has no classes in their profile, prompt them to add a class to their profile
    if not rows:
        return render_template("opening.html")

    return render_template("index.html", rows=rows)


# Copied from CS50 Finance Pset code
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Copied from CS50 Finance Pset code
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


# Copied from CS50 Finance Pset code and edited
@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        firstname = request.form.get("firstname").capitalize()
        lastname = request.form.get("lastname").capitalize()
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        elif not firstname:
            return apology("must enter first name")

        elif not lastname:
            return apology("must enter last name")

        # Ensure password was submitted
        elif not password:
            return apology("must provide password")

        # Check if passwords match
        if password != confirmation:
            return apology('passwords do not match', 403)

        # Select all entries in the table with that user name
        testname = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # If username already exists return error
        if len(testname) == 1:
            return apology('username is taken', 403)

        else:

            # Generate password hash
            hash = generate_password_hash(password)

            # Insert new user's username and hashed password to SQL database
            db.execute("INSERT INTO users (firstname, lastname, username, hash) VALUES (:firstname, :lastname, :username, :hash)",
                       firstname=firstname, lastname=lastname, username=username, hash=hash)

        # Select id number for new user
        id_number = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # Remember which user has logged in
        session["user_id"] = id_number[0]["id"]
        session["username"] = id_number[0]["username"]

        # Redirect to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# Change password
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":

        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Check if current password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], request.form.get("current_password")):
            return apology("incorrect Password", 403)

        # Check if new passwords match
        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        new_pass = generate_password_hash(request.form.get("confirmation"))

        # Insert new password hash into the current user's entry in the users table
        db.execute("UPDATE users SET hash = :new_pass WHERE id = :user_id", new_pass=new_pass, user_id=session["user_id"])

        return redirect("/")

    else:
        return render_template("change_password.html")


# Lists current friends
@app.route("/friends")
def friends():

    # Select all friends of the current user
    friends = db.execute(
        "SELECT * FROM users WHERE username IN (SELECT recipient FROM friends WHERE sender=:user AND accepted='TRUE') OR username IN (SELECT sender FROM friends WHERE recipient=:user AND accepted='TRUE')", user=session["username"])

    # If the user has no friends return a screen which prompts the user to add friends
    if not friends:
        return render_template("nofriends.html")

    return render_template("friends.html", rows=friends)


# View add friends and method to submit add friends form
@app.route("/add_friends", methods=["GET", "POST"])
@login_required
def add_friends():
    if request.method == "POST":

        # Store username form input in variable username
        username = request.form.get("username")

        # Ensure input for username
        if not username:
            return render_template("blank.html", title="Enter username", message="You must enter a username")

        # If the input is the current user's username, tell the user they cannot add themself as a friend
        if username == session["username"]:
            return apology("You cannot add yourself as a friend")

        # Select user which has the the inputted username
        user = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        # if no user has the username, inform the user the person does not exist
        if not user:
            return render_template("blank.html", title="User Not Found", message="User not found")

        # Check friendship of inputted username and current user
        if checkFriendship(session["username"], username) == True:

            # Tell user they are already friends with this user
            return render_template("blank.html", title="Already Friends", message="You are already friends with this individual")

        # Users are not friends
        else:
            friends = db.execute("SELECT * FROM friends WHERE (sender=:username AND recipient=:user) OR (sender=:user AND recipient=:username)",
                                 username=username, user=session["username"])

            # If there are no requests between the two users, insert the request in the friends table
            if not friends:
                db.execute("INSERT INTO friends (sender, recipient) VALUES (:sender, :recipient)",
                            sender=session["username"], recipient=username)

            # If a request has already been sent/received and not yet accepted/ignored inform the user
            else:
                return render_template("blank.html", title="Request Already Sent", message="Request in progress - reply pending")

        return redirect("/friends")

    # Return the add_friends template if the method is get
    else:
        return render_template("add_friends.html")


# View friend's profile page - friend specified by username
@app.route("/view_friend/<username1>")
def view_friend(username1):
    # If username is the same as the current users, go to index
    if username1 == session["username"]:
        return redirect("/")

    # Select user with username1
    firstname = db.execute("SELECT * FROM users WHERE username=:username", username=username1)

    # Find all classes user with username1 has in common with the current user
    rows = db.execute("SELECT * FROM classes WHERE subject IN (SELECT subject FROM classes WHERE username=:username) AND number IN (SELECT number FROM classes WHERE username=:username) AND username=:user",
                      username=session["username"], user=username1)

    # Find all friends of user with username1
    friends = db.execute("SELECT * FROM users WHERE username IN (SELECT recipient FROM friends WHERE sender=:user) OR username IN (SELECT sender FROM friends WHERE recipient=:user)", user=username1)

    # If the current user and the clicked user are friends display their page
    if checkFriendship(session["username"], username1) == True:

        # If they have no classes in common, inform them they have no common classes
        if not rows:
            return render_template("no_common_classes.html",firstname=firstname[0]["firstname"], lastname=firstname[0]["lastname"], username=username1, names=friends)

        else:
            return render_template("view_friend.html", firstname=firstname[0]["firstname"], lastname=firstname[0]["lastname"], username=username1, rows=rows, names=friends)

    # If current user and requested user aren't friends display not_friends.html page
    else:
        return render_template("not_friends.html", firstname=firstname[0]["firstname"], lastname=firstname[0]["lastname"], username=username1)


# Displays friend request page
@app.route("/friend_request")
def friend_request():
    rows = db.execute("SELECT users.firstname, users.lastname, friends.sender FROM users JOIN friends ON users.username = friends.sender WHERE recipient = :username AND accepted = 'FALSE'",
        username=session["username"])

    # If there are no friend requests, inform the user
    if not rows:
        return render_template("blank.html", title="Friend Requests", message="You have no friend requests")

    # If there are friend requests, pass the rows variable to the template friend_request
    return render_template("friend_request.html", rows=rows)


# Accept request function for friend request page
@app.route("/accept_request/<username>", methods=["POST"])
def accept_request(username):

    # Set accepted status to TRUE
    db.execute("UPDATE friends SET accepted='TRUE' WHERE sender=:username AND recipient=:name", username=username, name=session["username"])

    return redirect("/friends")


# Ignore request function for friend request page
@app.route("/ignore_request/<username>", methods=["POST"])
def ignore_request(username):

    # Delete request from friends table
    # This allows the user to send a request in the future even if it was ignore previously
    db.execute("DELETE FROM friends WHERE sender=:username AND recipient=:user", username=username, user=session["username"])
    return redirect("/friends")


# Page to add a class to your profile
@app.route("/add_class", methods=["POST", "GET"])
def add_class():
    if request.method == "POST":
        number = request.form.get("number")
        subject = request.form.get("subject")

        # Ensure input for the course number
        if not number:
            return apology("must enter a course number")

        # SQL command variable to see if the user is already enrolled in the class
        existing = db.execute("SELECT * FROM classes WHERE username= :username AND subject=:subject AND number=:number",
                              username=session["username"], subject=subject, number=number)

        # If the user is not already in the class do the following
        if not existing:

            # I did not check whether the class is in the directory, since many classes
            # are not listed in the directory
            # I didn't want to prompt users with an apology for valid input.
            db.execute("INSERT INTO classes (username, subject, number) VALUES (:username, :subject, :number)",
                        username=session["username"], subject=subject, number=number)

            return redirect("/")

        # If the user is already in the class do the following
        else:
            return apology("This class is already part of your profile")

    else:

        # Integrated course data - selects all distinct subjects from course list
        rows = db.execute("SELECT DISTINCT subject FROM realclasses ORDER BY subject;")

        return render_template("update_classes.html", rows=rows)


# View a specific class's page
@app.route("/view_class/<subject>/<number>")
def view_class(subject, number):

    # Select all students in the class - including the current user
    rows = db.execute("SELECT users.firstname, users.lastname, users.username FROM users JOIN classes ON users.username = classes.username WHERE subject=:subject AND number=:number", number=number,subject=subject)

    # Select course stream chats for the specified class
    chats = db.execute("SELECT * FROM streams JOIN users ON users.username = streams.sender where subject=:subject AND number=:number ORDER BY time DESC", subject=subject, number=number)

    # If there are no course stream chats then display the nochats template
    if not chats:
        return render_template("view_class_nochats.html", rows=rows, subject=subject , number=number)

    return render_template("view_class.html", rows=rows, chats=chats, subject=subject , number=number)


# Route to remove a course from a user's profile
@app.route("/remove/<subject>/<number>", methods=["POST"])
def remove(subject, number):

    # Delete specific entry from the table classes for the current user
    db.execute("DELETE FROM classes WHERE username=:username AND subject=:subject AND number=:number", username=session["username"], subject=subject, number=number)

    # Delete user's posts from the course stream
    db.execute("DELETE FROM streams WHERE sender=:username AND subject=:subject AND number=:number", username=session["username"], subject=subject, number=number)

    return redirect("/")


# Post message to course stream
@app.route("/post_stream/<subject>/<number>", methods=["POST", "GET"])
def post_stream(subject, number):
    if request.method == "POST":
        message = request.form.get("message")
        topic = request.form.get("subject")

        # Ensure input for message
        if not message:
            return apology("You must enter a message")

        # Ensure input for subject
        if not topic:
            return apology("You must enter a subject")

        # Insert message and subject into the streams table
        db.execute("INSERT INTO streams (sender, topic, number, subject, message) VALUES (:username, :topic, :number, :subject, :message)",
        username=session["username"], topic=topic, number=number, subject=subject, message=message)

        return redirect(f"/view_class/{subject}/{number}")

    else:
        return render_template("post_stream.html", subject=subject, number=number)


@app.route("/chat",)
def chat():
    rows = db.execute("SELECT * FROM chats JOIN users ON chats.sender = users.username WHERE recipient=:username AND read='FALSE' ORDER BY time DESC", username=session["username"])

    # If there are no unread chats
    if not rows:
        return render_template("no_chats.html")

    # Otherwise list the unread chats
    return render_template("chat.html", rows=rows)


@app.route("/send_chat", methods=["GET","POST"])
def send_chat():
    if request.method == "POST":
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Ensure input for recipient
        if not recipient:
            return apology("Please enter a recipient username")

        # Ensure input for subject
        if not subject:
            return apology("Please enter a subject")

        # Ensure input for message
        if not message:
            return apology("Please enter a message")

        exists = db.execute("SELECT * FROM users WHERE username=:recipient", recipient=recipient)

        # If the user does not exist
        if not exists:
            return apology("This user does not exist")

        # If these two users are not friends, tell the user they cannot message
        if checkFriendship(recipient, session["username"]) == False:
            return apology("You can't message this person until you're friends.")

        # Insert chat into sqlite table chats
        db.execute("INSERT INTO chats (sender, recipient, subject, message) VALUES (:sender, :recipient, :subject, :message)",
                   sender=session["username"], recipient=recipient, message=message, subject=subject)
        return redirect("/chat")

    else:
        return render_template("send_chat.html")


# View messages previously sent by the current user
@app.route("/view_sent", methods=["POST"])
def view_sent():

    # Pick messages where the sender was the current user - order by newest chat first
    rows = db.execute("SELECT * FROM chats JOIN users ON chats.recipient = users.username WHERE sender=:username ORDER BY time DESC", username=session["username"])

    # If there are no entries in "rows" then inform the user they've sent no messages
    if not rows:
        return render_template("blank.html", title="No Sent Message", message="You have not sent any messages yet")

    return render_template("view_sent.html", rows=rows)


# View all read messages
@app.route("/view_all", methods=["POST"])
def view_all():

    # Pick all messages addressed to current user that have been read - order by newest chat first
    rows = db.execute("SELECT * FROM chats JOIN users ON chats.sender = users.username WHERE recipient=:username AND read='TRUE' ORDER BY time DESC", username=session["username"])

    # If there are no read messages, inform the user
    if not rows:
        return render_template("blank.html", title="No Read Message", message="You have no read messages")

    return render_template("view_all_chats.html", rows=rows)


# Reply to message
@app.route("/reply/<sender>/<time>", methods=["POST", "GET"])
def reply(sender, time):
    if request.method == "POST":

        # Select specific chat from chats table
        rows = db.execute("SELECT * FROM chats JOIN users ON chats.sender = users.username WHERE sender=:sender AND time=:time", sender=sender, time=time)

        # Mark chat as read in the chats table
        db.execute("UPDATE chats SET read = 'TRUE' WHERE sender=:sender AND recipient=:username AND time=:time", sender=sender, time=time, username=session["username"])

        # Obtain message from the user
        message = request.form.get("message")
        subject = (f"Re: {rows[0]['subject']}")

        # Ensure input for message
        if not message:
            return apology("Please insert a message")

        # Insert new chat into chats
        db.execute("INSERT INTO chats (sender, recipient, subject, message) VALUES (:sender, :recipient, :subject, :message)",
        recipient=sender,  sender=session["username"], message=message, subject=subject)

        return redirect("/chat")

    else:
        rows = db.execute("SELECT * FROM chats JOIN users ON chats.sender = users.username WHERE sender=:sender AND time=:time", sender=sender, time=time)
        return render_template("reply.html", rows=rows[0])


@app.route("/mark_as_read/<sender>/<time>", methods=["POST"])
def mark_as_read(sender, time):

    # Mark message as read by setting read='TRUE'
    db.execute("UPDATE chats SET read = 'TRUE' WHERE sender=:sender AND recipient=:username AND time=:time", sender=sender, time=time, username=session["username"])

    return redirect("/chat")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# Function to check the friendship of two users given their usernames
def checkFriendship (username1, username2):

    # Select any entries which indicates the users are both friends
    friends = db.execute("SELECT * FROM friends WHERE accepted='TRUE' AND ((recipient=:username1 AND sender=:username2) OR (sender=:username1 AND recipient=:username2))", username1=username1, username2=username2)

    # If no entries exists return False
    if not friends:
        return False

    # If entries exist then these two users are friends, return True
    else:
        return True
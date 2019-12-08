# Crimson Connection

Crimson Connection is a social network that enables users to find other students in their classes,
post messages to the entire class, and chat with other users. The network is designed in such a way
that you can friend anyone at Harvard College, so you are not limited to only contacting individuals
in your classes.

View this project's YouTube video: https://youtu.be/onPCTZ41hpo

More information about the design of the program can be found in `DESIGN.md`.

## Opening the website
This program was designed on CS50 IDE. It is recommended that the program be run in the same environment.

1. If the course list data is not already stored in `interests.db`, open `upload_course_data.py`.
In the terminal, enter `python upload_course_data.py` and wait until the program finishes running.
If the course list data is already stored, ignore this step.

2. In the CS50 IDE, enter `cd finalproject` into the terminal to navigate to that directory. After
that, enter `flask run` into the terminal. You should then see a link provided by the server. Click
it to visit the Crimson Connection website.

## Usage
### Registering for an Account
1. Click register
2. Enter your first name, last name, username, and password (two times for confirmation)
3. You will be directed to a home page that prompts you to add classes - click the "Add Classes" button
4. Select your class's subject and enter its course code as a single entry with no spaces (i.e. "101a")
5. You will be taken back to your home page - you will now see the class you just added listed appear

### Classes
On the home page there is an "Add Classes" button at the bottom of the page. Click this button and
follow steps 4 and 5 of registering for an account.

On the home page, click the button of any class you're enrolled in. You'll be taken to a course page.
Here you can post to the course stream (a course-wide chat), see messages in the course stream,
and see which peers are in your class.

To post to the course stream click the "Add Post to Course Stream" button. You will be taken to a
page where you can enter a subject and message. Once you enter your post and click the "Post to
Course Stream" button to submit, you will be redirected back to the class page, where you will now
see your post (and likely other posts below it). The post will display the subject, who posted it,
and the time posted. To see the contents of the message, click the post and the message will appear.

In the class page, you can click on any person's listing in the student table to visit their profile
page.

To remove a class from your profile, there is a button at the bottom of the specific class page that
you can click.

### Friends
To view friend requests, click the "Friend Requests" button in the navbar. If you have no friend
requests you will be told so. Otherwise, the person's full name and username will appear along with
and "Accept" and "Ignore button" for each request. Click the appropriate button to either add that
person to your friends list or to ignore their friend request. Regardless of what you choose, you
will be taken to the friends list page.

The "Friends" button in the navbar of the page take you to a page that lists all of your friends.
On that page, you can find each friend's full name and username listed in a table. If you click on
that person's row in the table you will be taken to their profile page.

At the bottom of the friends page, there is an "Add Friends" button. On the add friends page, enter
the username of the friend you would like to request. If you've already sent a request, the website
will let you know.

### Chats
On Crimson Connection, you can only chat with your friends. To view your inbox, click "Inbox" in the
navbar. You will be taken to a page that lists all your unread chats. Each chat will display a subject,
a sender, and the time sent.

Click on a message and its contents will appear. Below each message is a "Mark as Read" and "Reply"
button. Clicking "Mark as Read" adds the message to you read messages. Learn more about "Reply"
below. At the bottom of the Inbox are two buttons: "View Sent Messages" and "View Read Messages".
Click each respectively to view messages you've sent and messages you've marked as read.


Upon clicking the reply button you will be taken to a page where you can enter a message in response.
The page will display the recipient, their previous message, and the subject will autofill to "Re:
{ the received subject }".

To send a chat, click "Send Chat" in the navbar. Enter a username, subject, and message. Simply
click the "Send Message" button to send that message.


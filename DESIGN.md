# Design Document

## Front-End
The front end was largely designed with HTML and CSS. For many of the buttons forms, and other design
features, Bootstrap was used to stylize these elements. Throughout the code, there are references to
Boostrap.

### Major Design Decisions
1. Used an HTML template to make writing new HTML pages more simple and easier to read
2. Used CSS to stylize several elements such as tables, text, and buttons
3. The functional to insert 'for' and 'if' statements into HTML was extremely helpful for iterating
through SQLite database data

### Button Styling
Since there were a variety of button sizes and shapes for this program, I created several
ids and classes for each button to style each one different. Generally, I used ids since
I was already using a Bootstrap button class. This allowed for consistency in button size,
text size, and text color for similar buttons. This was largely an aesthetic concern.

### Grouping
I decided to keep four functions in the navbar: Friend Requests, Friends List, Send Chat, and Inbox.
In my mind, these functions did not seem to fall into any other bucket. Moreover, a function like
Friend Requests needs to be checked often as does not distinctly fit within the scope of a list of
friends. Other functions, such as the "Add Class" button, for example, is found at the bottom of the
home page will lists all the classes the user is enrolled in. Similarly, the "Add Friends" button is
found on the Friends List page. Within each page is greater functionality.

Horizontal lines were used on each page to separate different information or buttons from one another.
For example, on the View Class page there is a line between the course stream messages, the student
list, and the "Remove Class" button. This is mainly for visual appeal and aesthetic pleasure. It is
also easier to see different sections of each webpage with this visual barrier

### Javascript
I used Javascript in this website for all messages, including chats and course streams. This code
was copied from W3, but its main function was to hide the contents of a message until the message
icon was clicked on. There were two elements: a collapsible and content. The collapsible displays
each message's subject, sender/recipient (depending on the page), and the time sent/received. If
the user clicks the collapsible, then the user will be shown the contents of the message right below.

## Back-End
The back-end used Python and flask.

### Functions and App Routes
Several functions were created for different operations in the program. This was done using flask
and Python. The reason is three-fold:
1. Assigning multiple methods to a function enables the source code to be more compact and easy to read
2. The functionality of these programs for web apps is simplistic and straightforward than other programs
3. SQLite's seamless integration with Python and Flask

In addition, I used the functionality that a variable can be passed to a function for an app route.
For example, the view class function takes a subject and number input which correspond to the course
subect and the course number. Therefore, the function only displays the unique page for that course
instead of displaying a generic course page (or even worse, a wrong course page).

### Course Data Integration

I integrated the course data into this program. In `upload_course_data.py`, I used `json.load()` to
import the course data into a table in a SQLite database. I then iterated through all these subjects
and created a dropdown list for users to browse through when adding a class. Therefore, users could
not select a subject that did not exist. However, there is one caveat. The course list was not
exhaustive, so I did not check if the number was in the course list (i.e. Ec 10a is not in the list).
This opens the program up to some errors, but I considered that it would be better to add functionality
to every class than to limit Crimson Connection's usage to 2,500 classes only.

### Data Storage
Most of Crimson Connection operates using SQLite databases. Users, friends, friend requests what
classes users are enrolled in, chats, and course stream posts are store in respective tables of
`interests.db`.

The intent for doing this was two-fold:
1. This website required the storage of several different types of "permanent" data (unique data is
stored for each user after a user logs out). It made much more sense to aggregate this data in a
SQLite database where it was highly accessible and easy to find.

2. SQLite databases are integrated well with flask, HTML, Python, and CS50 IDE. It was often the case
when designing this program that SQLite data had to be iterated over. The functionality of dictionaries
with HTML made it easy to do this.



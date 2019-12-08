#import json to manipualte the json file format the course data was provided in
import json
from cs50 import SQL

db = SQL("sqlite:///interests.db")

# Open the courses2.json file using json.load to convert the data into a python dictionary
# Used https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/ for reference #
with open('courses2.json', 'r', encoding='utf-8') as data_file:
    data = json.load(data_file)

    # Iterate through each row in the data and write the subject and course number in a SQL database
    for p in range(len(data)):
        db.execute("INSERT INTO realclasses (subject, number) VALUES(:subject,:number)", subject=data[p]["classes"][0]["catalogSubject"], number=data[p]["classes"][0]["courseNumber"])
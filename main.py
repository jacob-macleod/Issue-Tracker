from flask import Flask, render_template, request, redirect, url_for, flash, make_response

import csv
import os

app = Flask(__name__)

def remove_first_and_last_characters (string) :
        #Remove the first and last characters (') of string - convert it to an array first
        string = list(string)
        string_stripped = ""

        #Reconstruct the array back into a string, not using the first and last characters
        for i in range (0, len(string)) :
            if i == 0 or i == len(string)-1 :
                pass
            else :
                string_stripped = string_stripped + string[i]
        
        return string_stripped


#Delete specific line number from csv
def delete_line(original_file, line_number):
    is_skipped = False
    current_index = 0
    dummy_file = original_file + '.bak'
    # Open the origional and dummy files
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Copy every line in the origional file to the dumy file
        for line in read_obj:
            # If current line number matches the given line number then skip
            if current_index != line_number:
                write_obj.write(line)
            else:
                is_skipped = True
            current_index += 1

    # If any line is skipped then rename dummy file as the origional file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        #Delete the origional file
        os.remove(dummy_file)


@app.route('/', methods = ['post', 'get'])
def index():
    issue_names = ""
    issue_tags = ""
    csv_length = 0

    #Read the data.csv file
    with open('data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            #Append the name of the issue in the csv file to the issue_names string
            issue_names = issue_names + row[0] + "%"

            #Count the numbers of rows cycled through to find the number of lines in the csv
            csv_length = csv_length + 1

            #Append the text of the tags to a variable
            issue_tags = issue_tags + row[2] + "%"

    issue_names_length = csv_length
    #TODO: CHANGE TEMPLATE RETURNED LATER!
    return render_template('index.html', issue_names=issue_names, issue_names_length=issue_names_length, issue_tags=issue_tags)  

@app.route("/issue", methods = ['post', 'get'])
def issue () :
    tags = ""
    desc = ""

    issue_name = request.cookies.get("issue")
    #Remove '<span' from issue_name
    issue_name = issue_name.split('<')[0] + "'"

    #Remove first and last characters (')
    issue_name = remove_first_and_last_characters(issue_name)

    with open('data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] == issue_name:
                desc = row[1]
                tags = row[2]


    return render_template("issue.html", title=issue_name, desc=desc, tags=tags)

@app.route('/create_issue', methods = ['post', 'get'])
def create_issue () :
    #If somebody presses submit after entering issue details
    if request.method == "POST": 
       # getting input
       title = request.form.get("title") 
       desc = request.form.get("desc")  
       tags = request.form.get("tags")  

       #Save input to file
       file = open("data.csv", 'a')
       file.write("\n" + title + ", " + desc + ", " + tags)
       return render_template("issue_created.html")

    return render_template("create_issue.html")


@app.route("/delete_issue", methods = ["post", "get"])
def delete_issue () :
    index = 0

    if request.method == "POST" :
        title = request.form.get("name")

        #Delete issue
        with open('data.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                if row[0] == title :
                    line_to_deleted = index
                index = index + 1

            delete_line("data.csv", line_to_deleted)
        return render_template("issue_deleted.html")
        
    return render_template("delete_issue.html")

#Runs the webserver and the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
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


def add_comment(original_file, line_number, comment):
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
                #For the comment collum, write the data it already has plus comment
                split_line = line.split(',')
                write_obj.write(split_line[0] + ',' + split_line[1] + ',' + split_line[2] + ',' + split_line[3].split("\n")[0] + "newlineToken" + comment + ',' + split_line[4] + "," + split_line[5])
            current_index = current_index + 1
                        

    #Rename dummy file as the origional file then delete the dummy file
    os.remove(original_file)
    os.rename(dummy_file, original_file)

def add_person(original_file, line_number, name):
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
                #For the person collum, write the data it already has plus comment
                split_line = line.split(',')
                new_line = split_line[0] + ',' + split_line[1] + ',' + split_line[2] + ',' + split_line[3] + ',' + split_line[4] + name + "newlineToken" + "," + split_line[5]
                write_obj.write(new_line)
            current_index = current_index + 1

    #Rename dummy file as the origional file then delete the dummy file
    os.remove(original_file)
    os.rename(dummy_file, original_file)
                        
def change_issue_status(original_file, line_number, status):
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
                #For the issue collum, write the data it already has plus comment
                split_line = line.split(',')
                write_obj.write(split_line[0] + ',' + split_line[1] + ',' + split_line[2] + ',' + split_line[3] + ',' + split_line[4] + "," + status + "\n")
            current_index = current_index + 1

    #Rename dummy file as the origional file then delete the dummy file
    os.remove(original_file)
    os.rename(dummy_file, original_file)

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
#TODO: Add a seperate page that you can click onto to show closed issues - closed issues do not show by default - so like a "View Closed" button
def index():
    issue_names = ""
    issue_tags = ""
    csv_length = 0

    #Read the data.csv file
    with open('data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            #If the issue is still open
            if row[5] != "Close" :
                #Append the name of the issue in the csv file to the issue_names string
                issue_names = issue_names + row[0] + "%"

                #Count the numbers of rows cycled through to find the number of lines in the csv
                csv_length = csv_length + 1

                #Append the text of the tags to a variable
                issue_tags = issue_tags + row[2] + "%"

    issue_names_length = csv_length
    return render_template('index.html', issue_names=issue_names, issue_names_length=issue_names_length, issue_tags=issue_tags)  


@app.route('/closed', methods = ['post', 'get'])
#TODO: Add a seperate page that you can click onto to show closed issues - closed issues do not show by default - so like a "View Closed" button
def closed():
    issue_names = ""
    issue_tags = ""
    csv_length = 0

    #Read the data.csv file
    with open('data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            #If the issue is not open
            if row[5] != "Open" :
                #Append the name of the issue in the csv file to the issue_names string
                issue_names = issue_names + row[0] + "%"

                #Count the numbers of rows cycled through to find the number of lines in the csv
                csv_length = csv_length + 1

                #Append the text of the tags to a variable
                issue_tags = issue_tags + row[2] + "%"

    issue_names_length = csv_length
    return render_template('closed_issues.html', issue_names=issue_names, issue_names_length=issue_names_length, issue_tags=issue_tags)

@app.route("/issue", methods = ['post', 'get'])
def issue () :
    line_in_csv_of_issue_clicked = 0
    row_count = 0
    tags = ""
    desc = ""
    notes = ""

    issue_name = request.cookies.get("issue")
    person = request.cookies.get("person").split("'")[1]
    issue_status = request.cookies.get("issue_status")

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
                notes = row[3]
                people = row[4]
                status = row[5]
            else :
                line_in_csv_of_issue_clicked = line_in_csv_of_issue_clicked + 1

    #If the user has enetered a person's name
    if person != "%noneValue%" :
        add_person("data.csv", line_in_csv_of_issue_clicked, person)
    else:
        pass


    if issue_status != "%noneValue%" :
        change_issue_status("data.csv", line_in_csv_of_issue_clicked, issue_status)

    if request.method == "POST": 
        # getting input
        note = request.form.get("note_name") 
        add_comment("data.csv", line_in_csv_of_issue_clicked, note)
        return render_template("issue.html", title=issue_name, desc=desc, tags=tags, notes=notes, people=people, status=status)


    return render_template("issue.html", title=issue_name, desc=desc, tags=tags, notes=notes, people=people, status=status)

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
       file.write(title + ", " + desc + ", " + tags + ", Notes:\n")
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
            try :
                delete_line("data.csv", line_to_deleted)
            except:
                return "Sorry, that issue does not exist!"
        return render_template("issue_deleted.html")
        
    return render_template("delete_issue.html")

#Runs the webserver and the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
import sys

from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('HomePage.html')


@app.route('/addPatientName', methods=['POST', 'GET'])


def addName():
    error = None
    if request.method == 'POST':
        #this method passes in the unique PID generated by the generatePID method
        result = add_name(request.form['FirstName'], request.form['LastName'], generatePID(request.form['FirstName'], request.form['LastName']))
        if result:
            #returns to the addPatientName page if there are valid results
            return render_template('addPatientName.html', error=error, result=result)
        else:
            error = 'invalid input name'
    #returns to the addPatientName Page if there are no results to update
    return render_template('addPatientName.html', error=error)

@app.route('/deletePatientName', methods=['POST', 'GET'])
def deleteName():
    error = None
    if request.method == 'POST':
        #method passes in the generatePID method so that all entries with unique PID can be deleted
        result = delete_name(request.form['FirstName'], request.form['LastName'], generatePID(request.form['FirstName'], request.form['LastName']))
        if result:
            #returns to the deletePatientName page if there are valid results
            return render_template('deletePatientName.html', error=error, result=result)
        else:
            error = 'invalid input name'
    #returns to the deletePatientName page if there are no results to update
    return render_template('deletePatientName.html', error=error)

@app.route("/selectPatientAction" , methods=['GET', 'POST'])
def selectPatientAction():
    #method uses the name attribute from the form to select a page to navigate to by concatinating the name with the HTML type
    error = None
    patientActionOption = request.form.get("pageMenu")
    return render_template(patientActionOption + '.html', error=error)



def add_name(first_name, last_name, P_ID):
    connection = sql.connect('database.db')
    #sets the PID as unique via the PRIMARY KEY keywords
    connection.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT, lastname TEXT, PID INTEGER PRIMARY KEY);')
    connection.execute('INSERT INTO users (firstname, lastname, PID) VALUES (?,?,?);', (first_name, last_name, P_ID))
    connection.commit()
    #removes duplicate tuples when getting values from table though the DISTINCT key word and groups all tuples with the same unique PID
    cursor = connection.execute('SELECT DISTINCT * FROM users GROUP BY PID;')
    return cursor.fetchall()

def delete_name(first_name, last_name, P_ID):
    connection = sql.connect('database.db')
    valueTodelete = generatePID(first_name, last_name)
    #deletes all tuples with the same unique PID by checking for the same hash generated by the generatePID method with the correspoding first_name and last_name
    connection.execute('DELETE FROM users WHERE PID like {};'.format(valueTodelete))
    connection.commit()
    cursor = connection.execute('SELECT DISTINCT * FROM users GROUP BY PID;')
    return cursor.fetchall()

#generates a unique PID by removing leading and trailing spaces and converting the result to all uppercase
# to ignore duplicate entries resulting from different case(eg:upper case or lower case)

#I was unsure as to what the instructions ment for a unique number for each entry
#since I did not know if it was for every new entry made into the system or every name combination
#I decided that each unique entry is a first and last name combination regardless of case
def generatePID(firstName, lastName):
    valueToHash = firstName.strip() + lastName.strip()
    #uses the built in hash method to generate a unique PID value which will be the same for any given first_name and last_name combination
    #uses abs to prevent negative PID values resulting from hash method
    return abs(hash(valueToHash.upper()))

if __name__ == "__main__":
    app.run()



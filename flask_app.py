from flask import Flask,render_template, request
import json
from difflib import get_close_matches
import sqlite3




data = json.load(open("data.json"))

app= Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
@app.route('/')
def home():


    return render_template("index.html")
@app.route ("/contact")

def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/result', methods=['POST'])

def result():
    word = request.form.get('query')
    mila, output = translate(word)

    if mila:
        return render_template("result.html", output=output)
    else:
        return render_template("retry.html", output=output)

@app.route('/feedback', methods=['POST'])
def feedback():
    firstname =  request.form.get('firstname')
    lastname =  request.form.get('lastname')
    country =  request.form.get('country')
    feedback =  request.form.get('subject')
    sqliteConnection = sqlite3.connect('FirstDatabase.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")
    create='''  CREATE TABLE IF NOT EXISTS FEEDBACK (
	firstname text NOT NULL,
	Lastname text NOT NULL,
	country text,
	feedback text
);
'''
    sqlite_select_Query = f'INSERT INTO FEEDBACK (firstname, Lastname, country ,feedback)  VALUES("{firstname}","{lastname}","{country}","{feedback}")'
    cursor.execute(create)
    cursor.execute(sqlite_select_Query)
    sqliteConnection.commit()
    cursor.close()
    return render_template("result.html", output="SUCCESSFUL")


def translate(w):
    w = w.lower()
    if w in data:
        return True, data[w]
    elif w.upper() in data:  # in case user enters words like USA or NATO
        return True, data[w.upper()]
    elif w.title() in data:
        return True,data[w.title()]
    elif len(get_close_matches(w, data.keys())) > 0:
        return False, get_close_matches(w, data.keys())[0]
    else:
        return False, "The word doesn't exist. Please double check it."




if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)

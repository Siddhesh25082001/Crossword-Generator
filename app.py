# ------------------------- This is the 'app.py'file - a .py file based on flask framework ---------------------- 

# 1. Setup for the Project

from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
from crossword_builder import *
import pdfkit
from savepdf import *
from flask import send_file

render_info = {}

def save_render_info(questions, answers, new_data, across_questions, down_questions, ac_qn, dn_qn, num_labels):
    global render_info

    render_info['questions'] = questions
    render_info['answers'] = answers
    render_info['new_data'] = new_data
    render_info['across_questions'] = across_questions
    render_info['down_questions'] = down_questions
    render_info['ac_qn'] = ac_qn
    render_info['dn_qn'] = dn_qn
    render_info['num_labels'] = num_labels

    return


app = Flask(__name__)
app.secret_key = "Siddhesh-Mane"

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pbl'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# ---------------------------------------------------------------------------------------------------------------------

# 2. Home Page for CRUD (C-Create, R-Read, U-Update, D-Delete)

@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('SELECT * FROM crossword')
    data = cur.fetchall()

    cur.close()
    return render_template('index.html', crossword = data)

@app.route('/add', methods=['POST'])
def add_crossword():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        cur.execute("INSERT INTO crossword (question, answer) VALUES (%s,%s)", (question, answer))
        conn.commit()
        flash('QnA Added successfully !!!')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_crossword(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('DELETE FROM crossword WHERE id = {0}'.format(id))
    conn.commit()
    flash('QnA Removed Successfully !!!')
    return redirect(url_for('Index'))

@app.route('/retrieve')
def retrive():
    # Retrieving the data from the database
    global mycw

    # Establishing a connection
    connection = pymysql.connect(host = "localhost", user ="root", passwd="",database="pbl") # Change the database name 
    cursor = connection.cursor()

    l = []
    questions = []
    answers = []
    across_questions = []
    down_questions = []
    ac_qn = []
    dn_qn = []
    points = []
    
    # Queries for retrieving all rows
    retrive = "Select * from crossword;"
    cursor.execute(retrive)
    rows = cursor.fetchall()

    for row in rows:
        l.append(list(row))

    for i in l:
        questions.append(i[1])
        answers.append(i[2])

    mycw = give_crossword(answers)
    # mycw.print_grid()
    # mycw.print_grid_info()
    new_data = [[chr(p) if p != 0 else p for p in s] for s in mycw.grid]

    num_labels = [[0 if p != 0 else p for p in s] for s in mycw.grid]

    for i in range(len(answers)):
        if mycw.grid_info[answers[i]]["type"] == 'a':
            across_questions.append(questions[i])
            ac_qn.append(i+1)
            num_labels[ mycw.grid_info[  answers[i] ]["cord"][0] ][ mycw.grid_info[  answers[i] ]["cord"][1] ] = i+1

        else:
            down_questions.append(questions[i])
            dn_qn.append(i+1)
            num_labels[ mycw.grid_info[  answers[i] ]["cord"][0] ][ mycw.grid_info[  answers[i] ]["cord"][1] ] = i+1

    # h = mycw.grid_info[answers[0]]["type"]
    # Commiting the connection and then closing itf
    connection.commit()
    connection.close()

    save_render_info( questions, answers, new_data, across_questions, down_questions, ac_qn, dn_qn, num_labels)

    entirehtml=render_template('toprint.html', questions=questions, answers=answers, new_data = new_data,
                           across_questions=across_questions, down_questions=down_questions, ac_qn=ac_qn, dn_qn=dn_qn, num_labels=num_labels)
    downpdf(entirehtml)

    return render_template('crossword.html', questions=questions, answers=answers, new_data = new_data,
                           across_questions=across_questions, down_questions=down_questions, ac_qn=ac_qn, dn_qn=dn_qn, num_labels=num_labels)

@app.route('/pdfdownload')
def give_print():
    return send_file('Crossword.pdf', attachment_filename='crossword.pdf')
    
    return render_template('crossword.html', questions= render_info['questions'], answers= render_info['answers'], new_data = render_info['new_data'],
                           across_questions= render_info['across_questions'], down_questions= render_info['down_questions'], ac_qn= render_info['ac_qn'], dn_qn= render_info['dn_qn'], num_labels= render_info['num_labels'])

# Running the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)







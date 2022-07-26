import os
import csv
from unicodedata import name
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from matplotlib.pyplot import table
from werkzeug.utils import secure_filename

import sqlite3 as sq
listoftables=[]


app = Flask(__name__)

conn = sq.connect('database.db',check_same_thread=False)
Cur = conn.cursor()

# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class MOSS(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Rno1 = db.Column(db.Integer, nullable=False)
#     Rno2 = db.Column(db.Integer, nullable=False)
#     Queslist = db.Column(db.String(100),nullable=False)

# db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/uploading', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        table = request.form['table']
        listoftables.append(table)
        f = request.files['file']
        f.save(secure_filename(f.filename))  # this will secure the file

        command1 = """CREATE TABLE IF NOT EXISTS '{}' (Sno VARCHAR(20),Rno1 DECIMAL(8,2),
            Rno2 DECIMAL(8,2), MossQ VARCHAR(20))"""
        Cur.execute(command1.format(table))

        with open(f.filename, 'r', newline="") as file:
            fn = csv.reader(file)
            next(fn)
            for row in fn:
                id = row[0]
                Rno1 = row[1]
                Rno2 = row[2]
                Queslist = row[3]

                # print(row)
                Cur.execute("""INSERT INTO '{}' VALUES('{}','{}','{}','{}')""".format(table,id,Rno1,Rno2,Queslist))
                conn.commit()
    conn.commit()
    return render_template("updated.html")

@app.route("/updatecol", methods=['GET', 'POST'])
def rendering():
    return render_template("update.html")

@app.route("/updatecollegedb", methods=['GET', 'POST'])
def updatecoldb():
    if request.method == 'POST':
        # table = request.form['table']
        f = request.files['file1']
        f.save(secure_filename(f.filename))  # this will secure the file
        # print(f.filename)

        command1 = """CREATE TABLE IF NOT EXISTS '{}' (Rno VARCHAR(20),Names VARCHAR(20))"""
        Cur.execute(command1.format("COLLEGEDB"))


        # Cur.execute(command1)

        with open(f.filename, 'r', newline="") as file:
            fn = csv.reader(file)
            next(fn)
            for row in fn:
                Rno = row[0]
                Name = row[1]
                Cur.execute("""INSERT INTO COLLEGEDB VALUES(?,?)""",(Rno,Name))
                conn.commit()
            conn.commit()
        D={}
        Cur.execute("SELECT * FROM COLLEGEDB")
        for row in Cur:
            D[int(row[0])]=row[1]
    # return "ok"
        print(D)
    return render_template("updated.html")

@app.route("/redirect",methods=["GET","POST"])
def redirecting():
    return render_template("index.html")

@app.route('/search',methods=['GET','POST'])
def display():
    Cur.execute("""SELECT name FROM sqlite_master 
    WHERE type='table';""")
    
    for row in Cur:
        for j in row:
            if j not in listoftables:
                if(j!='COLLEGEDB'):
                    listoftables.append(j)
    # print(listoftables)
    return render_template('search.html',listoftables=listoftables)

@app.route('/db',methods=['GET','POST'])
def showres():
    if request.method == "POST":
        choice=request.form['dropdown']
        rno1 = request.form['rno1']
        rno2 = request.form['rno2']
        # print(listoftables)
        Assignments=[]
        Resultlist=[]
        Names_dict={}
        Cur.execute("SELECT * FROM COLLEGEDB")
        for tup in Cur:
            Names_dict[int(tup[0])]=tup[1]
        # print(Names_dict)
        Cur.execute("SELECT * FROM A1")
        for row in Cur:
            print(row)
        for i in listoftables:
            if i != "ALL":
                Assignments.append(i)
        print(Assignments)
        print(rno1)
        print(rno2)
        if choice != "ALL":
            command1 = """SELECT * FROM '{}' """
            Cur.execute(command1.format(choice))
            # if int(rno2) == None: This doesnt work
            if rno2 == '':
                for j in Cur:
                    # print(j[1])
                    if j[1] == int(rno1) or j[2] == int(rno1):
                        # print("Got Mossed in Question",end=" ")
                        # print(j[3],end=" ")
                        # print("in",end=" ")
                        # print(choice)
                        # print(j)
                        Resultlist.append([choice,Names_dict[int(j[1])] ,j[1],Names_dict[int(j[2])],j[2],j[3]])
                        # Resultlist.append(-1)
                if len(Resultlist)==0:
                    Resultlist.append(-1)
            elif rno1 == '':
                for j in Cur:
                    # print(j[1])
                    if j[1] == int(rno2) or j[2] == int(rno2):
                        # print("Got Mossed in Question",end=" ")
                        # print(j[3],end=" ")
                        # print("in",end=" ")
                        # print(choice)
                        Resultlist.append([choice,Names_dict[int(j[1])] ,j[1],Names_dict[int(j[2])],j[2],j[3]])
                if len(Resultlist)==0:
                    Resultlist.append(-1)
            else:
                check=0
                for j in Cur:
                    # print(j[1])
                    if ((j[1] == int(rno1) or j[2] == int(rno1)) and (j[2] == int(rno2) or j[1] == int(rno2))):
                        # print("They both Got Mossed in Question",end=" ")
                        # print(j[3],end=" ")
                        # print("in",end=" ")
                        # print(choice)
                        Resultlist.append([choice,Names_dict[int(j[1])] ,j[1],Names_dict[int(j[2])],j[2],j[3]])
                        check=1
                if check == 0:
                    Resultlist.append(-1)
                    # print("The students entered weren't mossed with each other in this Assignment.")
        else:
            for i in Assignments:
                    command1 = """SELECT * FROM '{}' """
                    Cur.execute(command1.format(i))
                    if rno2 == '':
                        for j in Cur:
                            # print(j[1])
                            if j[1] == int(rno1) or j[2] == int(rno1):
                                # print("Got Mossed in Question",end=" ")
                                # print(j[3],end=" ")
                                # print("in",end=" ")
                                # print(i)
                                Resultlist.append([i,Names_dict[int(j[1])] ,j[1],Names_dict[int(j[2])],j[2],j[3]])
                    elif rno1 == '':
                        for j in Cur:
                            # print(j[1])
                            if j[1] == int(rno2) or j[2] == int(rno2):
                                # print("Got Mossed in Question",end=" ")
                                # print(j[3],end=" ")
                                # print("in",end=" ")
                                # print(i)
                                # print(j)
                                if(Resultlist[0]==-1):
                                        Resultlist.remove(-1)
                                Resultlist.append([i,Names_dict[int(j[1])] ,j[1],Names_dict[int(j[2])],j[2],j[3]])
                                # Resultlist.append(-1)
                    else:
                        check=0
                        for j in Cur:
                            # print(j[1])
                            if ((j[1] == int(rno1) or j[2] == int(rno1)) and (j[2] == int(rno2) or j[1] == int(rno2))):
                                # print("They both Got Mossed in Question",end=" ")
                                # print(j[3],end=" ")
                                # print("in",end=" ")
                                # print(i)
                                Resultlist.append([i,Names_dict[int(j[1])] ,j[1],Names_dict[int(j[2])],j[2],j[3]])
                                check=1
                            # print("The students entered weren't mossed with each other in this Assignment.")
        # print(Resultlist)
        if(Resultlist[0]==-1 or len(Resultlist)==0):
            return render_template("error.html")
        else:
            return render_template("jinjatable.html",res=Resultlist)

@app.route('/removefgs',methods=['GET','POST'])
def rem():
    Cur.execute("""SELECT name FROM sqlite_master 
    WHERE type='table';""")
    
    for row in Cur:
        for j in row:
            if j not in listoftables:
                if(j!='COLLEGEDB'):
                    listoftables.append(j)
    return render_template("removefgs.html",listoftables=listoftables)

@app.route('/dbedit',methods=['GET','POST'])
def edit():
    choice = request.form['dropdown']
    rno1 = request.form['rno1']
    rno2 = request.form['rno2']
    ques_string = request.form['ques']
    # print({rno1,rno2,ques_string})
    Cur.execute("""SELECT * FROM '{}' WHERE (Rno1='{}' AND Rno2='{}') or (Rno1='{}' AND Rno2='{}');""".format(choice,rno1,rno2,rno2,rno1))
    err=0
    Sno=0
    newst=""
    for row in Cur:
        print(row)
        Sno = row[0]
        orig = row[3].split(',')
        final = ques_string.split(',')
        print(orig,final)
        flag=0
        for i in orig:
            flag=0
            for j in final:
                if(j==i):
                    flag=1
                    break
                if j not in orig:
                    err=2
                    break
            if flag==0:
                newst = newst+i+","
        print(newst[:len(newst)-1:])
    if err==2:
        return render_template("error.html")
    Cur.execute("""DELETE FROM '{}' WHERE (Rno1='{}' AND Rno2='{}') or (Rno1='{}' AND Rno2='{}');""".format(choice,rno1,rno2,rno2,rno1))
    if(len(newst[:len(newst)-1:])>=1):
        Cur.execute("""INSERT INTO '{}' VALUES('{}','{}','{}','{}')""".format(choice,Sno,rno1,rno2,newst[:len(newst)-1:]))
    return render_template("updated.html")

if __name__ == '__main__':
    app.run(debug=True)

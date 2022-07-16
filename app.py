import os
import csv
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MOSS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Rno1 = db.Column(db.Integer, nullable=False)
    Rno2 = db.Column(db.Integer, nullable=False)
    Queslist = db.Column(db.String(100),nullable=False)

db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

# no use of enctype

@app.route('/uploading', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename)) # this will secure the file
        print(f.filename)
        with open(f.filename,'r',newline="") as file:
            fn = csv.reader(file)
            print(next(fn))
            for row in fn:
                id = int(row[0])
                Rno1 = int(row[1])
                Rno2 = int(row[2])
                Queslist = row[3]
                entry = MOSS(id=id,Rno1=Rno1 , Rno2=Rno2,Queslist=Queslist)
                db.session.add(entry)
        db.session.commit()
        return "ok"

if __name__ == '__main__':
    app.run(debug=True)

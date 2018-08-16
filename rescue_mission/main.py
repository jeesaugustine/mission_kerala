from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

# conn.execute('CREATE TABLE rescue_kerala (emergency TEXT, district TEXT,name TEXT, addr TEXT, \
               # pin TEXT, phone TEXT, alt_phone TEXT, no_people SMALLINT, \
               # no_kids SMALLINT, no_elderly SMALLINT, sick SMALLINT, preg SMALLINT, \
               # special TEXT, approx_time TEXT, stats TEXT)')

# print("Table created successfully")
conn.close()

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         emergency_ = request.form['emer']
         district_ = request.form['dist']
         name_ = request.form['nme']
         address_ = request.form['add']
         phone_ = request.form['phone_']
         alt_phone_ = request.form['alt_phone_']
         pin = request.form['pin']
         kids_ = request.form['kids']
         total_ = request.form['total_']
         elderly_ = request.form['elderly_']
         pregnent_ = request.form['pregnent_']
         sick_ = request.form['sick_']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO rescue_kerala \
                        (emergency, district,name, addr,pin, phone, alt_phone\
                        no_people, no_kids, no_elderly, sick, preg, \
                        ) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
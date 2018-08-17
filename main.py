from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

#-- conn.execute('CREATE TABLE rescue_kerala_1 (emergency TEXT, district TEXT,name TEXT, addr TEXT, \
#--               pin TEXT, phone TEXT, alt_phone TEXT, no_people TEXT, \
#--               no_kids TEXT, no_elderly TEXT, sick TEXT, preg TEXT, \
#--               special TEXT, approx_time TEXT, stats TEXT)')

print("Table created successfully")
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
      print('jees')
      try:

         emergency_ = request.form['emer']
         district_ = request.form['dist']
         fname = request.form['fname']
         address_ = request.form['add']
 
         phone_ = request.form['phone_']

         alt_phone_ = request.form['alt_phone_']

         pin = request.form['pin']

         kids_ = 'Null'
         elderly_ = 'Null'
         pregnent_ = 'Null'
         sick_ = 'Null'
         
         total_ = request.form['total_']
         kids_ = request.form['kids']

         elderly_ = request.form['elderly_']
         
         if request.form['pregnent_']:
            pregnent_ = request.form['pregnent_']
         
         sick_ = request.form['sick_']
         
         msg = 'STart'
         print(emergency_, district_, fname, address_, phone_, alt_phone_, pin, kids_, total_, elderly_, pregnent_, sick_, msg)
         with sql.connect("database.db") as con:
            cur = con.cursor()
            print('Curser started ')
            cur.execute("INSERT INTO rescue_kerala_1 \
                        (emergency, district, name, addr, pin, phone, alt_phone\
                        no_people, no_kids, no_elderly, sick, preg, \
                        ) VALUES (?,?,?,?, ?,?,?,?, ?,?,?,?)",(emer,dist,nme,add, phone_, alt_phone_, pin, kids, kids, elderly_, elderly_, sick_) )
            print('successfully')
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
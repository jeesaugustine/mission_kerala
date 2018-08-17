from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)
import requests
from geopy.geocoders import Nominatim

# from location_2 import get_address, get_lat_long

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

# conn.execute('CREATE TABLE rescue_kerala_1 (emergency TEXT, district TEXT,name TEXT, addr TEXT, pin TEXT, phone TEXT, alt_phone TEXT, no_people TEXT, no_kids TEXT, no_elderly TEXT, sick TEXT, preg TEXT, special TEXT, approx_time TEXT, stats TEXT)')
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
      print('jees')
      try:
         emergency_ = request.form['emer']   
         district_ = request.form['dist']
         namer = request.form['fname_']
         # print(namer)
         address_ = request.form['add']
         pin = request.form['pin']
         phone_ = request.form['phone_']
         alt_phone_ = request.form['alt_phone_']
         total_ = request.form['total_']
         kids_ = request.form['kids']
         elderly_ = request.form['elderly_']
         sick_ = request.form['sick_']
         pregnent_ = request.form['pregnent_']
         token = phone_
         msg = 'Start'
         print(emergency_, district_, address_, namer, phone_, alt_phone_, pin, total_, kids_, elderly_, pregnent_, sick_, msg)
         special = 'Jees'
         with sql.connect("database.db") as con:
            cur = con.cursor()
            print('Curser started ')
            cur.execute("INSERT INTO rescue_kerala_1 (emergency, district ,name , addr, pin ,phone ,alt_phone ,no_people ,no_kids ,no_elderly ,sick ,preg ,special) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (emergency_, district_,namer,address_, pin, phone_, alt_phone_, total_, kids_, elderly_, sick_, pregnent_, special))
            print('successfully')
            con.commit()
            msg = "ടോക്കൺ നമ്പർ(ഫോൺ നമ്പർ)-  " + token + " നിങ്ങൾക്ക് ലഭിച്ചിരിക്കുന്ന ടോക്കൺ നമ്പർ ദയവായി സൂക്ഷിക്കുക. ഈ നമ്പർ ഉപയോഗിച്ച് നിങ്ങൾക്ക് റെസ്ക്യൂ സംഘത്തെ ട്രാക്ക് ചെയ്യാവുന്നതാണ്. നിങ്ങൾ സുരക്ഷിത സ്ഥാനത്തെത്തിയാൽ ദയവായി ഈ ടോക്കൺ നമ്പർ ഉപയോഗിച്ച് രക്ഷപെട്ടു എന്ന്  രേഖപ്പെടുത്തുക.<br /> Rescue Team has your recored wait patiently. We are servicing your request."
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/status', methods = ['POST', 'GET'])
def status():
   return render_template('status.html')

@app.route('/status_1', methods = ['POST', 'GET'])
def status_1():
   if request.method == 'POST':
      try:
         msg = 'nice'
         phone_ = request.form['phone_']
         print(phone_)
         con = sql.connect("database.db")
         con.row_factory = sql.Row
         cur = con.cursor()
         query = "select name, district from rescue_kerala_1 where phone=" + str(phone_)
         print(query)
         cur.execute(query)
         rows = cur.fetchall();

         d = {'alp': 'ആലപ്പുഴ(Alappuzha)', 'ekm': 'എറണാകുളം(Ernakulam)', 'idk':'ഇടുക്കി(Idukki)', 'knr':'കണ്ണൂർ(Kannur)', 'kol':'കാസർഗോഡ്(Kasaragod)', 'klm':'കൊല്ലം(Kollam)','ktm':'കോട്ടയം(Kottayam)','koz':'കോഴിക്കോട്(Kozhikode)','mpm':'മലപ്പുറം(Malappuram)', 'pkd':'പാലക്കാട്(Palakkad)', 'ptm':'പത്തനംതിട്ട(Pathanamthitta)', 'tvm':'തിരുവനന്തപുരം(Thiruvananthapuram)', 'tcr':'തൃശ്ശൂർ(Thrissur)', 'wnd':'വയനാട്(Wayanad)'}
         dist = str(rows[0][1])
         d = d[dist]
         mesage = 'പേര് - name ' + str(rows[0][0]) + ' സ്ഥലം - district ' + d
         print(mesage)
         return render_template("list_first.html",rows = mesage)

      except:
         con.rollback()
         msg = "error in select operation"
      finally:
         return render_template("list_first.html",msg = mesage)
         con.close()

@app.route('/status_2', methods = ['POST', 'GET'])
def status_2():
   if request.method == 'POST':
      stat = request.form['status__']
      if stat == 'no':
         return render_template("list_no.html", msg = 'നിങ്ങളുടെ വിവരങ്ങൾ റെസ്ക്യൂ ടീമിന് കൈമാറിയിരിക്കുന്നു. റെസ്ക്യൂ ടീം നിങ്ങളുടെ അടുക്കലേക്കു വന്നു കൊണ്ടിരിക്കുന്നു. Your details have been forwarded to the rescue team. They are on the way.')
      else:
         return render_template("list_yes.html", msg = 'ആവശ്യപ്പെട്ട സേവനം ലഭിച്ചിരിക്കുന്നു. Requested service accomplished.')

@app.route('/rescue', methods = ['POST', 'GET'])
def rescue():
   return render_template('rescue.html')
   # college of engineering adoor, manakkala PO. adoor, Pathanamthitta

@app.route('/rescue_1', methods = ['POST', 'GET'])
def rescue_1():
   print('Hi')
   if request.method == 'POST':
      print('Hi')
      addr = request.form['add']
      print(addr)
      print(get_lat_long(addr, ''))
   return render_template('rescue.html')

def get_lat_long(Address_1, Address_2):
   Address_1 = Address_1.replace(" ","+")
   Address_2 = Address_2.replace(" ","+")
   search_address = Address_1+","+Address_2
   api_link = "https://maps.googleapis.com/maps/api/geocode/json?address="+search_address
   response = requests.get(api_link)
   resp_json_payload = response.json()
   return(resp_json_payload['results'][0]['geometry']['location'])

@app.route('/list', methods = ['POST', 'GET'])
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from rescue_kerala_1")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
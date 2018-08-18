from flask import Flask, render_template, request, send_file
import sqlite3 as sql
from flask import send_from_directory, current_app as app

app = Flask(__name__)
# <!-- Developed by Jees Augustine, Balan Ramesh, Jiss Sebastian and Sandeep Eldo -->
import requests
from geopy.geocoders import Nominatim

# from location_2 import get_address, get_lat_long

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

# conn.execute('CREATE TABLE rescue_kerala_1 (emergency TEXT, district TEXT,name TEXT, addr TEXT, pin TEXT, phone TEXT, alt_phone TEXT, no_people TEXT, no_kids TEXT, no_elderly TEXT, sick TEXT, preg TEXT, special TEXT, approx_time TEXT, stats TEXT, lat TEXT, lon TEXT)')
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
         print(district_)
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

         d = {'alp': 'ആലപ്പുഴ(Alappuzha)', 'ekm': 'എറണാകുളം(Ernakulam)', 'idk':'ഇടുക്കി(Idukki)', 'knr':'കണ്ണൂർ(Kannur)', 'kol':'കാസർഗോഡ്(Kasaragod)', 'klm':'കൊല്ലം(Kollam)','ktm':'കോട്ടയം(Kottayam)','koz':'കോഴിക്കോട്(Kozhikode)','mpm':'മലപ്പുറം(Malappuram)', 'pkd':'പാലക്കാട്(Palakkad)', 'ptm':'പത്തനംതിട്ട(Pathanamthitta)', 'tvm':'തിരുവനന്തപുരം(Thiruvananthapuram)', 'tcr':'തൃശ്ശൂർ(Thrissur)', 'wnd':'വയനാട്(Wayanad)'}
         place_holder = d[district_].split('(')[1].split(')')[0].strip()
         try:
            lat_long = get_lat_long(address_, '')
         except:
            lat_long = get_lat_long(place_holder, '')
         
         # print(lat_long)
         lat = lat_long['lat']
         lon = lat_long['lng']
         msg = 'Start'

         # print(lat, lon)
         print(emergency_, district_, address_, namer, phone_, alt_phone_, pin, total_, kids_, elderly_, pregnent_, sick_, msg)
         special = 'Jees'
         with sql.connect("database.db") as con:
            cur = con.cursor()
            print('Curser started ')
            cur.execute("INSERT INTO rescue_kerala_1 (emergency, district ,name , addr, pin ,phone ,alt_phone ,no_people ,no_kids ,no_elderly ,sick ,preg ,special, lat, lon, stats) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (emergency_, district_,namer,address_, pin, phone_, alt_phone_, total_, kids_, elderly_, sick_, pregnent_, special, lat, lon, 'n'))
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
         # session['phone'] = phone_
         con = sql.connect("database.db")
         con.row_factory = sql.Row
         cur = con.cursor()
         query = "select name, district from rescue_kerala_1 where phone=" + str(phone_) + " and stats=\'n\'"
         print(query)
         cur.execute(query)
         rows = cur.fetchall();
         print(rows)
         if rows:
            d = {'alp': 'ആലപ്പുഴ(Alappuzha)', 'ekm': 'എറണാകുളം(Ernakulam)', 'idk':'ഇടുക്കി(Idukki)', 'knr':'കണ്ണൂർ(Kannur)', 'kol':'കാസർഗോഡ്(Kasaragod)', 'klm':'കൊല്ലം(Kollam)','ktm':'കോട്ടയം(Kottayam)','koz':'കോഴിക്കോട്(Kozhikode)','mpm':'മലപ്പുറം(Malappuram)', 'pkd':'പാലക്കാട്(Palakkad)', 'ptm':'പത്തനംതിട്ട(Pathanamthitta)', 'tvm':'തിരുവനന്തപുരം(Thiruvananthapuram)', 'tcr':'തൃശ്ശൂർ(Thrissur)', 'wnd':'വയനാട്(Wayanad)'}
            dist = str(rows[0][1])
            d = d[dist]
            mesage = 'പേര് - name ' + str(rows[0][0]) + ' സ്ഥലം - district ' + d
            print(mesage)
            return render_template("list_first.html",rows = mesage)
         else:
            return render_template("list_no.html",rows = 'നിങ്ങൾ ആവശ്യപ്പെട്ട ആളെ രെക്ഷപെടുത്തിയതായി രേഖപ്പെടുത്തിയിരിക്കുന്നു. ഇനിയും ഇവർക്ക് സാധ്യം ലഭിച്ചില്ല എന്ന് നിങ്ങള്ക്ക് സംശയം ഉണ്ടെങ്കിൽ, ദയവായി നിങ്ങൾ ഉപയോഗിച്ച ഫോൺ നമ്പർ പരിശോധിക്കുക അല്ലെങ്കിൽ ഇദ്ദേഹത്തെ നിങ്ങൾ ഫോൺ ഉപയോഗിച്ചു ബന്ധപ്പെടാൻ ശ്രേമിക്കുക. ഞങ്ങളുടെ റെക്കോർഡ് പ്രകാരം ഇദ്ദേഹത്തെ രക്ഷപ്പെടുത്തിയിരിക്കുന്നു- The person you are trying to search, according to our records has been saved already. Please try to check the phone number once again or try contacting the phone number. Our records marked her/him as rescued. Thanks')
      except:
         con.rollback()
         msg = "error in select operation"
      finally:
         if rows:
            return render_template("list_first.html",msg = mesage)
            con.close()
         else:
            return render_template("list_no.html",msg = 'നിങ്ങൾ ആവശ്യപ്പെട്ട ആളെ രെക്ഷപെടുത്തിയതായി രേഖപ്പെടുത്തിയിരിക്കുന്നു. ഇനിയും ഇവർക്ക് സാധ്യം ലഭിച്ചില്ല എന്ന് നിങ്ങള്ക്ക് സംശയം ഉണ്ടെങ്കിൽ, ദയവായി നിങ്ങൾ ഉപയോഗിച്ച ഫോൺ നമ്പർ പരിശോധിക്കുക അല്ലെങ്കിൽ ഇദ്ദേഹത്തെ നിങ്ങൾ ഫോൺ ഉപയോഗിച്ചു ബന്ധപ്പെടാൻ ശ്രേമിക്കുക. ഞങ്ങളുടെ റെക്കോർഡ് പ്രകാരം ഇദ്ദേഹത്തെ രക്ഷപ്പെടുത്തിയിരിക്കുന്നു - The person you are trying to search, according to our records has been saved already. Please try to check the phone number once again or try contacting the phone number. Our records marked her/him as rescued. Thanks')

@app.route('/status_2', methods = ['POST', 'GET'])
def status_2():
   if request.method == 'POST':
      # phone_ = session.get('phone', None)
      # print(phone_)
      # p = request.form['firstbox']
      # print(p)
      stat = request.form['status__']
      if stat == 'no':
         return render_template("list_no.html", msg = 'നിങ്ങളുടെ വിവരങ്ങൾ റെസ്ക്യൂ ടീമിന് കൈമാറിയിരിക്കുന്നു. റെസ്ക്യൂ ടീം നിങ്ങളുടെ അടുക്കലേക്കു വന്നു കൊണ്ടിരിക്കുന്നു. Your details have been forwarded to the rescue team. They are on the way.')
      else:
         return render_template("list_yes.html", msg = 'ആവശ്യപ്പെട്ട സേവനം ലഭിച്ചിരിക്കുന്നു. Requested service accomplished.')

@app.route('/yes_2', methods = ['POST', 'GET'])
def yes_2():
   if request.method == 'POST':
      phone_ = request.form['phone_']
      con = sql.connect("database.db")
      con.row_factory = sql.Row
      query = "UPDATE rescue_kerala_1 SET stats=\'r\' WHERE phone=" + str(phone_)
      print(query)
      cur = con.cursor()
      cur.execute(query)
      rows = cur.fetchall();
      con.commit()
      return render_template("list_no.html",msg = 'Your request is updated')

@app.route('/emergency_ph', methods = ['POST', 'GET'])
def emergency_ph():
   print('Jees is here')
   return render_template('emergency.html')
   # with open('/static/FloodRedAlertSaveLife.pdf', 'rb') as static_file:
   #    return send_file(static_file, attachment_filename='FloodRedAlertSaveLife.pdf')
   # return render_template('social.html')

@app.route('/social', methods = ['POST', 'GET'])
def social():
   return render_template('social.html')

@app.route('/about', methods = ['POST', 'GET'])
def about():
   return render_template('about.html')

@app.route('/rescue', methods = ['POST', 'GET'])
def rescue():
   return render_template('rescue.html')
   # college of engineering adoor, manakkala PO. adoor, Pathanamthitta

@app.route('/hidden', methods = ['POST', 'GET'])
def hidden():
      if request.method == 'POST':
         try:
            con = sql.connect("database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            query = "select name, district from rescue_kerala_1"
            print(query)
            cur.execute(query)
            rows = cur.fetchall()
            print(rows)

            if rows:
               return render_template("list.html",rows = rows)
            else:
               return render_template("list_no.html",msg = 'നിങ്ങൾ ആവശ്യപ്പെട്ട ആളെ രെക്ഷപെടുത്തിയതായി രേഖപ്പെടുത്തിയിരിക്കുന്നു. ഇനിയും ഇവർക്ക് സാധ്യം ലഭിച്ചില്ല എന്ന് നിങ്ങള്ക്ക് സംശയം ഉണ്ടെങ്കിൽ, ദയവായി നിങ്ങൾ ഉപയോഗിച്ച ഫോൺ നമ്പർ പരിശോധിക്കുക അല്ലെങ്കിൽ ഇദ്ദേഹത്തെ നിങ്ങൾ ഫോൺ ഉപയോഗിച്ചു ബന്ധപ്പെടാൻ ശ്രേമിക്കുക. ഞങ്ങളുടെ റെക്കോർഡ് പ്രകാരം ഇദ്ദേഹത്തെ രക്ഷപ്പെടുത്തിയിരിക്കുന്നു- The person you are trying to search, according to our records has been saved already. Please try to check the phone number once again or try contacting the phone number. Our records marked her/him as rescued. Thanks')
         except:
            con.rollback()
            msg = "error in select operation"
         finally:
            if rows:
               return render_template("list.html",rows = rows)
               con.close()
            else:
               return render_template("list_no.html",msg = 'നിങ്ങൾ ആവശ്യപ്പെട്ട ആളെ രെക്ഷപെടുത്തിയതായി രേഖപ്പെടുത്തിയിരിക്കുന്നു. ഇനിയും ഇവർക്ക് സാധ്യം ലഭിച്ചില്ല എന്ന് നിങ്ങള്ക്ക് സംശയം ഉണ്ടെങ്കിൽ, ദയവായി നിങ്ങൾ ഉപയോഗിച്ച ഫോൺ നമ്പർ പരിശോധിക്കുക അല്ലെങ്കിൽ ഇദ്ദേഹത്തെ നിങ്ങൾ ഫോൺ ഉപയോഗിച്ചു ബന്ധപ്പെടാൻ ശ്രേമിക്കുക. ഞങ്ങളുടെ റെക്കോർഡ് പ്രകാരം ഇദ്ദേഹത്തെ രക്ഷപ്പെടുത്തിയിരിക്കുന്നു - The person you are trying to search, according to our records has been saved already. Please try to check the phone number once again or try contacting the phone number. Our records marked her/him as rescued. Thanks')

@app.route('/rescue_1', methods = ['POST', 'GET'])
def rescue_1():
   print('Hi')
   if request.method == 'POST':
      print('Hi')
      addr = request.form['add']
      print(addr)
      lat_long = get_lat_long(addr, '')
      radi = request.form['radius']
      lat = 0.009
      if str(radi) == 'one':
         new_rad_1 = lat_long['lat'] + lat
         new_rad_2 = lat_long['lat'] - lat
      elif str(radi) == 'two':
         new_rad_1 = lat_long['lat'] + 2*lat
         new_rad_2 = lat_long['lat'] - 2*lat
      elif str(radi) == 'three':
         new_rad_1 = lat_long['lat'] + 3*lat
         new_rad_2 = lat_long['lat'] - 3*lat
      elif str(radi) == 'five':
         new_rad_1 = lat_long['lat'] + 5*lat
         new_rad_2 = lat_long['lat'] - 3*lat


      lon = 0.011
      if str(radi) == 'one':
         new_lon_1 = lat_long['lng'] + lon
         new_lon_2 = lat_long['lng'] - lon
      elif str(radi) == 'two':
         new_lon_1 = lat_long['lng'] + 2*lon
         new_lon_2 = lat_long['lng'] - 2*lon
      elif str(radi) == 'three':
         new_lon_1 = lat_long['lng'] + 3*lon
         new_lon_2 = lat_long['lng'] - 3*lon
      elif str(radi) == 'five':
         new_lon_1 = lat_long['lng'] + 5*lon
         new_lon_2 = lat_long['lng'] - 5*lon


      con = sql.connect("database.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      query = "select name, addr, no_people, phone  from rescue_kerala_1 where lat>=" + str(new_rad_2) + ' and lat<=' + str(new_rad_1) + ' and lon>=' + str(new_lon_2) + ' and lon<=' + str(new_lon_1) + " and stats=\'n\'" +' order by no_people'
      print(query)
      cur.execute(query)
      rows = cur.fetchall();
      if rows:
         return render_template("list.html",rows = rows)
      else:
         return render_template("list_no.html",msg = "ഈ ചുറ്റളവിൽ രക്ഷാഡൗത്യം അന്വേഷിക്കുന്ന ആരും തന്നെ ഇല്ല. ദയവായി കൂടുതൽ സെർച്ച് ദൂരത്തേക്ക് വ്യാപിപ്പിക്കുക.അല്ലെങ്കിൽ നിങ്ങൾ എല്ലാവര്‌യും രക്ഷിച്ചിരിക്കുന്നു. -No request found in this range, please expand your search radius. Or you have saved everyone in this range")

      # return render_template('rescue.html')

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

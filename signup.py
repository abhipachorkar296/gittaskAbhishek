#!/usr/bin/env python
#!/usr/bin/env python
from flask import Flask, render_template,request,json,session
import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='soumick',
                             password='ufEn5x4puY0xrDy4',
                             db='bookmyshow',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

@app.route('/search-movie', methods=['GET','POST'])
#def showdisp():
@app.route('/', methods=['GET','POST'])
def display():
    return render_template('loginpage.html')

@app.route('/login', methods=['GET', 'POST'])
def logincheck():
    msg= ''
    if request.method=='POST':
        username = request.form['email']
        password = request.form['psw']
        category = request.form['category']
        try:
            with connection.cursor() as cursor:
                if category=='customer':
                    print("customer category")
                    cursor.execute('SELECT * FROM customer_info WHERE email_id= %s AND password = %s',(username,password))
                    print("here")
                    account = cursor.fetchone()
                    print(account)
                    if account:
                        print("success")
                        session['loggedin'] = True
                        session['id']=account['id']
                        session['email'] = account['email_id']

                        # print("success")
                    else:
                        print("Incorrect username/password")
                        msg = 'Incorrect username/password'
                elif category=='theater_owner':
                    print("theater category")
                    cursor.execute('SELECT * FROM theater_owner WHERE email_id= %s AND password = %s',(username,password))
                    account = cursor.fetchone()
                    if account:
                        msg="success!"
                        print("success")
                        session['email'] = account['email_id']
                    else:
                        print("incorrect")
                        msg = 'Incorrect username/password'
                else:
                    print('admin')
        except:
            print('error login')
    return render_template('loginpage.html',msg=msg)


@app.route('/save-post',methods=['POST', 'GET'])
def signUp():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['psw']
        category=request.form['category']
        print(name)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                if category=='customer':
                    sql = "INSERT INTO customer_info(name,password,email_id) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (name,password,email))
                    connection.commit()
                elif category=='theatre_owner':
                    sql = "INSERT INTO theatre_owner_info(name,password,email_id) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (name,password,email))
                    connection.commit()
                else:
                    print('admin')
        finally:
            connection.close()
            return "Saved successfully."
    return render_template('signupform.html')   
    """redirect"""

if __name__ == "__main__":
    app.run(debug = True)
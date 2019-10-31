from flask import Flask, render_template,request,json , redirect , url_for
import pymysql.cursors
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
from flask_table import Table, Col

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='Bookmyshow',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)
# app.config['MAIL_SERVER'] = ''
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'pranitpawar296@gmail.com'
# app.config['MAIL_PASSWORD'] = 'pranitbail'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# class Results(show_list):
#     id = Col('id' , show = Flase)
#     theater_name = Col('theater_name' )
#     image = Col('image')
#     movie_name = Col('movie_name')
#     category = Col('movie_name')
#     1st_show = Col('9:00am')
#     2st_show = Col('12:00pm')
#     3st_show = Col('3:00pm')
#     4st_show = Col('6:00pm')

@app.route('/',methods=['POST', 'GET'])
def loginup():
    return render_template('login.html')

# @app.route('/' ,methods=['POST','GET'])
# def home():
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM ...")
#             data = cursor.fetchall() 
#     return render_template("home.html" , data = data)


@app.route('/login',methods=['POST', 'GET'])
def login():
    print("Reachedeee")
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        category = request.form['category']
        # print
        try:
            with connection.cursor() as cursor:
                if category == 'customer':
                    cursor.execute('SELECT * FROM customer_info WHERE email_id = %s AND password = %s', (email, password))
                    account = cursor.fetchone()

                    if account:
                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['email'] = account['email_id']
                        msg = 'Logged successful'
                        return redirect(url_for(customer))
                    else:
                        msg = 'Incorrect username/password'
            
                elif category == 'theater_owner':
                    print("Inside")
                    cursor.execute('SELECT * FROM Theater_owners_info WHERE email_id = %s AND password = %s', (email, password))
                    account = cursor.fetchone()

                    if account:
                        print("Fetched")
                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['email'] = account['email_id']
                        msg = 'logged successful'
                        return redirect(url_for(theater))
                    else:
                        msg = 'Incorrect username/password'
                else:
                    print('Admin') 
        except:
            print('error login')
    return render_template('login.html',msg = msg)


@app.route('/signUp',methods=['POST', 'GET'])
def signUp():
    print("ff")
    if request.method=='POST':
        name = request.form['name']
        print(name)
        print(request.form)
        email=request.form['email']
        password=request.form['password']
        category = request.form['category']
        try:
            with connection.cursor() as cursor:
                if category == 'customer':
            
                    print(email,password)
                  # Read a single record
                    sql = "INSERT INTO  customer_info (name,email_id,password) VALUES (%s,%s, %s)"
                   
                    cursor.execute(sql, (name, email,password))
                    connection.commit()
                elif category == 'theater_owner':
                    print(email,password)
                  # Read a single record
                    sql = "INSERT INTO  Theater_owners_info (name,email_id,password) VALUES (%s,%s, %s)"
                   
                    cursor.execute(sql, (name,email,password))
                    connection.commit()
                else:
                    print('admin')
                print("RR")
        except Exception as e:
            print(e)
            # connection.close()
            return "saved successfully."
        return render_template('login.html')
    return render_template('signupform.html')
       
@app.route('/theater_specification', methods=['POST' , 'GET'])
def theater():
    if request.method=='POST':
        image = request.form['#image']
        address = request.form['Address']
        specifications = request.form['specifications']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO  theater_speecifications ('''image''' , address , specifications) VALUES(%s,%s,%s)"
                cursor.execute(sql , ('''image''' , address , specifications))
                connection.commit()
        finally:
            connection.close()
            return "saved successfully"
    return render__template('theater_specifications.html')

@app.route('/search-movie' , methods = ['POST' , 'GET'])
def customer():
    if request.method=='POST':
        movie = request.form['movie']
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM show_list WHERE movie_name = %s ', (movie_name))
                account  = cursor.fetchall()

                if account:
                    return render__template('customerpageresults.html' , session = account)
                else:
                        msg = 'ERROR'
        finally:
            connection.close()
    # return render__template()




# cursor.execute('SELECT * FROM theater_owner_info WHERE email_id = %s AND password = %s', (email, password))
#                     account = cursor.fetchone()

# @app.route('/search-movie', methods = ['POST' , 'GET'] )
# def send_mail():
#     message = Mail(
#         from_email='pranitpawar@gmail.com'
#         to_email='email_id'
#         subject=subject
#         html_content=content)
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(message)
#         #to be continued...


if __name__ == "__main__":
    app.run(debug=True)


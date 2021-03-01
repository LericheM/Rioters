from flask import Flask, request, render_template, redirect, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import os 
import logging 
import messaging 

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

logging.basicConfig(level=logging.INFO)

# tag::login_required[]
def login_required(f):
    """
    Decorator that returns a redirect if session['email'] is not set 
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session: 
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
#end::login)required[]

@app.route('/')
def index():
    return render_template("index.html")
#database={'Will' : '123', 'Omar' : 'abc', 'Matt' : 'xyz', 'Hashim' : '456'}

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

#tag::register[]
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        msg = messaging.Messaging()
        msg.send(
            'REGISTER',
            {
                'email': email,
                'hash' : generate_password_hash(password)
            }
        )
        response = msg.receive()
        if response['success']:
            session['email'] = email
            return redirect ('/')
        else:
            return f"{response['message']}"
    return render_template('register.html')
#end::register[]

# tag::login[] 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        msg = messaging.Messaging()
        msg.send('GETHASH', { 'email': email })
        response = msg.receive()
        if response['success'] != True:
            return "Login failed."
        if check_password_hash(response['hash'], password):
            session['email'] = email
            return redirect('/')
        else:
            return "Login failed."
    return render_template('login.html')
# end::login[] 

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

    #UN = request.form['Username']
    #PW = request.form['Password']
    #if name1 not in database:
     #   return render_template('login.html', info='Invalid User')
    #else:
     #   if database[name1]!=PW:
      #      return render_template('login.html', info='Invalid Password')
       # else: 
        #    return render_template('home.html', name =name1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
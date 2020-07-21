from flask import Flask,render_template, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key="shilpa"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route('/sucs',methods = ["POST"])  
def sucs():  
    if request.method == "POST":  
        session['uname']=request.form['uname']  
    return render_template('sucs.html')  

@app.route('/logout')  
def logout():  
    if 'uname' in session:  
        session.pop('uname',None)  
        return render_template('logout.html');  
    else:  
         return '<p>user already logged out</p>'  
 

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/profile')
def profile():
    if 'uname' in session:
        uname = session['uname']
        return render_template('profile.html',name=uname)
    else:
        return '<p>Please login first</p>' 
    

@app.route('/sucs')  
def upload():  
    return render_template("sucs.html")

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(secure_filename(f.filename))  
        return render_template("success.html", name = f.filename)    

                             
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
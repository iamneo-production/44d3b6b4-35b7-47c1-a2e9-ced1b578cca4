from flask import Flask,render_template,flash,request,redirect,url_for,session
import sqlite3
app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("CREATE TABLE IF NOT EXISTS data(pid INTEGER PRIMARY KEY, name TEXT,age INTEGER,gender TEXT,phone INTEGER,mail Varchar,password Varchar, place TEXT)")
con.close()

@app.route('/')
def home():  # put application's code here
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/adddata',methods=["POST","GET"])
def adddata():
    if request.method=="POST":
        try:
            name=request.form['name']
            age=request.form['age']
            phone=request.form['phone']
            mail=request.form['mail']
            place=request.form['place']
            password=request.form['password']
            gender=request.form['gender']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("INSERT INTO data(name,age,gender,phone,mail,password,place)values(?,?,?,?,?,?,?)",(name,age,gender,phone,mail,password,place))
            con.commit()
            flash("Register Successful","success")
        except:
            flash("Error in Registration","danger")
        finally:
            return redirect(url_for("home"))
            con.close()

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        mail=request.form['mail']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("Select * from data where mail=? and password=?",(mail,password))
        data=cur.fetchone()

        if data:
            session["mail"]=data["mail"]
            session["password"]=data["password"]
            return render_template("home.html")
        else:
            flash("Mail and Password Mismatch","danger")
            return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)

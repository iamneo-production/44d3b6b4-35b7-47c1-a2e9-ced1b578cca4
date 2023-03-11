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

@app.route('/homepage')
def homepage():
    return render_template("home.html")

@app.route('/profile')
def profile():
    name=session["mail"]
    age=session["age"]
    gender=session["gender"]
    mail=session["mail"]
    password=session["password"]
    place=session["place"]
    phone=session["phone"]
    return render_template("profile.html",name=name,age=age,gender=gender,mail=mail,password=password,place=place,phone=phone)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/manage')
def manage():
    return render_template("manage.html")


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
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            session["phone"]=data["phone"]
            session["age"]=data["age"]
            session["gender"]=data["gender"]
            session["place"]=data["place"]
            session["password"]=data["password"]
            return render_template("home.html")
        else:
            flash("Mail and Password Mismatch","danger")
            return redirect(url_for("home"))

@app.route('/alogin', methods=["POST", "GET"])
def alogin():
        if request.method == "POST":
            name = request.form['name']
            password = request.form['password']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("Select * from data where name=? and password=?", (name, password))
            data = cur.fetchone()
            if data:
                return redirect(url_for("view"))
            else:
                flash("Username and Password Mismatch","danger")
                return redirect(url_for("admin"))


@app.route("/view")
def view():
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("Select* from data")
    data=cur.fetchall()
    con.close()
    return render_template("manage.html",data=data)

@app.route("/update/<string:id>",methods=["POST","GET"])
def update(id):
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("Select * from data where pid=?",(id,))
    data=cur.fetchone()
    con.close()

    if request.method=="POST":
        try:
            name=request.form['name']
            age=request.form['age']
            phone=request.form['phone']
            mail=request.form['mail']
            place=request.form['place']
            gender=request.form['gender']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("UPDATE data SET name=?,age=?,gender=?,phone=?,mail=?,place=? where pid=?" ,(name,age,gender,phone,mail,place,id))
            con.commit()
            flash("Record Update Successfully","success ")
        except:
            flash("Error in Update Data","danger")
        finally:
            con.close()
            return redirect(url_for("manage"))

    return render_template("update.html",data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)

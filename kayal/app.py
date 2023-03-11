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



conn = sqlite3.connect('courses.db', check_same_thread=False)
c = conn.cursor()

# Create "registered" table
c.execute(
    'CREATE TABLE IF NOT EXISTS registered (cname TEXT, p1 INTEGER, p2 INTEGER, p3 INTEGER, p4 INTEGER, p5 INTEGER, score INTEGER)')

# Create "suggestion" table
c.execute('CREATE TABLE IF NOT EXISTS suggestion (cname TEXT, enroll TEXT)')

# Create "completed" table
c.execute('CREATE TABLE IF NOT EXISTS completed (cname TEXT)')



# Handle "Registered" button click
@app.route('/registered', methods=['POST'])
def registered():
    cname = request.form['cname']
    p1 = request.form['p1']
    p2 = request.form['p2']
    p3 = request.form['p3']
    p4 = request.form['p4']
    p5 = request.form['p5']
    score = 0  # initial score is 0
    c.execute('INSERT INTO registered (cname, p1, p2, p3, p4, p5, score) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (cname, p1, p2, p3, p4, p5, score))
    conn.commit()
    return redirect(url_for('index'))


# Handle "Suggestion" button click
@app.route('/suggestion', methods=['POST'])
def suggestion():
    cname = request.form['cname']
    c.execute('INSERT INTO suggestion (cname, enroll) VALUES (?, 0)', (cname,))
    conn.commit()
    return redirect(url_for('index'))


@app.route('/rview')
def rview():
    # Retrieve the data from the "registered" table
    c.execute("SELECT * FROM registered")
    data = c.fetchall()
    return render_template('registered.html', data=data)


@app.route('/cview')
def cview():
    # Retrieve the data from the "completed" table
    c.execute("SELECT * FROM completed")
    data = c.fetchall()
    return render_template('completed.html', data=data)


@app.route('/sview', methods=['GET', 'POST'])
def sview():

    # Retrieve the data from the "suggestion" table
    c.execute("SELECT * FROM suggestion")
    data = c.fetchall()
    return render_template('suggestion.html', data=data)


@app.route('/enroll')
def enroll():
    cname = request.args.get('cname')
    if cname:
        # Get course name and update registered table
        c.execute('SELECT cname FROM suggestion WHERE cname = ?', (cname,))
        row = c.fetchone()
        if row:
            cname = row[0]
            c.execute('INSERT INTO registered (cname, p1, p2, p3, p4, p5, score) VALUES (?, "", "", "", "", "", 0)', (cname,))
            # Delete row from suggestion table
            c.execute('DELETE FROM suggestion WHERE cname = ?', (cname,))
            conn.commit()
            return redirect(url_for('home'))
    return "Invalid request."


@app.route('/finish/<string:cname>')
def finish(cname):
    # Get current score
    c.execute('SELECT score FROM registered WHERE cname = ?', (cname,))
    score = c.fetchone()[0]

    # Update score and move to "completed" table if score is 100
    if score >= 100:
        c.execute('SELECT cname FROM registered WHERE cname = ?', (cname,))
        cname = c.fetchone()[0]
        c.execute('INSERT INTO completed (cname) VALUES (?)', (cname,))
        c.execute('DELETE FROM registered WHERE cname = ?', (cname,))

    conn.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

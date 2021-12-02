from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="todo"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)


@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM task"
    con.execute(sql)
    res = con.fetchall()
    return render_template("home.html", datas=res)


@app.route("/todo", methods=["GET", "POST"])
def addTodo():
    res = 0
    if request.method == 'POST':
        task = request.form['task']
        assignee = request.form['assignee']
        reporter = request.form['reporter']
        days = request.form['days']
        con = mysql.connection.cursor()
        sql = "insert into task(task, assignee, reporter, days) values(%s, %s, %s, %s)"
        con.execute(sql, [task, assignee, reporter, days])
        mysql.connection.commit()
        con.close()
    con = mysql.connection.cursor()
    sql1 = "SELECT * FROM task"
    con.execute(sql1)
    res = con.fetchall()
    con.close()
    return render_template("home.html", datas=res)


@app.route("/changeStatus/<int:sno>",methods=['GET','POST'])
def changeStatus(sno):
    con = mysql.connection.cursor()
    sql = "update task set status='done' where sno=%s"
    con.execute(sql, [sno])
    mysql.connection.commit()
    sql1 = "SELECT * FROM task"
    con.execute(sql1)
    res = con.fetchall()
    con.close()
    return render_template("home.html", datas=res)


@app.route("/deleteTask/<int:sno>",methods=['GET','POST'])
def deleteTask(sno):
    con = mysql.connection.cursor()
    sql = "delete from task where sno=%s"
    con.execute(sql, [sno])
    mysql.connection.commit()
    sql1 = "SELECT * FROM task"
    con.execute(sql1)
    res = con.fetchall()
    con.close()
    return render_template("home.html", datas=res)

if __name__=='__main__':
    app.run(debug=True)
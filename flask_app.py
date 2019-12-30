
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
import mysql.connector

# Flask and SQL setup
app = Flask(__name__)

mydb = mysql.connector.connect(
  host="braedons.mysql.pythonanywhere-services.com",
  user="braedons",
  passwd="zotreport",
  database="braedons$zotreport"
)

mycursor = mydb.cursor()


# Get column names
mycursor.execute("SHOW COLUMNS FROM locations")
keys = mycursor.fetchall()


# Flask pages
@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/confirm', methods=["POST", "GET"])
def confirm():
    if request.method == "POST":
        # Get http request parameters
        params = request.form

        if params["button"] == "Create":

            # SQL insert statement
            sql = "INSERT INTO locations (name, type, date) VALUES (%s, %s, %s)"
            values = (params["name"], params["type"], params["date"])
            mycursor.execute(sql, values)
            mydb.commit()
            mycursor.execute("SELECT * FROM locations WHERE id=" + str(mycursor.lastrowid))
            result = mycursor.fetchall()

            # Get all entries in DB
            mycursor.execute("SELECT * FROM locations")
            allentries = mycursor.fetchall()

            return render_template("test.html", keys=keys, result=result, allentries=allentries, action="Added")
        elif params["button"] == "Delete":
            sqlDel = "DELETE FROM locations"
            sqlSel = "SELECT * FROM locations"

            # Building SQL select statement
            isFirstParam = True
            for col in keys[1:]:
                key = col[0]
                if params[key] != "":
                    if isFirstParam:
                        sqlDel += " WHERE "
                        sqlSel += " WHERE "
                        isFirstParam = False
                    else:
                        sqlDel += " AND "
                        sqlSel += " AND "

                    sqlDel += key + "='" + params[key] + "'"
                    sqlSel += key + "='" + params[key] + "'"

            mycursor.execute(sqlSel)
            result = mycursor.fetchall()
            mycursor.execute(sqlDel)
            mydb.commit()

            mycursor.execute("SELECT * FROM locations")
            allentries = mycursor.fetchall()

            return render_template("test.html", keys=keys, result=result, allentries=allentries, action="Deleted")
    elif request.method == "GET":
        params = request.args
        sql = "SELECT * FROM locations"

        # Building SQL select statement
        isFirstParam = True
        for col in keys[1:]:
            key = col[0]
            if params[key] != "":
                if isFirstParam:
                    sql += " WHERE "
                    isFirstParam = False
                else:
                    sql += " AND "

                sql += key + "='" + params[key] + "'"

        mycursor.execute(sql)
        result=mycursor.fetchall()

        mycursor.execute("SELECT * FROM locations")
        allentries = mycursor.fetchall()

        return render_template("test.html", keys=keys, result=result, allentries=allentries, action="Found")
    # elif request.method == "PUT":
    #     # Get http request parameters
    #     params = request.form

    #     # SQL insert statement
    #     sql = "INSERT INTO locations (name, type, date) VALUES (%s, %s, %s)"
    #     values = (params["Name"], params["Type"], params["Date"])
    #     mycursor.execute(sql, values)
    #     mydb.commit()

    #     # Get all entries in DB
    #     mycursor.execute("SELECT * FROM locations")
    #     allentries = mycursor.fetchall()

    #     return render_template("test.html", keys=keys, result=params, allentries=allentries)

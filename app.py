from flask import Flask, render_template, request
import sqlite3 
app = Flask(__name__)

# con = sqlite3.connect("Researchers.db")  
# print("Database opened successfully")  
# con.execute("create table Researchers (id INTEGER PRIMARY KEY , surname TEXT NOT NULL, initials TEXT UNIQUE NOT NULL, rating TEXT NOT NULL,institution TEXT NOT NULL,primaryResearch TEXT NOT NULL,secondaryResearch TEXT NOT NULL)")  
# print("Table created successfully")  

# con1 = sqlite3.connect("Institutions.db")  
# print("Database opened successfully")  
# con1.execute("create table Institutions (Name TEXT UNIQUE NOT NULL PRIMARY KEY, Location TEXT NOT NULL, NumberOfResearchers INTEGER NOT NULL)")  
# print("Table created successfully")  

@app.route("/")  
def index():  
    return render_template("index.html"); 

@app.route("/add")  
def add():  
    return render_template("add.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            surname = request.form["surname"]  
            initials = request.form["initials"]  
            rating = request.form["rating"]  
            institution = request.form["institution"]
            primaryResearch = request.form["primaryResearch"]
            secondaryResearch = request.form["secondaryResearch"]

            with sqlite3.connect("Researchers.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Researchers (surname, initials, rating, institution,primaryResearch,secondaryResearch) values (?,?,?,?,?,?)",(surname, initials, rating, institution,primaryResearch,secondaryResearch))  
                con.commit()  
                msg = "Researcher successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the researcher to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()   


@app.route("/addInstitution")  
def addInstitution():  
    return render_template("addInstitution.html")  
 
@app.route("/savedetailsOFInstitution",methods = ["POST","GET"])  
def saveDetailsOFInstitution():  
    msg1 = "msg"  
    if request.method == "POST":  
        try:  
            Name = request.form["Name"]  
            Location = request.form["Location"]  
            NumberOfResearchers = request.form["NumberOfResearchers"]  
            

            with sqlite3.connect("Institutions.db") as con1:  
                cur1 = con1.cursor()  
                cur1.execute("INSERT into Institutions (Name, Location, NumberOfResearchers) values (?,?,?)",(Name, Location, NumberOfResearchers))  
                con1.commit()  
                msg1 = "Institution successfully Added"  
        except:  
            con1.rollback()  
            msg1 = "We can not add the institution to the list"  
        finally:  
            return render_template("SuccessInstitution.html",msg1 = msg1)  
            con1.close()   




@app.route("/researchers")  
def researchers():  
    con = sqlite3.connect("Researchers.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Researchers")  
    rows = cur.fetchall()  
    return render_template("researchers.html",rows = rows)

@app.route("/institutions")  
def institutions():  
    con1 = sqlite3.connect("Institutions.db")  
    con1.row_factory = sqlite3.Row  
    cur1 = con1.cursor()  
    cur1.execute("select * from Institutions")  
    rows = cur1.fetchall()  
    return render_template("institutions.html",rows = rows)   

@app.route("/delete")  
def delete():  
    return render_template("delete.html")  

@app.route("/universityofcpt")  
def universityofcpt():  
    return render_template("institution.html")  

@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form["id"]  
    with sqlite3.connect("Researchers.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Researchers where id = ?",id)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)


@app.route("/deleteInstitution")  
def deleteInstitution():  
    return render_template("deleteInstitution.html")  

@app.route("/deleterecordInstitution",methods = ["POST"])  
def deleterecordInstitution():  
    Name = request.form["Name"]  
    with sqlite3.connect("Institutions.db") as con1:  
        try:  
            cur1 = con1.cursor()  
            cur1.execute("delete from Institutions where Name = ?",Name)  
            msg1 = "record successfully deleted"  
        except:  
            msg1 = "can't be deleted"  
        finally:  
            return render_template("delete_recordInstitution.html",msg1 = msg1)


# Search Function
# @app.route("/SearchResearcher")  
# def SearchResearcher():  
#     return render_template("SearchResearcher.html")  

# @app.route("/ResultResearcher",methods = ["POST"])  
# def ResultResearcher():  
#     Name = request.form["Name"]  
#     with sqlite3.connect("Researchers.db") as con:  
#         try:  
#             cur = con1.cursor()  
#             cur.execute("delete from Institutions where id = ?",id)  
#             msg = "record successfully deleted"  
#         except:  
#             msg = "can't be deleted"  
#         finally:  
#             return render_template("delete_recordInstitution.html",msg = msg)
   
if __name__ == '__main__':
   app.run(debug = True)
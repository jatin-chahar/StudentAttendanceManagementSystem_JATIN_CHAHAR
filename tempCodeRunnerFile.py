from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    passwd="12345",  # Replace with your MySQL password
    db="AttendanceDB"
)
cursor = db.cursor()

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Add Student Page
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        class_id = request.form["class_id"]
        
        # Insert into database
        query = "INSERT INTO Student (Name, Email, ClassID) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, class_id))
        db.commit()
        
        return redirect("/")
    return render_template("add_student.html")

# Mark Attendance
@app.route("/mark-attendance", methods=["GET", "POST"])
def mark_attendance():
    if request.method == "POST":
        student_id = request.form["student_id"]
        class_id = request.form["class_id"]
        date = request.form["date"]
        status = request.form["status"]
        
        # Insert attendance
        query = "INSERT INTO Attendance (StudentID, ClassID, Date, Status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (student_id, class_id, date, status))
        db.commit()
        
        return redirect("/")
    return render_template("mark_attendance.html")

# View Attendance
@app.route("/view-attendance")
def view_attendance():
    query = "SELECT * FROM Attendance"
    cursor.execute(query)
    attendance_records = cursor.fetchall()
    return render_template("view_attendance.html", records=attendance_records)

if __name__ == "__main__":
    app.run(debug=True)

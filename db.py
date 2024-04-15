#!/usr/bin/env python3
# Leah Tritz
# Gradebook to be used with standardized grading in my elementary school

import sqlite3
from contextlib import closing

from business import Student, Grade

# Initialize the connection to the SQLite database
conn = None

def connect():
    global conn
    if not conn:
        # Specify the database file
        DB_FILE = "gradebook_db.sqlite"
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

    # Create the StudentInfo table if it doesn't exist
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS StudentInfo(
                        studentID INTEGER PRIMARY KEY AUTOINCREMENT,
                        firstName TEXT,
                        lastName TEXT,
                        homeRoom TEXT)''')

    # Create the GradeInfo table if it doesn't exist
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS GradeInfo(
                    gradeID INTEGER PRIMARY KEY AUTOINCREMENT,
                    studentID INTEGER,
                    classDate DATE,
                    pracGrade INTEGER,
                    behavGrade INTEGER,
                    pracGradeTotal INTEGER DEFAULT 0,
                    behavGradeTotal INTEGER DEFAULT 0,
                    pracGradeCount INTEGER DEFAULT 0,
                    behavGradeCount INTEGER DEFAULT 0)''')
        
# Close the database connection
def close():
    if conn:
        conn.close()

# Create a Student object from a database row
def make_student(row):
    return Student(row["studentID"],
                   row["firstName"],
                   row["lastName"],
                   row["homeRoom"])

# Create a Grade object from a database row
def make_grade(row):
    try:
        if isinstance(row, dict):
            row_dict = row
        else:
            row_dict = {key: row[key] for key in row.keys()} 

        grade = Grade(
            row_dict.get("gradeID", None),
            row_dict.get("studentID", None),
            row_dict.get("classDate", None),
            row_dict.get("pracGrade", None),
            row_dict.get("behavGrade", None),
            row_dict.get("pracGradeTotal", 0),
            row_dict.get("behavGradeTotal", 0),
            row_dict.get("pracGradeCount", 0),
            row_dict.get("behavGradeCount", 0)
        )

        return grade
    except Exception as e:
        print(f"Error creating Grade: {e}")
        return None

# Retrieve an individual student with their grades from the database
def get_ind_student(id):
    student_query = '''SELECT studentID,
                              firstName,
                              lastName,
                              homeRoom
                      FROM StudentInfo
                      WHERE studentID = ?'''

    grade_query = '''SELECT gradeID,
                             classDate,
                             pracGrade,
                             behavGrade
                      FROM GradeInfo
                      WHERE studentID = ?
                      ORDER BY classDate'''

    with closing(conn.cursor()) as c:
        c.execute(student_query, (id,))
        student_row = c.fetchone()

        if student_row:
            student = make_student(student_row)

            c.execute(grade_query, (id,))
            grade_rows = c.fetchall()

            for grade_row in grade_rows:
                grade = make_grade(grade_row)
                student.add_grade(grade)

            return student
        else:
            return None

# Retrieve all students in a specific homeroom from the database
def get_classroom(homeroom):
    homeroom = homeroom.upper()
    query = '''SELECT studentID,
                      firstName,
                      lastName,
                      homeRoom
               FROM StudentInfo
               WHERE UPPER(homeRoom) = ?
               ORDER BY lastName'''
    with closing(conn.cursor()) as c:
        c.execute(query, (homeroom,))
        results = c.fetchall()

        classroom = []
        for row in results:
            student = make_student(row)
            classroom.append(student)
        return classroom

# Retrieve all students from the database
def get_all_students():
    query = '''SELECT studentID,
                      firstName,
                      lastName,
                      homeRoom
               FROM StudentInfo
               ORDER BY lastName'''
    with closing(conn.cursor()) as c:
        c.execute(query,)
        results = c.fetchall()

        all_students = []
        for row in results:
            student = make_student(row)
            all_students.append(student)
        return all_students
    
# Add a new student to the database
def add_student(student):
    query = '''INSERT INTO StudentInfo(
                           firstName,
                           lastName,
                           homeRoom)
                           VALUES (?,?,?)'''
    with closing(conn.cursor()) as c:
        c.execute(query, (
            student.firstName,
            student.lastName,
            student.homeRoom))
        conn.commit()
        return c.lastrowid

# Add grades for a student to the database
def add_grades(grade):
    query = '''INSERT INTO GradeInfo(
                            studentID,
                            classDate,
                            pracGrade,
                            behavGrade)
                            VALUES (?,?,?,?)'''
    with closing(conn.cursor()) as c:
        c.execute(query, (
            grade.studentID,
            grade.classDate,
            grade.pracGrade,
            grade.behavGrade))
        conn.commit()

        # Update the total and count values for practical and behavioral grades
        query_update_totals = '''UPDATE GradeInfo
                        SET
                            pracGradeTotal = pracGradeTotal + ?,
                            behavGradeTotal = behavGradeTotal + ?,
                            pracGradeCount = pracGradeCount + 1,
                            behavGradeCount = behavGradeCount + 1
                        WHERE studentID = ?'''

        c.execute(query_update_totals, (grade.pracGrade, grade.behavGrade, grade.studentID))
        conn.commit()

# Delete a student and their grades from the database
def delete_student_grade(studentID):
    query1 = '''DELETE FROM StudentInfo WHERE studentID = ?'''
    query2 = '''DELETE FROM GradeInfo WHERE studentID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query1, (studentID,))
        c.execute(query2, (studentID,))
    conn.commit()

# Update grades for a specific student in the database
def update_grades(gradeID, classDate, pracGrade, behavGrade):
    with closing(conn.cursor()) as c:
        query = '''UPDATE GradeInfo
                   SET
                       classDate = ?,
                       pracGrade = ?,
                       behavGrade = ?
                   WHERE gradeID = ?'''
        c.execute(query, (classDate, pracGrade, behavGrade, gradeID))
        conn.commit()

# Update the homeroom for a specific student in the database
def update_homeroom(studentID, homeRoom):
    with closing(conn.cursor()) as c:
        query = '''UPDATE StudentInfo
                   SET homeRoom = ?
                   WHERE studentID = ?'''
        c.execute(query, (homeRoom, studentID))
        conn.commit()

# Check if a student has a grade entry for a specific date in the database
def check_duplicate_date(student_id, class_date):
    query = '''SELECT COUNT(*)
               FROM GradeInfo
               WHERE studentID = ? AND classDate = ?'''

    with closing(conn.cursor()) as c:
        c.execute(query, (student_id, class_date))
        count = c.fetchone()[0]

    return count > 0

# Main function to demonstrate database operations
def main():
    connect()
    classroom = get_classroom(homeroom)
    for student in classroom:
        # Print student information along with grade details
        print(Student.studentID, Student.firstName,
              Student.lastName, Student.homeRoom,
              Grade.classDate, Grade.pracGrade,
              Grade.behavGrade, Grade.pracGradeAvg,
              Grade.behavGradeAvg)

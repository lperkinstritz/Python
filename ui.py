#!/usr/bin/env python3
# Leah Tritz
# Gradebook to be used with standardized grading in my elementary school

import db
from business import Student, Grade
from datetime import datetime

# List of homeroom options
HOMEROOM = ("KVH", "KLF", "KAN", "KBS", "KMK", "KEM",
            "1RW", "1JC", "1AO", "1MG", "1KB", "1TO",
            "2JF", "2KG", "2CE", "2BB", "2RB", "2JB",
            "3AD", "3GV", "3RW", "3MN", "3SD", "3LH",
            "4AS", "4SJ", "4TS", "4JN", "4PD", "4CN")

# Function to add a new student and their grades to the gradebook
def add_student_and_grades():
    firstName = input("First name of student: ").title()
    lastName = input("Last name of student: ").title()
    studentID = None  
    homeroom = get_homeroom(studentID)
    studentID = db.add_student(Student(studentID=None, firstName=firstName, lastName=lastName, homeRoom=homeroom))
    student = db.get_ind_student(studentID)
    print(f"{student.fullName} was added with Student ID {student.studentID}.\n")

    while True:
        classDate = get_classDate()
        if classDate == '0' or classDate is None:
            print("Finished adding grades.")
            print()
            print()
            break   
        if not db.check_duplicate_date(student.studentID, classDate):
            pracGrade = get_pracGrade()
            behavGrade = get_behavGrade()
            formatted_date = classDate
            grade = Grade(gradeID=None, studentID=student.studentID, classDate=formatted_date, pracGrade=pracGrade, behavGrade=behavGrade)
            db.add_grades(grade)
            print(f"Grades were added for {student.fullName}.\n")
        else:
            print(f"Duplicate date detected. Please enter a different date.")
        

# Function to add grades for an existing student in the gradebook
def add_grades():
    print("You have chosen to add grades for a student.")
    while True:
        studentID_Grades_To_Be_Added = get_student_ID()

        if studentID_Grades_To_Be_Added is None:
            print("Returning to the main menu.")
            return

        student = db.get_ind_student(studentID_Grades_To_Be_Added)

        # Validate that the student exists
        if student is not None:
            print(f"You selected {student.fullName} grades to add.")

            if student.grades is not None:
                print()
                print()
                print(f"{student.fullName}")
                print(f"{'Date':<15}{'Practical Grade':<20}{'Behavioral Grade':<20}")
                print("-" * 60)

                for grade in student.grades:
                    print(f"{grade.classDate:<15}{grade.pracGrade:<20}{grade.behavGrade:<20}")

                print()
                print()

                while True:
                    classDate = get_classDate()

                    if classDate == '0' or classDate is None:
                        print(f"Finished adding grades for {student.fullName}.")
                        print()
                        print()
                        return

                    # Check for duplicate date before adding the grade
                    if not db.check_duplicate_date(student.studentID, classDate):
                        pracGrade = get_pracGrade()
                        behavGrade = get_behavGrade()
                        formatted_date = classDate
                        new_grade = Grade(studentID=studentID_Grades_To_Be_Added, classDate=formatted_date, pracGrade=pracGrade, behavGrade=behavGrade)
                        db.add_grades(new_grade)
                        print(f"Grades were added for {student.fullName} on {formatted_date}.\n")
                    else:
                        print(f"Duplicate date detected. Please enter a different date.")
                print()
                print()
        else:
            print(f"Error: Student with ID {studentID_Grades_To_Be_Added} not found. Please check the ID and try again.")


# Function to retrieve the homeroom from user input
def get_homeroom(studentID):
    while True:
            homeroom = input("Enter student homeroom:  ").upper()
            if homeroom in HOMEROOM:
                return homeroom
            else:
                print("Invalid homeroom. Try again.")
                display_homerooms()


# Function to retrieve the student ID from user input
def get_student_ID():
    while True:
        display_students()

        student_ID = input("Enter student ID (or 0 to go back to the main menu): ").strip()

        if student_ID == '0':
            return None  # User wants to go back to the main menu

        if not student_ID.isdigit():
            print("Invalid input. Please enter a numeric student ID.")
            continue

        student_ID = int(student_ID)

        # Check if the entered student ID exists
        if db.get_ind_student(student_ID) is not None:
            return student_ID
        else:
            print("Invalid student ID. Please try again.")


# Function to display homeroom options
def display_homerooms():
    print(HOMEROOM)


# Function to retrieve practical grade from user input
def get_pracGrade():
    while True:
        pracGrade = int(input("Enter standardized grade for practical skills:  "))
        if pracGrade not in {1, 2, 3}:
            print("Invalid grade. Please enter 1, 2, or 3")
        else:
            return pracGrade


# Function to retrieve behavioral grade from user input
def get_behavGrade():
    while True:
        behavGrade = int(input("Enter standardized grade for behavior:  "))
        if behavGrade not in {1, 2, 3}:
            print("Invalid grade. Please enter 1, 2, or 3")
        else:
            return behavGrade


# Function to retrieve class date from user input
def get_classDate():
    while True:
        date_str = input("Enter class date (yyyy-mm-dd) or 0 to end: ")
        if date_str == '0':
            return None
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            print("Invalid date format. Please enter the date in yyyy-mm-dd format.")


# Function to view grades of an individual student
def view_student_grades():
    print("You are viewing individual student grades.")
    grades_to_be_viewed = get_student_ID()
    student = db.get_ind_student(grades_to_be_viewed)

    if student is not None and student.grades is not None:
        print()
        print()
        print(f"{student.fullName}")
        print(f"{'Date':<15}{'Practical Grade':<20}{'Behavioral Grade':<20}")
        print("-" * 60)

        for grade in student.grades:
            print(f"{grade.classDate:<15}{grade.pracGrade:<20}{grade.behavGrade:<20}")
            
    else:
        print(f"No grades found for {student.fullName} (Student ID: {grades_to_be_viewed}).")

    print()
    print()


# Function to delete a student and their grades from the gradebook
def delete_student():
    print("You are deleting a student.")
    studentID_To_Be_Deleted = get_student_ID()
    
    # Check if the entered student ID exists
    if studentID_To_Be_Deleted is not None:
        student = db.get_ind_student(studentID_To_Be_Deleted)

        # Validate that the student exists
        if student is not None:
            db.delete_student_grade(studentID_To_Be_Deleted)
            print(f"{student.fullName} was deleted.\n")
        else:
            print(f"Error: Student with ID {studentID_To_Be_Deleted} not found. Please check the ID and try again.")
    else:
        print("Returning to the main menu.")


# Function to update the homeroom of a student in the gradebook
def update_student_homeroom():
    print("You are updating a student's homeroom")
    studentID_To_Be_Updated = get_student_ID()
    
    # Check if the entered student ID exists
    if studentID_To_Be_Updated is not None:
        student = db.get_ind_student(studentID_To_Be_Updated)

        # Validate that the student exists
        if student is not None:
            print(f"You selected {student.fullName} to update homeroom.")
            print()
            print("Enter the new classroom.")
            homeRoom = get_homeroom(studentID_To_Be_Updated)

            student.homeRoom = homeRoom
            db.update_homeroom(student.studentID, homeRoom)
            print(f"{student.fullName} was updated.")
            print()
            print()
        else:
            print(f"Error: Student with ID {studentID_To_Be_Updated} not found. Please check the ID and try again.")
    else:
        print("Returning to the main menu.")


# Function to edit grades of a student in the gradebook
def edit_grades():
    print("You've chosen to change a student's grades")

    studentID_Grades_To_Be_Updated = get_student_ID()
    student = db.get_ind_student(studentID_Grades_To_Be_Updated)

    # Validate that the student exists
    if student is not None:
        print()
        print()
        if student and student.grades:
            print(f"You selected {student.fullName} grades to update.")

            while True:
                print()
                print(f"{'Grade ID':<10}{'Date':<15}{'Practical Grade':<20}{'Behavioral Grade':<20}")
                print("-" * 80)

                for grade in student.grades:
                    print(f"{grade.gradeID:<10}{grade.classDate:<15}{grade.pracGrade:<20}{grade.behavGrade:<20}")

                print()
                gradeID_to_update = int(input("Enter the Grade ID you want to update (0 to exit): "))

                if gradeID_to_update == 0:
                    print("Finished updating grades.")
                    print()
                    print()
                    return

                # Find the existing grade for the specified gradeID
                existing_grade = next((grade for grade in student.grades if grade.gradeID == gradeID_to_update), None)

                if existing_grade:
                    pracGrade = get_pracGrade()
                    behavGrade = get_behavGrade()

                    # Update the existing_grade directly
                    existing_grade.pracGrade = pracGrade
                    existing_grade.behavGrade = behavGrade

                    db.update_grades(existing_grade.gradeID, existing_grade.classDate, pracGrade, behavGrade)

                    print()
                    print(f"{student.fullName}'s grades with Grade ID {gradeID_to_update} have been updated.")
                    print()
                else:
                    print(f"No grades found for {student.fullName} with Grade ID {gradeID_to_update}. Please try again.")

        else:
            print(f"No grades found for {student.fullName} (Student ID: {studentID_Grades_To_Be_Updated}).")
    else:
        print(f"Error: Student with ID {studentID_Grades_To_Be_Updated} not found. Please check the ID and try again.")


# Function to display students in the gradebook
def display_students(homeroom=None):
    homeroom_input = input("Enter student homeroom (ALL for every student or LIST for homerooms):  ").strip().upper()

    if homeroom_input == 'ALL':
        students = db.get_all_students()
        if students:
            print()
            print(f"{'Student ID':<13}  {'Student':<20}{'Homeroom':<10}  {'Avg Practical Grade':<20}  {'Avg Behavior Grade':<20}")
            print("-" * 90)
            for student in students:
                student = db.get_ind_student(student.studentID)
                print(f"{student.studentID:<13d}{student.fullName:<25}{student.homeRoom:18}",
                      end=f"{student.get_pracGradeAvg():<24.2f} {student.get_behavGradeAvg():<24.2f}\n")
            print()
        else:
            print()
            print("There are currently no students in the gradebook.")
    elif homeroom_input == 'LIST':
        print()
        print()
        print("All Elementary homerooms:  ", HOMEROOM)
        print()
        print()
    elif homeroom_input in HOMEROOM:
        students = db.get_classroom(homeroom_input)
        if not students:
            print(f"The {homeroom_input} class is empty.")
        else:
            print()
            print(f"{'Student ID':<13}  {'Student':<20}{'Homeroom':<10}  {'Avg Practical Grade':<20}  {'Avg Behavior Grade':<20}")
            print("-" * 90)
            for student in students:
                student = db.get_ind_student(student.studentID)
                print(f"{student.studentID:<13d}{student.fullName:<25}{student.homeRoom:18}",
                      end=f"{student.get_pracGradeAvg():<24.2f} {student.get_behavGradeAvg():<24.2f}\n")
            print()
    else:
        print("Invalid homeroom entered.")

    print()
    print()


# Function to display the title of the gradebook
def display_title():
    title = "2023-2024 Computer Gradebook"
    centered_title = title.center(60)
    print(centered_title)


# Function to display the main menu options
def display_menu():
    print()
    print()
    print("Menu Options")
    print("1 - Display classroom")
    print("2 - Add student and grades")
    print("3 - Remove student")
    print("4 - Edit student homeroom")
    print("5 - Edit student grades")
    print("6 - Add student grades")
    print("7 - View individual student grades")
    print("0 - Exit")
    print()


# Main function to run the gradebook program
def main():
    display_title()
    db.connect()

    while True:
        display_menu()

        try:
            option = int(input("Menu option: "))
        except ValueError:
            print("Invalid input. Please enter a valid numeric option.\n")
            continue

        if option == 1:
            display_students()
        elif option == 2:
            add_student_and_grades()
        elif option == 3:
            delete_student()
        elif option == 4:
            update_student_homeroom()
        elif option == 5:
            edit_grades()
        elif option == 6:
            add_grades()
        elif option == 7:
            view_student_grades()
        elif option == 0:
            db.close()
            print("Gradebook Closed")
            break
        else:
            print("Not a valid option. Please try again.\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Leah Tritz
# Gradebook to be used with standardized grading in my elementary school

from dataclasses import dataclass
from typing import List

# Defining the Grade class
class Grade:
    def __init__(self, gradeID=None, studentID=None, classDate=None, pracGrade=None, behavGrade=None, 
                 pracGradeTotal=0, behavGradeTotal=0, pracGradeCount=0, behavGradeCount=0):
        self.gradeID = gradeID
        self.studentID = studentID
        self.classDate = classDate
        self.pracGrade = pracGrade
        self.behavGrade = behavGrade
        self.pracGradeTotal = pracGradeTotal
        self.behavGradeTotal = behavGradeTotal
        self.pracGradeCount = pracGradeCount
        self.behavGradeCount = behavGradeCount

    # Calculate practical grade average
    def get_pracGradeAvg(self):
        return self.pracGradeTotal / self.pracGradeCount if self.pracGradeCount > 0 else 0

    # Calculate behavioral grade average
    def get_behavGradeAvg(self):
        return self.behavGradeTotal / self.behavGradeCount if self.behavGradeCount > 0 else 0


# Defining the Student class
class Student:
    def __init__(self, studentID, firstName, lastName, homeRoom):
        self.studentID = studentID
        self.firstName = firstName
        self.lastName = lastName
        self.homeRoom = homeRoom
        self.grades = []

    # Add a grade to the student's list of grades
    def add_grade(self, grade):
        self.grades.append(grade)
        
    # Calculate the average practical grade for the student
    def get_pracGradeAvg(self):
        if self.grades:
            return sum(grade.pracGrade for grade in self.grades) / len(self.grades)
        else:
            return 0

    # Calculate the average behavioral grade for the student
    def get_behavGradeAvg(self):
        if self.grades:
            return sum(grade.behavGrade for grade in self.grades) / len(self.grades)
        else:
            return 0

    # Computed property to get the full name of the student
    @property
    def fullName(self):
        return f"{self.firstName} {self.lastName}"
        

if __name__=="__main__":
    # The main function is missing, assuming it will be added later
    pass

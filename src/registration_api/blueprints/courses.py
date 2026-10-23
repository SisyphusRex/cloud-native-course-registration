"""Course catalog endpoint."""

# Standard Library imports

# Third Party imports
from flask import Blueprint, jsonify

# First party imports

courses_bp = Blueprint(name="courses", import_name=__name__)

# WMU graduate Computer Science courses (source: docs/courses.txt).
COURSES = [
    {"id": "CS5110", "title": "Big Data"},
    {"id": "CS5115", "title": "Programming Prep for Graduate Studies"},
    {"id": "CS5260", "title": "Parallel Computations"},
    {"id": "CS5270", "title": "Computer Graphics"},
    {"id": "CS5300", "title": "Artificial Neural Systems"},
    {"id": "CS5310", "title": "Algorithms"},
    {"id": "CS5410", "title": "Game Programming"},
    {"id": "CS5430", "title": "Database Systems"},
    {"id": "CS5541", "title": "Computer Systems"},
    {"id": "CS5550", "title": "Computer Networks and Distributed Systems"},
    {"id": "CS5560", "title": "Network Programming"},
    {"id": "CS5610", "title": "Advanced R Programming for Data Science"},
    {"id": "CS5700", "title": "Computer Security and Information Assurance"},
    {"id": "CS5750", "title": "Secure Software Development"},
    {"id": "CS5800", "title": "Theory Foundations"},
    {"id": "CS5810", "title": "Compiler Design and Implementation"},
    {"id": "CS5820", "title": "Artificial Intelligence"},
    {"id": "CS5821", "title": "Machine Learning"},
    {"id": "CS5822", "title": "Natural Language Processing"},
    {"id": "CS5823", "title": "Autonomous Vehicles for CS Majors"},
    {"id": "CS5950", "title": "Advanced Topics in Computer and Information Science"},
    {"id": "CS5990", "title": "Independent Study in Computer Science"},
    {"id": "CS6030", "title": "Cloud Computing"},
    {"id": "CS6100", "title": "Advanced Storage, Retrieval and Processing of Big Data"},
    {"id": "CS6110", "title": "Data Science Foundations"},
    {"id": "CS6250", "title": "Advanced Computer Architecture"},
    {"id": "CS6260", "title": "Advanced Parallel Computations"},
    {"id": "CS6310", "title": "Advanced Design and Analysis of Algorithms"},
    {"id": "CS6430", "title": "Database Management System Implementation"},
    {"id": "CS6530", "title": "Data Mining"},
    {"id": "CS6550", "title": "Advanced Operating Systems"},
    {"id": "CS6560", "title": "Advanced Computer Networks: Anatomy of the Internet"},
    {"id": "CS6570", "title": "Wireless Networks"},
    {"id": "CS6580", "title": "Pervasive Computing"},
    {"id": "CS6600", "title": "Software Engineering"},
    {"id": "CS6610", "title": "Software Testing"},
    {"id": "CS6700", "title": "Advanced Computer and Information Security"},
    {"id": "CS6720", "title": "Pattern Recognition"},
    {"id": "CS6800", "title": "Advanced Theory of Computation"},
    {"id": "CS6810", "title": "Compiler Optimization"},
    {"id": "CS6820", "title": "Advanced Artificial Intelligence"},
    {"id": "CS6821", "title": "Information Retrieval"},
    {"id": "CS6910", "title": "Seminar in Computer Science"},
    {"id": "CS6970", "title": "Master's Project"},
    {"id": "CS7000", "title": "Master's Thesis"},
    {"id": "CS7100", "title": "Independent Research"},
    {"id": "CS7120", "title": "Professional Field Experience"},
    {"id": "CS7250", "title": "Doctoral Research Seminar"},
    {"id": "CS7300", "title": "Doctoral Dissertation"},
    {"id": "CS7350", "title": "Graduate Research"},
]
COURSE_IDS = {course["id"] for course in COURSES}


# courses page
@courses_bp.get("/courses")
def list_courses():
    return jsonify(COURSES)

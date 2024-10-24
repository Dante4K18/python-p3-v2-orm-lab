#!/usr/bin/env python3

from __init__ import CONN, CURSOR
import random
from department import Department
from employee import Employee
from review import Review
import ipdb


def reset_database():
    Review.drop_table()
    Employee.drop_table()
    Department.drop_table()
    Department.create_table()
    Employee.create_table()
    Review.create_table()

def test_get_employees(self):
    from employee import Employee  # Avoid circular import
    Employee.all = {}  # Reset Employee records


    # Create seed data
    department1 = Department.create("Payroll", "Building A, 5th Floor")
    department2 = Department.create("Human Resources", "Building C, 2nd Floor")
    employee1 = Employee.create("Raha", "Accountant", department1.id)
    employee2 = Employee.create("Tal", "Senior Accountant", department1.id)
    employee3 = Employee.create("Amir", "Manager", department2.id)
    Review.create(2023, "Efficient worker", employee1.id)
    Review.create(2022, "Good work ethic", employee1.id)
    Review.create(2023, "Excellent communication skills", employee2.id)

    employees = department1.employees()
    assert len(employees) == 2

reset_database()
ipdb.set_trace()

# lib/employee.py
from __init__ import CURSOR, CONN
from department import Department
from lib.db import CURSOR
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'

    id = Column (Integer, primary_key=True)
    name = Column (String)

    @classmethod
    def create_table(cls, session):
        cls.__table__.create(bind=session.bind, checkfirst=True)

    @classmethod
    def drop_table(cls, session):
        cls.__table__.drop(bind=session.bind, checkfirst=True)

     # Dictionary of objects saved to the database.
    all = {}

    @classmethod
    def create(cls, name, job_title, department_id):
        # Code to create and insert a new Employee instance
        employee = cls(None, name, job_title, department_id)
        CURSOR.execute(
            "INSERT INTO employees (name, job_title, department_id) VALUES (?, ?, ?)",
            (name, job_title, department_id)
        )
        employee.id = CURSOR.lastrowid
        return employee

    @classmethod
    def create(cls, session, name):
        if not name:
            raise ValueError("Name must be a non-empty string")
        employee = cls(name=name)
        session.add(employee)
        session.commit()
        return employee


   
    def __init__(self, name, job_title, department_id, id=None):
        self.id = id
        self.name = name
        self.job_title = job_title
        self.department_id = department_id

    def __repr__(self):
        return (
            f"<Employee {self.id}: {self.name}, {self.job_title}, " +
            f"Department ID: {self.department_id}>"
        )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def job_title(self):
        return self.job_title

    @job_title.setter
    def job_title(self, job_title):
        if isinstance(job_title, str) and len(job_title):
            self._job_title = job_title
        else:
            raise ValueError(
                "job_title must be a non-empty string"
            )

    @property
    def department_id(self):
        return self._department_id

    @department_id.setter
    def department_id(self, department_id):
        if type(department_id) is int and Department.find_by_id(department_id):
            self._department_id = department_id
        else:
            raise ValueError(
                "department_id must reference a department in the database")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Employee instances """
        sql = """
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            job_title TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id))
        """
        CURSOR.execute(sql)
        CONN.commit()
        CURSOR.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(CURSOR.fetchall())  # This should list all tables, including 'employees' if it was created


    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Employee instances """
        sql = """
            DROP TABLE IF EXISTS employees;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, job title, and department id values of the current Employee object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO employees (name, job_title, department_id)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.job_title, self.department_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self, session, name):
        if not name:
            raise ValueError("Name must be a non-empty string")
        self.name = name
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()


    @classmethod
    def instance_from_db(cls, row):
        """Return an Employee object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        employee = cls.all.get(row[0])
        if employee:
            # ensure attributes match row values in case local instance was modified
            employee.name = row[1]
            employee.job_title = row[2]
            employee.department_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            employee = cls(row[1], row[2], row[3])
            employee.id = row[0]
            cls.all[employee.id] = employee
        return employee

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, employee_id):
        employee = session.query(cls).filter_by(id=employee_id).first()
        if employee is None:
            raise ValueError("Employee not found")
        return employee
    
    @classmethod
    def find_by_name(cls, name):
        """Return Employee object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM employees
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def reviews(self):
     from review import Review  # Avoid circular import
    
    # Fetch all reviews for this employee
     CURSOR.execute("SELECT * FROM reviews WHERE employee_id = ?", (self.id,))
     review_rows = CURSOR.fetchall()
     print("Fetched reviews:", review_rows)  # Debug statement
    
    # Create Review instances
     if review_rows:
        review_instances = [Review.instance_from_db(row) for row in review_rows]
        return review_instances
     return []


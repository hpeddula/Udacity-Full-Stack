import os
import sys
from sqlalchemy import Column,Integer,ForeignKey,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    name = Column(String(80),nullable=False)
    id = Column(Integer,primary_key=True)

class Address(Base):
    __tablename__ ='address'
    street = Column(String(80),nullable=False)
    zip = Column(String(5),nullable=False)
    id = Column(Integer,primary_key=True)
    employee_id = Column(Integer,ForeignKey('employee.id'))
    employee = relationship(Employee)
    #relationship tells SQLAlchemy what relationship one table has with another
    #Foreign Key allows us to refer a row in a different table,if there is a relationship between those two tables.
engine = create_engine('sqlite:///empData.db')

Base.metadata.create_all(engine)

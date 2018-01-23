# Specter Block Implementation
# Nick Frichette 1/23/2017

"""This is the base that transcends classes for SQL Alchemy"""

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import os
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

SQLBase = sqlalchemy.ext.declarative.declarative_base()

class Racks(SQLBase):
    __tablename__ = "racks"
    name = sqlalchemy.Column(sqlalchemy.String(63), nullable=False, primary_key=True)
    height = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    order = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    room = sqlalchemy.Column(sqlalchemy.String(16), nullable=False)
    last_updated = sqlalchemy.Column(sqlalchemy.TIMESTAMP(), nullable=False)
    last_updated_by = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)

class Devices(SQLBase):
    __tablename__ = "devices"
    id = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    rack = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    rack_first_slot = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    rack_last_slot = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    ip = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    contact = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    owner = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    service_level = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    model = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    comments = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)

    last_updated = sqlalchemy.Column(sqlalchemy.TIMESTAMP(), nullable=False)
    last_updated_by = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)

with open(os.path.join(os.getenv("HOME"), ".my.cnf")) as f:
    password = dict(line.strip().split("=") for line in f if line.count("=") == 1)["password"]

sqlengine = sqlalchemy.create_engine("mysql://cela:%s@sql.mit.edu/cela+hwops" % password)
SQLBase.metadata.bind = sqlengine

session = sqlalchemy.orm.sessionmaker(bind=sqlengine)()

def get_all_racks():
    return session.query(Racks).all()

def get_all_devices():
    return session.query(Devices).all()

def get_rack(name):
    return session.query(Racks).filter_by(name=name).one()

def get_device(id):
    return session.query(Devices).filter_by(id=id).one()

def add(x):
    session.add(x)
    session.commit()

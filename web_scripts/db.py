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

class DeviceIDs(SQLBase):
    __tablename__ = "deviceids"
    id = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False, primary_key=True)

class DeviceUpdates(SQLBase):
    __tablename__ = "devices"
    id = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    txid = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    rack = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    rack_first_slot = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    rack_last_slot = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    ip = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    contact = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    owner = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    service_level = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    model = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    notes = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)

    last_updated = sqlalchemy.Column(sqlalchemy.TIMESTAMP(), nullable=False)
    last_updated_by = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)

class Parts(SQLBase):
    __tablename__ = "parts"
    sku = sqlalchemy.Column(sqlalchemy.String(63), nullable=False, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    comments = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)

    last_updated = sqlalchemy.Column(sqlalchemy.TIMESTAMP(), nullable=False)
    last_updated_by = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)

class Inventory(SQLBase):
    __tablename__ = "inventory"
    txid = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False, primary_key=True)
    sku = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)
    new_count = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    comment = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)

    submitted = sqlalchemy.Column(sqlalchemy.TIMESTAMP(), nullable=False)
    submitted_by = sqlalchemy.Column(sqlalchemy.String(63), nullable=False)

with open(os.path.join(os.getenv("HOME"), ".my.cnf")) as f:
    password = dict(line.strip().split("=") for line in f if line.count("=") == 1)["password"]

sqlengine = sqlalchemy.create_engine("mysql://hwops:%s@sql.mit.edu/hwops+hwops" % password)
SQLBase.metadata.bind = sqlengine

session = sqlalchemy.orm.sessionmaker(bind=sqlengine)()

def get_all_racks():
    return session.query(Racks).all()

def get_all_devices():
    devices = []
    seen = set()
    for device in session.query(DeviceUpdates).order_by(DeviceUpdates.txid.desc()).all():
        if device.id in seen:
            continue
        seen.add(device.id)
        devices.append(device)
    return devices

def get_all_parts():
    return session.query(Parts).all()

def get_latest_inventory():
    # TODO: do this more efficiently
    updates = session.query(Inventory).all()
    latest = {}
    for update in updates:
        if update.sku not in latest or latest[update.sku].txid < update.txid:
            latest[update.sku] = update
    return latest

def get_inventory(sku):
    return session.query(Inventory).filter_by(sku=sku).all()

def get_part(sku):
    return session.query(Parts).filter_by(sku=sku).one()

def get_rack(name):
    return session.query(Racks).filter_by(name=name).one()

# latest version is at the end of the returned list
def get_device_history(id):
    return session.query(DeviceUpdates).filter_by(id=id).order_by(DeviceUpdates.txid).all()

def get_device_latest(id):
    return session.query(DeviceUpdates).filter_by(id=id).order_by(DeviceUpdates.txid.desc()).limit(1).one()

def add(x):
    session.add(x)
    session.commit()

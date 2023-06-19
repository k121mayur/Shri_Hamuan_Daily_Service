from application.database import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(64))
    mobile_number = db.Column(db.Integer)
    role = db.Column(db.String(10))
    username = db.Column(db.String(32), index=True, unique=True)
    password= db.Column(db.String(32))

    def is_active(self):
        return True

class party(db.Model):
    __tablename__ = "party"
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    business_name = db.Column(db.String(64))
    owner_name = db.Column(db.String(64))
    mobile_number = db.Column(db.Integer)
    address = db.Column(db.String(256))
    gst_number = db.Column(db.String(32))
    pan_number = db.Column(db.String(15))
    rate = db.Column(db.Float)

class consignee(db.Model):
    __tablename__ = "consignee"
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    business_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    owner_name = db.Column(db.String(64))
    mobile_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(256), nullable=False)

    '''<!-- 
                Following Questions need to be added: 
                1) Consignors Name type=options
                2) Consignees Name type=text
                3) Consignees Address type=text
                4) From Branch type=Option
                5) To Branch type=Option
                6) Invoice Number type=number
                7) Description of Goods = text
                8) Consignment Value type=number
                9) Consignment Weight type=number
                10) POD chanrges type=number
                11) Payment Method type=option
                12) Consignment Charges type=number
            -->'''
class orders():
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    order_date = db.Column(db.DateTime)
    from_branch = db.Column(db.String())
    to_branch = db.Column(db.String())
    party_id = db.Column(db.Integer, db.ForeignKey("party.id"))
    cosignee_name = db.Column(db.String())
    consinee_address = db.Column(db.String())
    inovice_number = db.Column(db.Integer)
    description_of_goods = db.Column(db.String())
    number_of_packges = db.Column(db.Integer)
    consignment_value = db.Column(db.Float)
    consignment_weight = db.Column(db.Float)
    pod_charges = db.Column(db.Integer)
    payment_mode = db.Column(db.String())
    total_amount = db.Column(db.Float)
    entry_by = db.Column(db.Integer, db.ForeignKey("users.id"))


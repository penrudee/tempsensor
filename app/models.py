from app import app, db, login_manager
from sqlalchemy import ForeignKey,Column,Integer,String,DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import datetime
from sqlalchemy.orm import relationship
import jwt
from time import time
import pytz
tz=pytz.timezone('Asia/Bangkok')


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    businessunits = db.relationship('BusinessUnit', backref='staff', lazy='dynamic')
    role = db.Column(db.String(),default='USER')
    about = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.datetime.now(tz))
    line =db.Column(db.String())
    mobile=db.Column(db.String)
    nodess = db.relationship('Nodes', backref='staff', lazy='dynamic')
    Node_SetUp=db.relationship('Node_SetUp',backref='staff',lazy='dynamic')
    def __repr__(self):
        return '<User {}, email{},role{}>'.format(self.username,self.email,self.role)  
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self): # line 37
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class BusinessUnit(UserMixin, db.Model):
    __tablename__='businessunit'
    id = db.Column(db.Integer, primary_key=True)
    bu_name = db.Column(db.String(64), index=True, unique=True)
    image_bu=db.Column(db.String)
    gps_location=db.Column(db.String)
    create_on = db.Column(db.DateTime, nullable=False,  default=datetime.datetime.now(tz))
    edit_on = db.Column(db.DateTime, nullable=False,  default=datetime.datetime.now(tz))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User",backref="businessunit")
    nodes = db.relationship('Node', backref='businessunit', lazy='dynamic')
    nodess = db.relationship('Nodes', backref='businessunit', lazy='dynamic')
    Node_SetUp = db.relationship('Node_SetUp', backref='businessunit', lazy='dynamic')
    def __repr__(self):
        return '<Business Unit id={}, Business Unit name ={}>'.format(self.id,self.bu_name)
    def __init__(self,
                bu_name="",
                image_bu="",
                gps_location=""):
        self.bu_name=bu_name
        self.image_bun=image_bu
        self.gps_location=gps_location
        

    def as_dict(self):
        return {'id':self.id,
                'bu_name':self.bu_name
                }

class Node(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String)
    gps_latitude=db.Column(db.String)
    gps_longtitude=db.Column(db.String)

    image_node =db.Column(db.String) 
    sensor_name = db.Column(db.String)
    imei=db.Column(db.String)

    tank_size = db.Column(db.String,default=0)
    current_Height = db.Column(db.String,default=0)
    current_Volumn = db.Column(db.String,default=0)
    timestamp =   db.Column(db.DateTime, nullable=False,  default=datetime.datetime.now(tz))
    high_level_alert = db.Column(db.String,default=0)
    low_level_alert = db.Column(db.String,default=0)
    maximum_rise_alert = db.Column(db.String,default=0)
    maximum_drop_alert = db.Column(db.String,default=0)

    bu_id = db.Column(db.Integer, db.ForeignKey('businessunit.id'))
    businessunits = relationship("BusinessUnit",backref="node")
    def __repr__(self):
        return '<Node id={}, Node name ={}>'.format(self.id,self.node_name)




class Edit(db.Model):
    __tablename__="edit"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_on = db.Column(db.DateTime, nullable=False,  default=datetime.datetime.now(tz))
    def __init__(self,create_on):
        self.create_on = datetime.datetime.now(tz)
        
    def __repr__(self):
        return '<Edit id={}, create on={}>'.format(self.id,self.create_on)
class Edit_node(db.Model):
    __tablename__="edit_node"
    id             =db.Column(db.Integer, primary_key=True, autoincrement=True)
    edit_id        = db.Column(db.Integer, db.ForeignKey("edit.id"),nullable=False)
    node_id         = db.Column(db.Integer, db.ForeignKey("node.id"), nullable=False)
    edit           = relationship("Edit", backref ="edit_node")
    node            = relationship("Node", backref="edit_node")
    user_id        = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user           = relationship("User",backref="edit_node")     
class Nodes(db.Model):
    __tablename__='Nodes'
    id = db.Column(db.Integer,primary_key=True)
    api_key = db.Column(db.String)
    mac = db.Column(db.String,unique=True)    
    user_id        = db.Column(db.Integer, db.ForeignKey("user.id"))
    user           = relationship("User",backref="Nodes")
    bu_id = db.Column(db.Integer, db.ForeignKey('businessunit.id'))
    businessunits = relationship("BusinessUnit",backref="Nodes")
    temp_hight_alert=db.Column(db.String)
    temp_low_alert=db.Column(db.String)
    hu_hight_alert=db.Column(db.String)
    hu_low_aleret=db.Column(db.String)
    sensor_name=db.Column(db.String)
    tmandhus = db.relationship('TmAndHu', backref='Nodes', lazy='dynamic')
    @property
    def serialize(self):
        return {
        'api_key':self.api_key,
        'mac':self.mac,
        
        
        
        }
   
    def __init__(self,
                api_key='',
                mac='',
                
                temp_hight_alert='',
                temp_low_alert='',
                hu_hight_alert='',
                hu_low_aleret='',
                sensor_name=''):
        self.api_key
        self.mac
       
        self.temp_hight_alert
        self.temp_low_alert
        self.hu_hight_alert
        self.hu_low_aleret
        self.sensor_name
    def __repr__(self):
        return '<Nodes id={},mac={},sensor_name={}'.format(self.id,self.mac,self.sensor_name)

class TmAndHu(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    n_mac = db.Column(db.String, db.ForeignKey("Nodes.mac"))
    tm = db.Column(db.String)
    hu = db.Column(db.String)
    dateTime=db.Column(db.DateTime)
    nodess = relationship("Nodes", backref="tmandhu")
    def __repr__(self):
        return f"TmAndHu id=('{self.id} temperature = {self.tm}')"
    @property
    def serialize(self):
        return {
        'n_mac':self.n_mac,
        'tm':self.tm,
        'hu':self.hu,
        'dateTime':self.dateTime}
class Node_SetUp(db.Model):
    __tablename__="Node_SetUp"
    id = db.Column(db.Integer,primary_key=True,unique=True)
    node = db.Column(db.String,unique=True)
    mac = db.Column(db.String,unique=True)    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    bu_id = db.Column(db.Integer, db.ForeignKey('businessunit.id'))
    businessunits = relationship("BusinessUnit",backref="Node_SetUp")
    temp_hight_alert=db.Column(db.String)
    temp_low_alert=db.Column(db.String)
    hu_hight_alert=db.Column(db.String)
    hu_low_aleret=db.Column(db.String)
    sensor_name=db.Column(db.String,unique=True)
    Temp_data = db.relationship('Temp_data', backref='Node_SetUp', lazy='dynamic')
    time_alert = db.Column(db.String)
    @property
    def serialize(self):
        return {
        'node':self.node,
        'mac':self.mac,
        }
   
    def __init__(self,
                node='',
                mac='',                
                temp_hight_alert='',
                temp_low_alert='',
                hu_hight_alert='',
                hu_low_aleret='',
                sensor_name='',
                time_alert=''):
        self.node=node
        self.mac=mac       
        self.temp_hight_alert =temp_hight_alert
        self.temp_low_alert   =temp_low_alert
        self.hu_hight_alert   =hu_hight_alert
        self.hu_low_aleret    =hu_low_aleret
        self.sensor_name      =sensor_name
        self.time_alert       =time_alert
    def __repr__(self):
        return '<Nodes id={},mac={},node={}'.format(self.id,self.mac,self.node)

class Temp_data(db.Model):
    __tablename__="Temp_data"
    id                   = db.Column(db.Integer,primary_key=True)
    # manserv_id           = db.Column(db.Integer,db.ForeignKey("Node_SetUp.id"))
    node_name1    = db.Column(db.String, db.ForeignKey('Node_SetUp.node'))
    temperature          = db.Column(db.String)
    humidity             = db.Column(db.String)
    dateTime             = db.Column(db.DateTime,nullable=False,  default=datetime.datetime.now(tz))
    h_temp               = db.Column(db.String)
    l_temp               = db.Column(db.String)
    h_hu                 = db.Column(db.String)
    l_hu                 = db.Column(db.String)
    ab_temp              = db.Column(db.String)
    ab_hu                = db.Column(db.String)
    @property
    def serialize(self):
        return {
        'dateTime':self.dateTime,
        'humidity':self.humidity,
        'node_name1':self.node_name1,
        'temperature':self.temperature
        
        
        }
   
    
    def __repr__(self):
        return f"Temp_data id=('{self.id} temperature = {self.temperature}')"
    def __init__(self,dateTime=''
                ,humidity=''
                ,node_name1=''
                ,temperature=''
                ,h_temp=''
                ,l_temp=''
                ,h_hu=''
                ,l_hu=''
                ,ab_temp=''
                ,ab_hu=''):
            self.dateTime=datetime.datetime.now(tz)
            self.humidity=humidity
            self.node_name1=node_name1
            self.temperature=temperature 
            self.h_temp=h_temp
            self.l_temp=l_temp
            self.h_hu=h_hu
            self.l_hu=l_hu
            self.ab_temp = ab_temp
            self.ab_hu   = ab_hu            
            
           
           

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


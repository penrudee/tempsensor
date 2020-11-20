from app import app
from flask_login import login_user, logout_user, current_user, login_required
from flask import make_response,render_template, flash, redirect, url_for, request, jsonify, g, Response
from app.forms import LoginForm, RegistrationForm,EditProfileForm, \
    ResetPasswordRequestForm,ResetPasswordForm,EmptyForm,NodeForm
from werkzeug.urls import url_parse
from app import db
from app.models import User,Edit,BusinessUnit,Node,Edit_node,Nodes,TmAndHu,Node_SetUp,Temp_data
from io import TextIOWrapper
from PIL import Image
from functools import wraps
from flask import send_from_directory, make_response, abort
from app.email import send_password_reset_email,send_password_reset_email,send_email,send_email_alert
from bs4 import BeautifulSoup as bp
from config import Config
from flask_wtf.csrf import CSRFProtect
from app.timer import Timer
# from parinya import LINE
from songline import Sendline
import datetime
import folium
import unicodedata
import random
import json
import requests
import os
import csv
import pytz
import pdfkit
import schedule



csrf = CSRFProtect(app)
tz=pytz.timezone('Asia/Bangkok')




def save_avatar(pic):
    form = EditProfileForm()
    pic_name= pic.filename
    
    image_path = os.path.join(app.root_path, 'static/avatar',pic_name )
    i = Image.open(pic)
    i.save(image_path)
    return pic_name

def save_image_node(image_node):
    form=NodeForm()
    p_name= image_node.filename
    
    image_path = os.path.join(app.root_path, 'static\image_node',p_name )
    i = Image.open(image_node)
    i.save(image_path)
    return p_name

def save_image(pic):
    form=EmptyForm()
    p_name= pic.filename
    
    image_path = os.path.join(app.root_path, 'static/images/pic',p_name )
    i = Image.open(pic)
    i.save(image_path)
    return p_name


def addData(dateTime,humidity,node_name1,temperature):
    m = Node_SetUp.query.filter_by(node=node_name1).first()   
    h_temp_alert = m.temp_hight_alert
    l_temp_alert = m.temp_low_alert
    h_hu_alert   = m.hu_hight_alert
    l_hu_alert   = m.hu_low_aleret
    if m.node == node_name1:
        
        if temperature > float(h_temp_alert) and humidity > float(h_hu_alert):

            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
           
            db.session.add(Nodes)
            db.session.commit()
        elif temperature > float(h_temp_alert) and float(h_hu_alert) > humidity > float(l_hu_alert) :
            
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            
            db.session.add(Nodes)
            db.session.commit()

        elif temperature > float(h_temp_alert) and float(l_hu_alert) > humidity:
           
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            Nodes.ab_hu             = humidity
            
            db.session.add(Nodes)
            db.session.commit()

        elif float(l_temp_alert) > temperature and float(l_hu_alert) > humidity:
           
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            Nodes.ab_hu             = humidity
            
            db.session.add(Nodes)
            db.session.commit()
        
        elif float(l_temp_alert) > temperature and float(h_hu_alert) > humidity > float(l_hu_alert):
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            
            
            db.session.add(Nodes)
            db.session.commit()
        elif float(l_temp_alert) > temperature and humidity > float(h_hu_alert):
           
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            Nodes.ab_hu             = humidity
            
            db.session.add(Nodes)
            db.session.commit()
        
        else:
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            
            db.session.add(Nodes)
            db.session.commit()
        return jsonify(Temp_data=Nodes.serialize)
    else:
        Nodes = Node_SetUp(node=node_name1)
        db.session.add(Nodes)
        db.session.flush()

        
        if temperature > float(h_temp_alert) and humidity > float(h_hu_alert):

            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
           
            db.session.add(Nodes)
            db.session.commit()
        elif temperature > float(h_temp_alert) and float(h_hu_alert) > humidity > float(l_hu_alert) :
            
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            
            db.session.add(Nodes)
            db.session.commit()

        elif temperature > float(h_temp_alert) and float(l_hu_alert) > humidity:
           
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            Nodes.ab_hu             = humidity
            
            db.session.add(Nodes)
            db.session.commit()

        elif float(l_temp_alert) > temperature and float(l_hu_alert) > humidity:
           
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            Nodes.ab_hu             = humidity
            
            db.session.add(Nodes)
            db.session.commit()
        
        elif float(l_temp_alert) > temperature and float(h_hu_alert) > humidity > float(l_hu_alert):
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            
            
            db.session.add(Nodes)
            db.session.commit()
        elif float(l_temp_alert) > temperature and humidity > float(h_hu_alert):
           
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            Nodes.ab_temp           = temperature
            Nodes.ab_hu             = humidity
            
            db.session.add(Nodes)
            db.session.commit()
        
        else:
            Nodes                   = Temp_data()
            Nodes.dateTime          = datetime.datetime.now(tz)
            Nodes.humidity          = humidity
            Nodes.node_name1 = node_name1
            Nodes.temperature       = temperature
            
            db.session.add(Nodes)
            db.session.commit()
        
        return jsonify(Temp_data=Nodes.serialize)



class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)
@app.route("/api2",methods=['GET','POST'])
# def write_data_point2(temperature,humidity,node):
# @csrf.exempt
def write_data_point2():
    ''''
         10 นาที = 2 จุด
         15 นาที = 3 จุด
         20 นาที = 4 จุด
         25 นาที = 5 จุด
         30 นาที = 6 จุด
    '''
# กำหนดตัวแปรจำนวนจุด conti = Continuously
    content = request.get_json()
    
    temperature       = content['temperature']
    humidity          = content['humidity']
    node_name1 = content['node']
    dateTime          = content['dateTime']
    print(f'temp={temperature}')
    print(f'hu={humidity}')
    print(f'node={node_name1}')
    print(f'dateTime ={dateTime}')
    nodes = Node_SetUp.query.filter_by(node=node_name1)
    
    
    len_ab_temp=[]
    no_de=node_name1
    for n in nodes:
        time_alert = int(n.time_alert) #เวลาเป็นาทีที่เลือกให้เตือน
        print(f'time_alert ={time_alert}, type = {type(time_alert)}')
        count = time_alert / 5
        int_count=int(count)
        print(f'int_count ={int_count}, type = {type(int_count)}')
        t_h_alert = n.temp_hight_alert
        t_l_alert = n.temp_low_alert
        # temp = Temp_data.query.filter_by(node_name1=n.node).order_by(Temp_data.id.desc())
        e = n.staff.email.split(",")   #แบ่งอีเมลของแต่ละคนออกมาเป็น list
        
        now = datetime.datetime.now()
        min_time_alert = datetime.timedelta(minutes=time_alert)
        print(f'now = {now}')
        print(f'min_time_alert = {min_time_alert}')
        diff_time = (now - min_time_alert)
        print(f'diff_time = {diff_time}')
        email = e
        user  =n.staff.username  
        try:     
            temp = Temp_data.query.filter(Temp_data.dateTime >= diff_time).filter(Temp_data.dateTime <= now)
            for t in temp:
                last_ab_temp=t.ab_temp[-1]
                messenger = Sendline(token)
                print(f'n.node={node_name1}')
                messenger.sendtext(f'อุณหภูมิของ {node_name1} ขณะนี้เท่ากับ {t.ab_temp} องศาเซลเซียส กรุณาตรวจสอบ')
            # for t in temp:
            #     print(f't.ab_temp = {t.ab_temp}:{len(t.ab_temp)}')
            #     print(len(t.ab_temp))
                # if len(t.ab_temp) >= count:
                #     print(f't.ab_temp = {t.ab_temp}')
                #     send_email_alert(email,user,no_de,t.ab_temp)
                # else:
                #     print('No No No')
                
        except:
            pass
        
            



        
        # send_email_alert(email,user,no_de,tempss)  
            
        
    return addData(dateTime,humidity,node_name1,temperature)
    

@app.route('/')
@app.route('/index')
@login_required
def index():
    s = BusinessUnit.query.all()
    q = Node.query.all()
    page = request.args.get( 'page', 1, type=int)
    posts = Node.query.order_by(Node.id.desc()).paginate(page, 20, False)
    
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html',
                           title='Index',
                           q=posts.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           s=s
                          )




@app.route("/temperature_chart/<string:node>")
def temperature_chart(node):
    legend = 'Temperatures'
    hight_limit ="Hight Level"
    low_limit = "Low Level"
    AbnormalTemperature = "Abnormal Temperature"
    q = Temp_data.query.filter_by(node_name1=node)
    nd = Node_SetUp.query.filter_by(node=node)
    for n in nd:
        t = Temp_data.query.filter_by(node_name1=n.node).order_by(Temp_data.id.desc()).first()
        print(f'temperature = t.temperature')
    L=Node_SetUp.query.filter_by(node=node)
    hlimit=[]
    lowlimit_dataset=[]
    temperatures = []    
    times=[]
    humidity=[]
    ab_temperature= []
    ab_humidity = []
    for qq in q:
        temperatures.append(qq.temperature)
        humidity.append(qq.humidity)
        times.append(qq.dateTime)
        
        ab_temperature.append(qq.ab_temp)
        ab_humidity.append(qq.ab_hu)
    print(f'ab_temp={ab_temperature}')
    for ll in L:
        y = ll.temp_hight_alert
        hlimit_dataset=[y for i in temperatures ]

    for ll2 in L:
        y2 = ll2.temp_low_alert
        lowlimit_dataset=[y2 for i in temperatures ]       
    return render_template('time_chart.html',
                           q=q,
                           nd=nd, 
                           values=temperatures,
                           values2=humidity,
                           values3=ab_temperature,
                           labels=times, 
                           legend=legend,
                           hight_limit=hight_limit,
                           low_limit=low_limit,
                           hlimit=hlimit_dataset,
                           lowlimit=lowlimit_dataset,
                           Temp_data=Temp_data,
                           AbnormalTemperature=AbnormalTemperature,
                           title="Temperature and Humidity Chart")

@app.route("/time_chart/<string:mac>")
def time_chart(mac):
    legend = 'Temperatures'
    hight_limit ="Hight Level"
    low_limit = "Low Level"
    q = TmAndHu.query.filter_by(n_mac=mac)
    nd = Nodes.query.filter_by(mac=mac).first()
    L=Nodes.query.filter_by(mac=mac)
    hlimit=[]
    lowlimit_dataset=[]
    temperatures = []    
    times=[]
    humidity=[]
    for qq in q:
        temperatures.append(qq.tm)
        humidity.append(qq.hu)
        times.append(qq.dateTime)
        
    for ll in L:
        y = ll.temp_hight_alert
        hlimit_dataset=[y for i in temperatures ]

    for ll2 in L:
        y2 = ll2.temp_low_alert
        lowlimit_dataset=[y2 for i in temperatures ]       
    return render_template('time_chart.html',
                           q=q,
                           nd=nd, 
                           values=temperatures,
                           values2=humidity,
                           labels=times, 
                           legend=legend,
                           hight_limit=hight_limit,
                           low_limit=low_limit,
                           hlimit=hlimit_dataset,
                           lowlimit=lowlimit_dataset,
                           title="Temperature and Humidity Chart")



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


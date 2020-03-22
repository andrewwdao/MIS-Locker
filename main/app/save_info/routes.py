"""------------------------------------------------------------*-
  Route module for the saveInfo Server.
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Miguel Grinberg 2018
  version 1.30 - 19/10/2019
 --------------------------------------------------------------
 *  html routes for functions of the server
 *
 --------------------------------------------------------------"""
from flask import render_template, flash, redirect, url_for, request
from app import saveInfo_app, db
from app.save_info.forms import InfoForm
from app.models import User
import subprocess as subpro

def __readwrite():
    subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
    
def __readonly():
    db.session.close() # need to this everytime you alter the db
    subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro

def shutdownServer():
    # Start shutting down server
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@saveInfo_app.route('/', methods=['GET', 'POST'])
@saveInfo_app.route('/index', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        __readwrite()
        user = User.query.filter_by(mssv=form.mssv.data).first()
        if user is None:
            newUser = User.query.order_by(User.timestamp.desc()).first()  # get the lastest user out
            print('Hello')
            newUser.name = form.name.data
            newUser.mssv = form.mssv.data
            db.session.commit()
        __readonly()
        return redirect(url_for('gotInfo'))
    templateData = {
        'server_title': 'MIS Locker',
        'main_title': 'MIS Locker System',
        'main_func': 'Add Guest ID',
        'form': form
    }
    return render_template('save_info/index.html', **templateData)


@saveInfo_app.route('/gotinfo', methods=['GET', 'POST'])
def gotInfo():
    __readwrite()
    user = User.query.order_by(User.timestamp.desc()).first()  # get the lastest user out
    __readonly()
    templateData = {
        'server_title': 'MIS Locker',
        'main_title': 'MIS Locker System',
        'main_func': 'Information received',
        'user_name': user.name,
        'user_id': user.mssv
    }
    # Start shutting down server
    shutdownServer()
    return render_template('save_info/gotInfo.html', **templateData)


@saveInfo_app.route('/shutdown')
def shutdown():
    templateData = {
        'server_title': 'MIS Locker',
        'main_title': 'MIS Locker System',
        'main_func': 'Service closing...',
    }
    # Start shutting down server
    shutdownServer()
    return render_template('shutdown.html', **templateData)


@saveInfo_app.route('/about')
def about():
    return render_template('about.html')

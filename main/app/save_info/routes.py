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
import os
import signal
from database import Database
import subprocess as subpro

# shutdown production server
def shutdownServer():
    print('Prepare to shutting down server...')
    # we want to do this, but in a little delay, so do it in a separate thread
    # os.kill(int(os.getpid()),signal.SIGTERM) # find out the current task it's running on, then kill it
    subpro.Popen(['sudo','python3','shutdown-server.py',str(os.getpid())], shell=False) # send the pid of the current webserver and send signal to kill it
    

# ======================== for development only =====================
# def shutdownServer():
#     # Start shutting down server
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()
# ===================================================================


@saveInfo_app.route('/', methods=['GET', 'POST'])
@saveInfo_app.route('/index', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mssv=form.mssv.data).first()
        if user is None:
            newUser = User.query.order_by(User.id.desc()).first()  # get the lastest user out
            newUser.name = form.name.data
            newUser.mssv = form.mssv.data
            db.session.commit()
        db.session.close() # need to this everytime you alter the db
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
    user = User.query.order_by(User.id.desc()).first()  # get the lastest user out
    templateData = {
        'server_title': 'MIS Locker',
        'main_title': 'MIS Locker System',
        'main_func': 'Information received',
        'user_name': user.name,
        'user_id': user.mssv
    }
    db.session.close() # need to this everytime you alter the db
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
    # incomplete member delete is handled on main
    # Start shutting down server
    shutdownServer()
    return render_template('shutdown.html', **templateData)


@saveInfo_app.route('/about')
def about():
    return render_template('about.html')

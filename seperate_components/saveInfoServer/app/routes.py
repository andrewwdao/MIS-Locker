from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import InfoForm
from app.models import User


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mssv=form.mssv.data).first()
        if user is None :
            newUser = User(name=form.name.data, mssv=form.mssv.data)
            db.session.add(newUser)
            db.session.commit()
            flash('Information received:\r\nName: {}\r\nID (MSSV): {}'.format(
                   form.name.data, form.mssv.data))
        return redirect(url_for('index'))
    templateData = {
        'server_title': 'MIS Locker System',
        'server_func': 'Add Guest ID',
        'form': form
    }
    return render_template('index.html', **templateData)


@app.route('/about')
def about():
    return render_template('about.html')


# if __name__ == "__main__":
# app.run(host='0.0.0.0', port=7497, debug=True)

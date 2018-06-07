from blog2.model.User import User
from blog2.model.Category import Category
import os

from blog2 import app,db
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g

@app.route('/')
def show_entries():
    categorys = Category.query.paginate(1, 4, False).items#分页
    # page = request.args.get('page', 1, type=int)
    return render_template('show_entries.html',entries=categorys)

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    content = request.form['text']
    category = Category(title,content)
    db.session.add(category)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/toregist')
def toregist():
    flash('hi')
    return render_template('regist.html')

@app.route('/regist',methods=['GET','POST'])
def regist():
    username = request.form['username']
    password = request.form['password']
    user = User(username,password)
    db.session.add(user)
    db.session.commit()
    flash('regist successfully')
    error = 'success!'
    return render_template('login.html', error=error)

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username,password=password).first()

        if user is None:
            error = 'Invalid username'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# @app.route('/userManage_admin', methods=['GET', 'POST'])
# def userManage_admin():
#     page = request.args.get('page', 1, type=int)
#         pagination = User.query.filter_by(user_role=0).paginate(page, per_page=current_app.config[
#             'FLASKY_POSTS_PER_PAGE'], error_out=False)
#         usrs = pagination.items
#         return render_template('userManage_admin.html',usrs=usrs, pagination = pagination )

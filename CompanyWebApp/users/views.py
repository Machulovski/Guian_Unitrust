#users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from CompanyWebApp import db
from CompanyWebApp.models import User, BlogPost
from CompanyWebApp.users.forms import  RegistrationForm, LoginForm, UpdateUserForm
from CompanyWebApp.users.picture_handler import add_profile_pic
  
users = Blueprint('users', __name__)
 
#REGISTRATION
@users.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,user_dep='外部', user_level='普通用户', admin=False, password=form.password.data, )

        db.session.add(user)
        db.session.commit()
        flash('感谢注册!')
        return redirect(url_for('users.login'))
    
    return render_template('user_register.html', form=form)

#LOGIN
@users.route('/login', methods=['POST','GET'])
def login():
    
    form = LoginForm()
    
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        
        if  user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('登录成功!')
            #IMPORTANT NEXT
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)

    return render_template('user_login.html', form = form)

#LOGOUT
@users.route('/logout')
def logout():
    logout_user()
    flash('用户已登出!')
    return redirect(url_for('core.index'))

#ACCOUNT (update UserForm) //// maybe need to change to account/<user_id>
@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            # GRAB THE NEW IMAGE TO UPDATE profile_image
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.user_dep = form.department.data
        current_user.user_level = form.level.data
        current_user.admin = form.admin.data

        db.session.commit()
        flash('用户信息成功更新!')

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.department.data = current_user.user_dep
        form.level.data = current_user.user_level
        form.admin.data = current_user.admin
    
    profile_image = url_for('static', filename= 'profile_pics/'+current_user.profile_image)

    return render_template('user_account.html', profile_image= profile_image, form=form)

#USER POST LIST VIEW
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('user_blog_posts.html', blog_posts = blog_posts, user= user )

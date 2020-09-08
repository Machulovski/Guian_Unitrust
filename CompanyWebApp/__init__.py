#CompanyWebApp/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from flask_restful import Resource, Api

app = Flask(__name__)

#RESTFUL SETUP
api = Api(app)
from CompanyWebApp.irr_calculators.crudapi import PuppyNames, AllNames
api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames,'/puppies')

#FORM SECRETKEY SETUP
app.config['SECRET_KEY'] = 'mysecret'

#DATABASE SETUP
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

#LOGIN CONFIG
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

#BLUEPRINTS
from CompanyWebApp.core.views import core
from CompanyWebApp.error_pages.handlers import error_pages
from CompanyWebApp.users.views import users
from CompanyWebApp.irr_calculators.views import irr_calculators
from CompanyWebApp.blog_posts.views import blog_posts

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(irr_calculators)
app.register_blueprint(blog_posts)
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

LOCAL_DB = 'sqlite:///data.db'
REMOTE_DB_ENV_VAR = 'DATABASE_URL' # env variable defined by heroku

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(REMOTE_DB_ENV_VAR, LOCAL_DB) 
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'blabla'

api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, '/item/<string:name>') 	# http://127.0.0.1:5000/item/product1
api.add_resource(ItemList, '/items') 			# http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)
import sqlite3, status
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

MSG_ITEM_ALREADY_EXISTS = 'item already exists in database.'
MSG_ITEM_DOES_NOT_EXIST = 'item does not exist in database.'
MSG_ITEM_DELETED = 'item deleted successfuly.'
MSG_NO_ITEM_FOUND = 'item not found.'

MSG_INSERT_EXCEPTION = 'An error occurred inserting the item.'
MSG_UPDATE_EXCEPTION = 'An error occurred updating the item.'
MSG_DELETE_EXCEPTION = 'An error occurred deleting the item.'

class ItemList(Resource):
	def get(self):
		return ItemModel.get_all_items()

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', 
		type=float, 
		required=True,
		help="This field cannot be left blank!"
	)
	parser.add_argument('store_id', 
		type=int, 
		required=True,
		help="Every item needs a store id"
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json(), status.OK
		return {'message': MSG_NO_ITEM_FOUND}, status.NOT_FOUND

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': MSG_ITEM_ALREADY_EXISTS}, status.BAD_REQUEST
		
		data = Item.parser.parse_args();
		item = ItemModel(name, **data)
		
		try:	
			item.save_to_db()
		except:
			return {"message": MSG_INSERT_EXCEPTION}, status.INTERNAL_SERVER_ERROR
		
		return item.json(), status.CREATED

	def put(self, name):
		data = Item.parser.parse_args();

		item = ItemModel.find_by_name(name)		

		if item is None:
			item = ItemModel(name, **data)
		else:
			item.price = data['price']

		try:
			item.save_to_db()
		except:
			return {"message": MSG_UPDATE_EXCEPTION}, status.INTERNAL_SERVER_ERROR			
		
		return item.json()

	def delete(self, name):

		item = ItemModel.find_by_name(name)
		if item is None:
			return {'message': MSG_ITEM_DOES_NOT_EXIST}, status.BAD_REQUEST

		try:
			item.delete_from_db()
		except:
			return {"message": MSG_DELETE_EXCEPTION}, status.INTERNAL_SERVER_ERROR	
		
		return {'message': MSG_ITEM_DELETED}
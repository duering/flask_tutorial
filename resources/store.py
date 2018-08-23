from flask_restful import Resource
from models.store import StoreModel

import status

class Store(Resource):
	MSG_STORE_ALREADY_EXISTS = 'store already exists in database.'
	MSG_STORE_DELETED = 'store deleted successfuly.'
	MSG_NO_STORE_FOUND = 'store not found.'
	MSG_INSERT_EXCEPTION = 'An error occurred inserting the item.'

	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json(), status.OK
		return {'message': self.MSG_NO_STORE_FOUND}, status.NOT_FOUND

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': self.MSG_STORE_ALREADY_EXISTS}, status.BAD_REQUEST

		store = StoreModel(name)

		try:
			store.save_to_db()
		except:
			return {'message': self.MSG_INSERT_EXCEPTION}

		return store.json(), status.CREATED

	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store is None:
			return {'message': self.MSG_NO_STORE_FOUND}, status.BAD_REQUEST

		store.delete_from_db()
		return {'message': self.MSG_STORE_DELETED}

class StoreList(Resource):
	def get(self):
		return {'stores': StoreModel.all()}
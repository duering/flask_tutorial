import status, sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
	
	MSG_USER_ALREADY_EXIST = "User already exists."
	MSG_USER_CREATED = "User {0} was created."
	
	parser = reqparse.RequestParser()
	parser.add_argument('username', 
		type=str, 
		required=True,
		help="This field cannot be left blank!"
	)
	parser.add_argument('password', 
		type=str, 
		required=True,
		help="This field cannot be left blank!"
	)

	def post(self):
		data = UserRegister.parser.parse_args()
		user = UserModel.find_by_username(data['username'])
		if user:
			return {"message": self.MSG_USER_ALREADY_EXIST}, status.BAD_REQUEST

		user = UserModel(**data)
		user.save_to_db()

		return {"message": self.MSG_USER_CREATED.format(user.username)}, status.CREATED
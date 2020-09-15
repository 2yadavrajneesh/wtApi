from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class IntentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f'CreateIntent(name={name}, position={position}, experience={experience})'

# db.create_all()

intent_put_args = reqparse.RequestParser()
intent_put_args.add_argument("name", type=str, help="Name of Intents is Required", required=True)
intent_put_args.add_argument("position", type=str, help="Position of Intents is Required", required=True)
intent_put_args.add_argument("experience", type=int, help="Experience in year of Intents is Required", required=True)

intent_update_args = reqparse.RequestParser()
intent_update_args.add_argument("name", type=str, help="Name of Intents is Required")
intent_update_args.add_argument("position", type=str, help="Position of Intents is Required")
intent_update_args.add_argument("experience", type=int, help="Experience in year of Intents is Required")

resourse_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'position': fields.String,
    'experience': fields.Integer
}

class CreateIntent(Resource):
    @marshal_with(resourse_fields)
    def put(self, intent_id):
        args = intent_put_args.parse_args()
        result = IntentModel.query.filter_by(id=intent_id).first()
        if result:
            abort(409, message="Intent is Taken")
        intent = IntentModel(id= intent_id, name=args['name'], position=args['position'], experience=args['experience'])
        db.session.add(intent)
        db.session.commit()
        return intent, 201

class ListIntent(Resource):
    @marshal_with(resourse_fields)
    def get(self, intent_id):
        result = IntentModel.query.filter_by(id=intent_id).first()
        if not result:
            abort(404, message="Intent was not found")
        return result

class UpdateIntent(Resource):
    @marshal_with(resourse_fields)
    def patch(self, intent_id):
        args = intent_update_args.parse_args()
        result = IntentModel.query.filter_by(id=intent_id).first()
        if not result:
            abort(404, message="Intent was not found, can not update")

        if args['name']:
            result.name = args['name']
        if args['position']:
            result.position = args['position']
        if args['experience']:
            result.experience = args['experience']

        db.session.commit()
        return result

api.add_resource(CreateIntent, "/createintent/<int:intent_id>")
api.add_resource(ListIntent, "/listintent/<int:intent_id>")
api.add_resource(UpdateIntent, "/updateintent/<int:intent_id>")

if __name__ == "__main__":
    app.run(debug=True)

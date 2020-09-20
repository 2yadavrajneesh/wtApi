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
    intent_name = db.Column(db.String(50), nullable=False)
    intent_description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f'CreateIntent(name={intent_name}, position={intent_description})'

db.create_all()

intent_put_args = reqparse.RequestParser()
intent_put_args.add_argument("intent_name", type=str, help="Name of Intents is Required", required=True)
intent_put_args.add_argument("intent_description", type=str, help="Description of Intents is Required", required=True)

intent_update_args = reqparse.RequestParser()
intent_update_args.add_argument("intent_name", type=str, help="Name of Intents is Required")
intent_update_args.add_argument("intent_description", type=str, help="Description of Intents is Required")

resourse_fields = {
    'id': fields.Integer,
    'intent_name': fields.String,
    'intent_description': fields.String,
}

class CreateIntent(Resource):
    @marshal_with(resourse_fields)
    def put(self, intent_id):
        args = intent_put_args.parse_args()
        result = IntentModel.query.filter_by(id=intent_id).first()
        if result:
            abort(409, message="Intent is Taken")
        intent = IntentModel(id= intent_id, intent_name=args['intent_name'], intent_description=args['intent_description'])
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

        if args['intent_name']:
            result.name = args['intent_name']
        if args['intent_description']:
            result.position = args['intent_description']

        db.session.commit()
        return result

api.add_resource(CreateIntent, "/createintent/<int:intent_id>")
api.add_resource(ListIntent, "/listintent/<int:intent_id>")
api.add_resource(UpdateIntent, "/updateintent/<int:intent_id>")

if __name__ == "__main__":
    app.run(debug=True)
from flask_restful import Resource, abort, marshal_with

from model.intent_model import IntentModel, resourse_fields, intent_put_args, intent_update_args, db


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
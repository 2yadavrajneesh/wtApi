from flask_restful import reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from run import app

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
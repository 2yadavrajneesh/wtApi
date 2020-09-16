from flask import Flask
from flask_restful import Api
from resources.intent import CreateIntent, ListIntent, UpdateIntent

app = Flask(__name__)
api = Api(app)

api.add_resource(CreateIntent, "/createintent/<int:intent_id>")
api.add_resource(ListIntent, "/listintent/<int:intent_id>")
api.add_resource(UpdateIntent, "/updateintent/<int:intent_id>")

if __name__ == "__main__":
    app.run(debug=True)

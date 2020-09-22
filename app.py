from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import os
import shutil
import glob

basedir = os.path.abspath(os.path.dirname(__file__))

# Init app
app = Flask(__name__)
api = Api(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

#############################
## intents argument handle ##
#############################

class IntentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intent_name = db.Column(db.String(50), nullable=False)
    intent_description = db.Column(db.String(100), nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey("create_bot_model.id"), nullable=False)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f'CreateIntents(intent_name={intent_name}, intent_description={intent_description}, bot_id={bot_id})'


intent_put_args = reqparse.RequestParser()
intent_put_args.add_argument("intent_name", type=str, help="Name of Intents is Required", required=True)
intent_put_args.add_argument("intent_description", type=str, help="Description of Intents is Required", required=True)
intent_put_args.add_argument("bot_id", type=int, help="Bot id is Required", required=True)

intent_update_args = reqparse.RequestParser()
intent_update_args.add_argument("intent_name", type=str, help="Name of Intents is Required")
intent_update_args.add_argument("intent_description", type=str, help="Description of Intents is Required")
intent_update_args.add_argument("bot_id", type=int, help="Bot id is Required")

resources_fields_intent = {
    'id': fields.Integer,
    'intent_name': fields.String,
    'intent_description': fields.String,
    'bot_id': fields.Integer,
}


##############################
## stories arguments handle ##
##############################

class StoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_name = db.Column(db.String(50), nullable=False)
    intent_story = db.Column(db.String(100), nullable=False)
    action_name = db.Column(db.String(100), nullable=False)
    bot_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f'CreateStories(story_name={story_name}, intent_story={intent_story}, action_name={action_name}, bot_id={bot_id} )'


stories_put_args = reqparse.RequestParser()
stories_put_args.add_argument("story_name", type=str, help="Name of Stories is Required", required=True)
stories_put_args.add_argument("intent_story", type=str, help="Intent Should be Mapped to Stories", required=True)
stories_put_args.add_argument("action_name", type=str, help="Action Should be Mapped to Intents for a Story",
                              required=True)
stories_put_args.add_argument("bot_id", type=int, help="Action Should be Mapped to Intents for a Story", required=True)

stories_update_args = reqparse.RequestParser()
stories_update_args.add_argument("story_name", type=str, help="Name of Stories is Required")
stories_update_args.add_argument("intent_story", type=str, help="Intent Should be Mapped to Stories")
stories_update_args.add_argument("action_name", type=str, help="Action Should be Mapped to Intents for a Story")
stories_update_args.add_argument("bot_id", type=int, help="Action Should be Mapped to Intents for a Story")

resources_fields_story = {
    'id': fields.Integer,
    'story_name': fields.String,
    'intent_story': fields.String,
    'action_name': fields.String,
    'bot_id': fields.Integer,

}

##########################
## bot arguments handle ##
##########################

# class BotModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     bot_id = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         # return '<User %r>' % self.name
#         return f'TrainBot(bot_id={bot_id})'


class CreateBotModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f'CreateBot(bot_name={bot_name})'


bot_put_args_bot = reqparse.RequestParser()
bot_put_args_bot.add_argument("bot_name", type=str, help="Bot Name Required", required=True)

resources_fields_bot = {
    'bot_name': fields.String,
}


# Comment after first initialization
# db.create_all()


#########
# Views #
#########

class CreateIntents(Resource):
    @marshal_with(resources_fields_intent)
    def put(self, intent_id):
        args = intent_put_args.parse_args()
        result = IntentModel.query.filter_by(id=intent_id).first()
        if result:
            abort(409, message="Intent is Taken")
        intent = IntentModel(
            id=intent_id,
            intent_name=args['intent_name'],
            intent_description=args['intent_description'],
            bot_id=args['bot_id']
        )

        pathnlu = str(args['bot_id']) + "/nlu.md"  # 999/nlu.md

        print("Bot id is", args['bot_id'])
        if str(path.exists(pathnlu)):
            f = open(pathnlu, "a")
            f.write("* ")
            f.write(args['intent_name'])
            f.write("\n")
            f.write("-  ")
            f.write(args['intent_description'])
            f.close()
        else:
            abort(409, message="Bot Doesn't Exist")

        db.session.add(intent)
        db.session.commit()

        return intent, 201


class ListIntent(Resource):
    @marshal_with(resources_fields_intent)
    def get(self, intent_id):
        result = IntentModel.query.filter_by(id=intent_id).first()
        if not result:
            abort(404, message="Intent was not found")
        return result


class UpdateIntent(Resource):
    @marshal_with(resources_fields_intent)
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

class CreateStories(Resource):
    @marshal_with(resources_fields_story)
    def put(self, story_id):
        args = stories_put_args.parse_args()
        result = StoryModel.query.filter_by(id=story_id).first()
        if result:
            abort(409, message="Story is Taken")
        story = StoryModel(
            id=story_id,
            story_name=args['story_name'],
            intent_story=args['intent_story'],
            action_name=args['action_name'],
            bot_id=args['bot_id']
        )

        pathstories = str(args['bot_id']) + "/stories.md"  # 999/stories.md

        f = open(pathstories, "a")
        f.write("## ")
        f.write(args['story_name'])
        f.write("\n")
        f.write("-  ")
        f.write(args['action_name'])
        f.close()

        db.session.add(story)
        db.session.commit()
        return story, 201


class CreateBot(Resource):
    @marshal_with(resources_fields_bot)
    def put(self, bot_id):
        args = bot_put_args_bot.parse_args()

        result = CreateBotModel.query.filter_by(id=bot_id).first()

        if result:
            abort(409, message="Bot is Taken")

        bot = CreateBotModel(id=bot_id, bot_name=args['bot_name'])

        db.session.add(bot)
        db.session.commit()

        dirName = str(bot.bot_name)

        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")

            # sample_bot = os.path.dirname('./sample_bot')
            for filename in glob.glob(os.path.join("sample_bot", '*.*')):
                shutil.copy(filename, dirName)

            # source_dir = 'sample_bot'
            #
            # file_names = os.listdir(source_dir)
            #
            # for file_name in file_names:
            #     shutil.copy(os.path.join(source_dir, file_name), dirName)

        except FileExistsError:
            print("Directory ", dirName, " already exists")

        return bot, 201


# class TrainBot(Resource):
#     @marshal_with(resources_fields_bot)
#     def post(self, bot_id):
#         result = BotModel.query.filter_by(bot_id=bot_id).first()
#         if not result:
#             abort(404, message="Bot Not Found")
#
#         os.system('cmd /c "rasa train"')
#
#         # train for particular bot
#         return result


# Add logic to deploy bot , execute rasa shell or rasa --endpoint

api.add_resource(CreateBot, "/createbot/<int:bot_id>")
api.add_resource(CreateIntents, "/createintents/<int:intent_id>")
api.add_resource(CreateStories, "/createstories/<int:story_id>")

# api.add_resource(TrainBot, "/trainbot/<int:bot_id>")

api.add_resource(ListIntent, "/listintents/<int:intent_id>")
api.add_resource(UpdateIntent, "/updateintent/<int:intent_id>")

# Add logic to deploy bot action, rasa --endpoint for the new bot or specific id
# foreach bot actions and endpoints

# api.add_resource(DeployBot, "/deploybot/<int:intent_id>")


# Run Server
if __name__ == '__main__':
    app.run(debug=True)

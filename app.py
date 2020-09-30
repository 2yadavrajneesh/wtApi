import subprocess
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
    bot_id = db.Column(db.Integer, db.ForeignKey("bot_model.id"), nullable=False)

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
    intent_id = db.Column(db.Integer, db.ForeignKey("intent_model.id"), nullable=False)
    action_name = db.Column(db.String(100), nullable=False)
    action_reply = db.Column(db.String(500), nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey("bot_model.id"), nullable=False)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f'CreateStories(story_name={story_name}, intent_id={intent_id}, action_name={action_name}, bot_id={bot_id} )'


stories_put_args = reqparse.RequestParser()
stories_put_args.add_argument("story_name", type=str, help="Name of Stories is Required", required=True)
stories_put_args.add_argument("intent_id", type=int, help="Intent Should be Mapped to Stories", required=True)
stories_put_args.add_argument("action_name", type=str, help="Action Should be Mapped to Intents for a Story",
                              required=True)
stories_put_args.add_argument("action_reply", type=str, help="Action Should be Mapped to Intents for a Story",
                              required=True)
stories_put_args.add_argument("bot_id", type=int, help="Action Should be Mapped to Intents for a Story", required=True)

stories_update_args = reqparse.RequestParser()
stories_update_args.add_argument("story_name", type=str, help="Name of Stories is Required")
stories_update_args.add_argument("intent_id", type=int, help="Intent Should be Mapped to Stories")
stories_update_args.add_argument("action_name", type=str, help="Action Should be Mapped to Intents for a Story")
stories_update_args.add_argument("action_reply", type=str, help="Action Should be Mapped to Intents for a Story")
stories_update_args.add_argument("bot_id", type=int, help="Action Should be Mapped to Intents for a Story")

resources_fields_story = {
    'id': fields.Integer,
    'story_name': fields.String,
    'intent_id': fields.Integer,
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


class BotModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        # return '<User %r>' % self.name
        return f'CreateBot(bot_name={bot_name})'


bot_put_args_bot = reqparse.RequestParser()
bot_put_args_bot.add_argument("bot_name", type=str, help="Bot Name Required", required=True)

bot_post_args_bot = reqparse.RequestParser()
bot_post_args_bot.add_argument("bot_name", type=str, help="Bot Name Required", required=True)

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

        bot_i = BotModel.query.filter_by(id=intent.bot_id).first()
        bot_name = bot_i.bot_name

        try:
            pathnlu = bot_name + "/data/nlu.md"
            print("Bot id is", args['bot_id'])
            if str(os.path.exists(pathnlu)):
                f = open(pathnlu, "a")
                f.write("\n")
                f.write("## intent:")
                f.write(intent.intent_name)
                f.write("\n")
                f.write("- ")
                f.write(intent.intent_description)
                f.close()
                print("Intent ", intent.intent_name, " Created ")
            else:
                print("Unable to Create Intent")

        except FileExistsError:
            print("Bot ", intent.bot_id, " Doesn't Exist")

        dpathstories = bot_name + "/domain.yml"

        try:
            if str(os.path.exists(dpathstories)):
                f = open(dpathstories, "a")

                f.write("\n")
                f.write("intent:")
                f.write("\n")
                f.write("  - ")
                f.write(intent.intent_name)
                f.write("\n")
                f.close()

                print("Intent ", intent.intent_name, " is Registered")
            else:
                print("Unable to Register Intent")

        except FileNotFoundError:
            print("File Not Found")

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
            result.intent_name = args['intent_name']
        if args['intent_description']:
            result.intent_description = args['intent_description']

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
            intent_id=args['intent_id'],
            action_name=args['action_name'],
            action_reply=args['action_reply'],
            bot_id=args['bot_id']
        )
        bot_i = BotModel.query.filter_by(id=story.bot_id).first()
        bot_name = bot_i.bot_name
        print("Bot id is", args['bot_id'])
        pathstories = bot_name + "/data/stories.md"
        intent_i = IntentModel.query.filter_by(id=story.intent_id).first()
        intent_name = intent_i.intent_name
        try:
            if str(os.path.exists(pathstories)):
                f = open(pathstories, "a")
                f.write("\n")
                f.write("## ")
                f.write(story.story_name)
                f.write("\n")
                f.write("* ")
                f.write(intent_name)
                f.write("\n")
                f.write("  - ")
                f.write(story.action_name)
                f.close()
                print("Story ", story.story_name, " Created ")
            else:
                print("Unable to Create Story")

        except FileExistsError:
            print("Bot ", story.bot_id, " Doesn't Exist")

        dpathstories = bot_name + "/domain.yml"

        try:
            if str(os.path.exists(dpathstories)):
                f = open(dpathstories, "a")
                f.write("\n")
                f.write("responses:")
                f.write("\n")
                f.write("  ")
                f.write(story.action_name)
                f.write(":")
                f.write("\n")
                f.write("  - text: ")
                f.write(story.action_reply)
                f.close()
                print("Story ", story.story_name, " is Register")
            else:
                print("Unable to Register Story")

        except FileNotFoundError:
            print("File not Found")

        db.session.add(story)
        db.session.commit()
        return story, 201


class CreateBot(Resource):
    @marshal_with(resources_fields_bot)
    def put(self, bot_id):
        args = bot_put_args_bot.parse_args()

        result = BotModel.query.filter_by(id=bot_id).first()

        if result:
            abort(409, message="Bot is Taken")

        bot = BotModel(id=bot_id, bot_name=args['bot_name'])

        db.session.add(bot)
        db.session.commit()

        dirName = str(bot.bot_name)

        try:
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")

            for root, dirs, files in os.walk('sample_bot'):
                for file in files:
                    path_file = os.path.join(root, file)
                    shutil.copy2(path_file, dirName)

            directory = 'data'
            path = os.path.join(dirName, directory)
            os.mkdir(path)

            for filename in glob.glob(os.path.join(dirName, '*.md')):
                shutil.move(filename, path)

        except FileExistsError:
            print("Directory ", dirName, " already exists")

        return bot, 201


class TrainBot(Resource):
    @marshal_with(resources_fields_bot)
    def post(self, bot_id):
        args = bot_post_args_bot.parse_args()
        result = BotModel.query.filter_by(id=bot_id).first()
        if not result:
            abort(404, message="Bot Not Found")

        bot = BotModel(id=bot_id, bot_name=args['bot_name'])

        dirName = str(bot.bot_name)

        try:
            subprocess.call('rasa train', shell=True, cwd=dirName)

        except FileNotFoundError:
            print("Directory ", dirName, " doesn't found")

        return result


class DeployBot(Resource):
    @marshal_with(resources_fields_bot)
    def post(self, bot_id):
        args = bot_post_args_bot.parse_args()
        result = BotModel.query.filter_by(id=bot_id).first()
        if not result:
            abort(404, message="Bot Not Found")

        bot = BotModel(id=bot_id, bot_name=args['bot_name'])

        dirName = str(bot.bot_name)

        try:
            subprocess.call('rasa actions', shell=True, cwd=dirName)

        except FileNotFoundError:
            print("Directory ", dirName, " doesn't found")

        return result


api.add_resource(CreateBot, "/createbot/<int:bot_id>")
api.add_resource(CreateIntents, "/createintents/<int:intent_id>")
api.add_resource(CreateStories, "/createstories/<int:story_id>")

api.add_resource(TrainBot, "/trainbot/<int:bot_id>")
api.add_resource(DeployBot, "/deploybot/<int:bot_id>")

api.add_resource(ListIntent, "/listintent/<int:intent_id>")
api.add_resource(UpdateIntent, "/updateintent/<int:intent_id>")


# Run Server
if __name__ == '__main__':
    app.run(debug=True)

import json

class User:

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.name = 'unknown'
        self.age = 0
        self.last_question = 0

    def get_as_json(self):
        return json.dumps({'name': self.name, 'age': self.age})

def create_user_from_json(chat_id, user_as_json):
    user_deserialised = json.loads(user_as_json)
    new_user = User(chat_id)
    new_user.name = user_deserialised['name']
    new_user.age = user_deserialised['age']
    return new_user

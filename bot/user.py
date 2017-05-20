import json
from questions import questions

class User:

    def __init__(self, chat_id):
        self.values = {}
        for key in questions.keys():
            self.values[key] = False
        self.chat_id = chat_id
        self.last_question = 0

    def get_as_json(self):
        self.values['last_question'] = self.last_question
        return json.dumps(self.values)

    def answer_question(self, data):
        self.values[self.last_question] = data

    def next_question(self):
        for key, value in self.values.items():
            if not value:
                return key

def create_user_from_json(chat_id, user_as_json):
    user_deserialised = json.loads(user_as_json)
    new_user = User(chat_id)
    for key in questions.keys():
        new_user.values[key] = user_deserialised[key]
    new_user.last_question = user_deserialised['last_question']
    return new_user


import json
from questions import questions
from institutions import institutions

class User:
    list_of_questions = questions
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

    def get_summary(self):
        summary = []
        for key, value in self.values.items():
            summary.append(str(key) + ': ' + str(value))
        return summary

    def get_summary_message(self):
        summary_list = self.get_summary()
        summary_message = ''
        for summary in summary_list:
            summary_message += summary + '\n'
        return summary_message


    def get_match(self):
        self.sanitize_inputs()
        for institution in institutions:
            is_match = []
            is_match.append(int(self.values['age']) < institution['age'])
            is_match.append(int(self.values['family_income']) < institution['family_income'])
            is_match.append(int(self.values['personal_income']) < institution['personal_income'])
            is_match.append(self.values['scholarship_type'].lower() in institution['scholarship_type'])
            is_match.append(self.values['languages'].lower() in institution['languages'])
            if institution['big_family']:
                is_match.append(self.values['big_family'] == 'Yes')
            if institution['disability']:
                is_match.append(self.values['disability'] == 'Yes')
            
            if False not in is_match:
                return institution

    def sanitize_inputs(self):
        try:
            self.values['age'] = int(self.values['age'])
        except Exception:
            self.values['age'] = 0

        try:
            self.values['family_income'] = int(self.values['family_income'])
        except Exception as e:
            self.values['family_income'] = 100000

        try:
            self.values['personal_income'] = int(self.values['personal_income'])
        except Exception as e:
            self.values['personal_income'] = 100000


def create_user_from_json(chat_id, user_as_json):
    user_deserialised = json.loads(user_as_json)
    new_user = User(chat_id)
    for key in questions.keys():
        new_user.values[key] = user_deserialised[key]
    new_user.last_question = user_deserialised['last_question']
    return new_user

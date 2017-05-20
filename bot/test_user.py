import user
import pytest


user.questions = {'age' : 'How old are you?', 'name': 'Hey! What’s your name'}

class TestClass:
    def test_user_create(self):
        new_user = user.User('123')
        assert new_user.chat_id =='123'

    def test_answer_name_question(self):
        new_user = user.User('123')
        new_user.last_question = 'name'
        new_user.answer_question('theo')
        assert new_user.values['name'] =='theo'

    def test_answer_age_question(self):
        new_user = user.User('123')
        new_user.last_question = 'age'
        new_user.answer_question(20)
        assert new_user.values['age'] == 20

    def test_find_next_question_age(self):
        new_user = user.User('123')
        new_user.values['name'] = 'theo'
        assert new_user.next_question() == 'age'

    def test_find_next_question_name(self):
        new_user = user.User('123')
        new_user.values['age'] = 5
        assert new_user.next_question() == 'name'

    def test_find_next_question_all_answered(self):
        new_user = user.User('123')
        new_user.values['age'] = 5
        new_user.values['name'] = 'theo'
        assert new_user.next_question() == None

    def test_generate_summary(self):
        new_user = user.User('123')
        new_user.values['age'] = 5
        new_user.values['name'] = 'theo'
        summary = new_user.get_summary()
        assert True == ('age: 5' in summary)
        assert True == ('name: theo' in summary)












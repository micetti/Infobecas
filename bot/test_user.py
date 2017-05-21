import user
from institutions import institutions

user.questions = {'age': 'How old are you?', 'name': 'Hey! Whats your name'}


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
        assert 'age: 5' in summary
        assert 'name: theo' in summary

    def test_match(self):
        new_user = user.User('123')
        values = {
            'age' : 20,
            'name': 'theo',
            'scholarship_type': 'Financial aid',
            'languages': 'english',
            'personal_income': '9.000',
            'family_income': 30000,
            'big_family': 'Yes',
            'disability': 'Yes',
            }
        new_user.values = values
        assert (new_user.get_match() == institutions[0])
        assert (new_user.get_match() != institutions[1])













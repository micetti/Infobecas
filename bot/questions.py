from telegram.emoji import Emoji
money_1 = Emoji.MONEY_WITH_WINGS
money_2 = Emoji.MONEY_BAG
disability = Emoji.WHEELCHAIR_SYMBOL
questions = {
'age' : 'How old are you?',
'name': 'Tell me your name, please.',
'scholarship_type': 'Which kind of scholarship are you interested in?',
'languages': 'Which is your primary language?',
'personal_income': 'What is your personal yearly income? ' + money_1,
'family_income': 'What is your families total income per year? ' + money_2,
'big_family': 'Do you have at least 3 siblings?',
'disability': 'Do you have a disability? ' + disability,
}
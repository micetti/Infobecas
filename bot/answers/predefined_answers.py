from telegram import Emoji

woman = Emoji.WOMAN
man = Emoji.MAN
undefined = Emoji.BLACK_QUESTION_MARK_ORNAMENT

welcome_message = "Hello, I'll help you find some grants"

predefined_answers={
'numbers': [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['0']],
'academic_degree': [['Higher education'], ['University degree'], ['Master']],
'scholarship_type': [['Financial aid'], ['Scholarships'], ['Investigation funding']],
'boolean_question': [['Yes'], ['No']],
'language_skills': [['English'], ['French'], ['Spanish']],
'financial_status': [['Sufficient'], ['No own income'], ['Financial need'], ['High financial need'], ['Financial emergency situation']],
'gender': [[woman], [man], [undefined]]
}
from telegram import Emoji

woman = Emoji.WOMAN
man = Emoji.MAN
undefined = Emoji.BLACK_QUESTION_MARK_ORNAMENT
waving_hand = Emoji.WAVING_HAND_SIGN
hourglass = Emoji.HOURGLASS

welcome_message = "Welcome to the Infobeca bot"
starting_message = "Hey there " + waving_hand + "!\nI am here to help you find a Grant.\nYou will see, it is riddiculosly easy."
start_explanation = "We are now going to have a little chat, so that I know just enough to help you. Get ready, first question:"
search_for_match = hourglass + "Hold on.\nI will now search for a match."

predefined_answers={
'academic_degree': [['Higher education'], ['University degree'], ['Master']],
'scholarship_type': [['Financial aid'], ['Scholarships'], ['Investigation funding']],
'disability': [['Yes'], ['No']],
'languages': [['English'], ['French'], ['Spanish']],
'financial_status': [['Sufficient'], ['No own income'], ['Financial need'], ['High financial need'], ['Financial emergency situation']],
'gender': [[woman], [man], [undefined]],
'big_family': [['Yes'], ['No']],
}
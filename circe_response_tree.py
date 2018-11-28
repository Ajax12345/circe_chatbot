import chatterbot as bot
import sqlite3, re, json

chat = bot.Chatterbot('circe')


def create_ul(f):
    def _wrapper(*args, **kwargs):
        _r = f(*args, **kwargs)
        return _r if not _r else '<ul>{}</ul>'.format('\n'.join(f'<li><p class="circe_text">{i}</p></li>' for i in _r))
    return _wrapper

@chat.welcome
def welcome():
    *_, _name = [b for _, b in sqlite3.connect('all_users.db').cursor().execute("SELECT * FROM users")]
    first_name = re.findall("^\w+", _name)[0]
    return chat.ChatterbotResponse(f'Hello, {first_name}! I am Circe, and I would like to discuss the fascinating field of humanities with you.', 1, subsequent=[lambda :"Tell me, have you selected a major?"])

@chat.chatterstream(1)
def has_major(_message:str) -> bot.chatRedirect:
    _parsed = [i.lower() for i in re.findall('\w+', _message.lower())]
    return bot.chatRedirect(2 if 'yes' in _parsed else 3)

@chat.chatterstream(2)
def second_message(_message:str):
    return chat.ChatterbotResponse('Good for you! Is your major a Humanity?', 4)

@chat.chatterstream(4)
def is_humanity(_message:str) -> bot.chatRedirect:
    return bot.chatRedirect(5 if 'yes' in [i.lower() for i in re.findall('\w+', _message.lower())] else 6)


@chat.chatterstream(5)
def best_case(_message:str):
    return chat.ChatterbotResponse("Great! I wish you the best of luck! Before you go, <a href='https://www.washingtonpost.com/news/answer-sheet/wp/2017/10/18/why-we-still-need-to-study-the-humanities-in-a-stem-world/' class='circe_link'>here</a> is an article that expands upon the import role of humanities in society. Have fun!", chat.end_chat)

@chat.chatterstream(6)
def get_user_scale(_message):
    return chat.ChatterbotResponse("On a scale of 1 to 10, how interested are you in switching to the humanities?", 7)

@chat.chatterstream(7)
def read_user_scale(_message):
    _results = [i for i in re.findall('\w+', _message.lower()) if i.isdigit() or i.lower() in chat.digits]
    if not _results:
        return bot.chatRedirect(8)
    if len(_results) > 1:
        return bot.chatRedirect(9)
    new_val = dict(zip(chat.digits, range(1, 11))).get(_results[0], int(_results[0]))
    
    return bot.chatRedirect(10 if new_val == 10 else 11 if 5 <= new_val < 10 else 25)

@chat.chatterstream(11)
def mid_range(_message):
    *_, _name = [b for _, b in sqlite3.connect('all_users.db').cursor().execute("SELECT * FROM users")]
    first_name = re.findall("^\w+", _name)[0]
    return chat.ChatterbotResponse(f"It seems you are interested in the humanities, {first_name}!", 19, subsequent=[lambda :"Are you currently taking any humanity courses, or will have any required humanities in the future?"])

@chat.chatterstream(10)
def positive_result(_message):
    return chat.ChatterbotResponse("Wonderful! Do you need help finding a humanities major at your college?", 14)

@chat.chatterstream(14)
def needs_help_find_major(_message):
    return bot.chatRedirect(15 if 'yes' in _message.lower() else 16)



@chat.chatterstream(15)
def find_college_majors(_message):
    return chat.ChatterbotResponse("I can help! What is your university name?", 17)

@create_ul
def get_humanity_majors(_school:str) -> list:
    with open('parsed_colleges_and_majors.json') as f:
        _all_schools = json.load(f)
    
    _resulting_school = [a for a, b in _all_schools.items() if _school.lower() in a.lower() or a.lower() in _school.lower()]
    print('resulting school', _resulting_school)
    if not _resulting_school:
        return False
    headers = ['Communication, Journalism & Related Programs', 'Philosophy & Religious Studies', 'Area, Ethnic, Cultural, & Gender Studies', 'History', 'Foreign Language, Literatures & Linguistics', 'Theology & Religious Vocations', 'English Language, Literature & Letters', 'Visual & Performing Arts', 'Liberal Arts & Sciences, Gen Studies & Humanities']
    return [i for b in headers for i in _all_schools[_resulting_school[0]].get(b, [])]


@chat.chatterstream(17)
def locate_school(_message):
    with open('all_schools.json') as f:
        schools = [i for b in json.load(f) for i in b]
    _option1 = [i for i in schools if i.lower() in _message.lower()]
    if _option1:
        _result = get_humanity_majors(_option1[0])
        #lambda :"<i>The arts and humanities teach us who we are and what we can be. They lie at the very core of the culture of which we’re a part</i>\n-Ronald Reagan", lambda :"Goodbye!"
        return chat.ChatterbotResponse("Sorry, I cannot find your school. Can you be more specific?", 17) if not _result else chat.ChatterbotResponse(f"Here are the humanities I found at {_option1[0]}:\n {_result}", 40, subsequent=[lambda :"Thank you for exploring the humanities with me!", lambda :"would you like to run another college search?"])
    with open('schools_with_abbrevs.json') as f:
        new_schools = json.load(f)
    new_options = [b for a, b in new_schools if a.lower() in _message.lower()]
    if new_options:
        _result = get_humanity_majors(new_options[0])
        return chat.ChatterbotResponse("Sorry, I cannot find your school. Can you be more specific?", 17) if not _result else chat.ChatterbotResponse(f"Here are the humanities I found at {new_options[0]}:\n {_result}", 40, subsequent=[lambda :"Thank you for exploring the humanities with me!", lambda :"would you like to run another college search?"])
    return chat.ChatterbotResponse("Sorry, I cannot find your school. Can you be more specific?", 17)


@chat.chatterstream(16)
def end_positive(_message):
    return chat.ChatterbotResponse("Very well, best of luck!", chat.end_chat)



@chat.chatterstream(8)
def scale_not_found(_message):
    return chat.ChatterbotResponse('Sorry, I cannot interpret your scale. Can you enter your value again?', 7)

@chat.chatterstream(9)
def more_specific(_message):
    return chat.ChatterbotResponse('Sorry, can you be more specific?', 7)

@chat.chatterstream(3)
def second_message(_val):
    *_, _name = [b for _, b in sqlite3.connect('all_users.db').cursor().execute("SELECT * FROM users")]
    first_name = re.findall("^\w+", _name)[0]
    return chat.ChatterbotResponse(f'What are some of your skills, {first_name}?', 30)

@chat.chatterstream(19)
def interpret_interested_medium(_message):

    return chat.ChatterbotResponse("What humanities courses are you currently taking, or will take later?", 21) if 'yes' in [i.lower() for i in re.findall('\w+', _message.lower())] else bot.chatRedirect(25)

@chat.chatterstream(21)
def get_humanities(_message):
    with open('humanities_benefits.json') as f:
        data = json.load(f)

    _results = [i['comment'] for i in data if i['subject'].lower() in _message.lower()]
    print('_results here for', _message, _results)
    return bot.chatRedirect(28) if not _results else chat.ChatterbotResponse(_results[0], 14, subsequent=[lambda :"Would you like to see a list of additional humanity options at your school?"])
    

@chat.chatterstream(25)
def query_values(_message):
    *_, _name = [b for _, b in sqlite3.connect('all_users.db').cursor().execute("SELECT * FROM users")]
    first_name = re.findall("^\w+", _name)[0]
    return chat.ChatterbotResponse(f"{first_name}, what are some things that you value?", 26)

@chat.chatterstream(26)
def get_values(_message):
    with open('humanities_values.json') as f:
        _values = json.load(f)
    _options = [i['description'] for i in _values if (i['value'].lower() in _message.lower() if isinstance(i['value'], str) else any(c.lower() in _message.lower() for c in i['value']))]
    return chat.ChatterbotResponse("The humanities have, for centuries, enabled mankind to think beyond itself, and grapple with the mysteries of the universe." if not _options else _options[0], 27, subsequent=[lambda :"Would you like me to find you a listing of humanities majors at your college?"])

@chat.chatterstream(27)
def possible_get_values(_message):
    return bot.chatRedirect(15 if 'yes' in _message.lower() else 16)

@chat.chatterstream(28)
def not_clear(_message):
    return chat.ChatterbotResponse("Sorry, I do not know about those humanity genres yet. Can you be more specific?", 21)


def matching_skill_banner(options:list, _name:str) -> str:
    return (f'Ok, {_name}, I found a humanity that matches your skills:\n' if len(options) == 1 else f"Ok, {_name}, here are the humanities that match your skills:\n")+'<ul>{}</ul>'.format('\n'.join(f'<li><p class="circe_text">{i}</p></li>' for i in options))

@chat.chatterstream(30)
def get_skills(_message):
    *_, _name = [b for _, b in sqlite3.connect('all_users.db').cursor().execute("SELECT * FROM users")]
    first_name = re.findall("^\w+", _name)[0]
    with open('humanities_skills.json') as f:
        data = json.load(f)
    _majors = [i['major'] for i in data if i['skill'].lower() in _message.lower()]
    print('possible majors', _majors)
    return chat.ChatterbotResponse("I do not know much about that. Can you tell me more? I, like you, am a student!", 31) if not _majors else chat.ChatterbotResponse(matching_skill_banner(_majors, first_name), 27, subsequent=[lambda :"Would you like to see a listing of possible humanities at your school?"])

@chat.chatterstream(40)
def terminate_or_search(_message):
    return bot.chatRedirect(15) if "yes" in _message.lower() else chat.ChatterbotResponse("Ok, goodby!", chat.end_chat)

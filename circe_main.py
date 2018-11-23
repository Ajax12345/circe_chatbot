import flask, random, string, json
import circe_users as _user
from circe_response_tree import chat as _chat


app = flask.Flask(__name__)
app.secret_key = ''.join(random.choice(string.printable) for _ in range(10))


@app.route('/', methods=['GET'])
def home():
    flask.session['message'] = 0
    return flask.render_template('circe_page.html', users = _user.Users.all_users())


@app.route('/add_user')
def add_user():
    _name = flask.request.args.get('name')
    _avatar, _initials, new_user_obj = _user.Users.add_user(_name)
    return flask.jsonify({"success":"True", 'html':flask.render_template('display_users.html', users=new_user_obj), 'num':len(new_user_obj), 'avatar':_avatar, 'initials':_initials})


@app.route('/get_welcome_message')
def get_welcome_message():
    _response = _chat.build('', 0)
    print(_response.html)
    flask.session['message'] = _response.next_node
    return flask.jsonify({'success':'True', 'html':_response.html})

@app.route('/get_circe_response')
def get_circe_response():
    _message = flask.request.args.get('message')
    _response = _chat.build(_message, flask.session['message'])
    flask.session['message'] = _response.next_node
    return flask.jsonify({"success":'True', 'html':_response.html})

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    app.debug = True
    app.run()

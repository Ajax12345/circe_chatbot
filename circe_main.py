import flask, random, string, json
import circe_users as _user

app = flask.Flask(__name__)
app.secret_key = ''.join(random.choice(string.printable) for _ in range(10))

@app.route('/', methods=['GET'])
def home():
    return flask.render_template('circe_page.html', users = _user.Users.all_users())


@app.route('/add_user')
def add_user():
    _name = flask.request.args.get('name')
    new_user_obj = _user.Users.add_user(_name)
    return flask.jsonify({"success":"True", 'html':flask.render_template('display_users.html', users=new_user_obj), 'num':len(new_user_obj)})

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
import configparser
import json

import requests
from bottle import Bottle, run, jinja2_view, jinja2_template, TEMPLATE_PATH, redirect, request, response
from slackclient import SlackClient

from imeerk.migrations import MigrationInit
from imeerk.sessions import DbSessions
from imeerk.users import DbUser
from imeerk.users import DbUsers

config = configparser.RawConfigParser()
config.read('local.cfg')

url = config.get('imeerk', 'url')
host = config.get('imeerk', 'host')
port = int(config.get('imeerk', 'port'))
db = config.get('imeerk', 'dbname')
client_id = config.get('slack-app', 'client_id')
client_secret = config.get('slack-app', 'client_secret')
scope = ["identify", "users.profile:write", "users.profile:read"]

TEMPLATE_PATH[:] = ['templates']
app = Bottle()


@app.get("/")
def index():
    token = request.get_cookie('token', 'guest')
    if token == 'guest':
        return jinja2_template(
            'login.html',
            slack_auth_url="https://slack.com/oauth/authorize?client_id={0}&scope={1}&redirect_uri={2}".format(
                client_id,
                " ".join(scope),
                "{0}/slack/login".format(url)
            )
        )
    else:
        return redirect(DbSessions(db).user(token).url())


@app.route("/slack/login")
def slack_login():
    code = request.query['code']
    result = requests.get(
        "https://slack.com/api/oauth.access?client_id={0}&client_secret={1}&code={2}&redirect_uri={3}".format(
            client_id,
            client_secret,
            code,
            "/slack/login".format(url)
        )
    )
    slack_token = result.json()['access_token']
    team = result.json()['team_id']

    sc = SlackClient(slack_token)
    result = sc.api_call('users.profile.get')
    if result['ok']:
        email = result['profile']['email']
        users = DbUsers(db)
        if not users.contains(email):
            users.add(email)
            DbUser(db, email).chats().add(
                team=team,
                token=slack_token,
                profile=json.dumps(result['profile'])
            )
        token = DbSessions(db).add(email)
        response.add_header('Set-Cookie', 'token={0}; Path=/; HttpOnly;'.format(token))
        return redirect('/')


@app.get('/user/<email>')
@jinja2_view('dashboard.html')
def dashboard(email):
    # type: (str) -> dict
    return {
        'email': email,
        'calendars': DbUser(db, email).calendars().as_html(),
        'add_new_calendar_url': app.get_url('add_calendar', email=email)
    }


@app.get('/user/<email>/calendars/ical/add', name='add_calendar')
@jinja2_view('calendars/ical/add.html')
def add_calendar(email):
    # type: (str) -> dict
    return {
        'email': email,
        'add_calendar_form': app.get_url('add_calendar_form', email=email)
    }


@app.post('/user/<email>/calendars/ical/add', name='add_calendar_form')
def add_calendar_form(email):
    # type: (str) -> str
    DbUser(db, email).calendars().add(request.forms['url'], request.forms['name'])
    return redirect('/user/' + email)


if __name__ == "__main__":
    MigrationInit(db).apply()
    run(app, host=host, port=port)

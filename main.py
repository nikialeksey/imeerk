import configparser
import json
import base64

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
store_dir = config.get('imeerk', 'store')
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
            "{0}/slack/login".format(url)
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
        'calendars': DbUser(db, email).calendars().as_html(
            lambda url: app.get_url('calendar', calendar=base64.b64encode(url.encode('utf-8')).decode('utf-8'))
        ),
        'add_new_calendar_url': app.get_url('add_calendar', email=email)
    }


@app.get('/calendars/ical/<calendar>', name='calendar')
@jinja2_view('calendars/ical/ical.html')
def calendar(calendar: str) -> dict:
    token = request.get_cookie('token', 'guest')
    return {
        'calendar': DbSessions(db)
        .user(token)
        .calendars()
        .calendar(base64.b64decode(calendar).decode('utf-8'))
        .as_html(
            lambda url: app.get_url('sync_calendar', calendar=base64.b64encode(url.encode('utf-8')).decode('utf-8'))
        )
    }


@app.get('/calendars/ical/<calendar>/sync', name='sync_calendar')
@jinja2_view('calendars/ical/sync.html')
def sync_calendar(calendar: str) -> dict:
    DbSessions(db)\
        .user(
            request.get_cookie('token', 'guest')
        )\
        .calendars()\
        .calendar(
            base64.b64decode(calendar).decode('utf-8')
        )\
        .sync(store_dir)
    return {}


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

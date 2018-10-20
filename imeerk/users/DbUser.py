from imeerk.calendars.icalendar import DbIcalCalendars
from imeerk.calendars.icalendar import IcalCalendars
from imeerk.chats.slack import DbSlackChats
from imeerk.chats.slack import SlackChats
from .User import User


class DbUser(User):

    def __init__(self, db_name: str, email: str) -> None:
        self.db_name = db_name
        self.email = email

    def chats(self) -> SlackChats:
        return DbSlackChats(self.db_name, self.email)

    def calendars(self) -> IcalCalendars:
        return DbIcalCalendars(self.db_name, self.email)

    def url(self) -> str:
        return '/user/' + self.email

from .User import User
from imeerk.chats.slack import DbSlackChats
from imeerk.chats.slack import SlackChats
from imeerk.calendars.icalendar import IcalCalendars
from imeerk.calendars.icalendar import DbIcalCalendars


class DbUser(User):

    def __init__(self, db_name: str, email: str) -> None:
        self.db_name = db_name
        self.email = email

    def chats(self):
        # type: () -> SlackChats
        return DbSlackChats(self.db_name, self.email)

    def calendars(self):
        # type: () -> IcalCalendars
        return DbIcalCalendars(self.db_name, self.email)

    def url(self) -> str:
        return '/user/' + self.email

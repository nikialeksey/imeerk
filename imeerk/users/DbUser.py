from imeerk.calendars.icalendar import DbIcalCalendars
from imeerk.calendars.icalendar import IcalCalendars
from imeerk.notifications.slack import DbSlackNotifications
from imeerk.notifications.slack import SlackNotifications
from .User import User


class DbUser(User):

    def __init__(self, db_name: str, email: str) -> None:
        self.db_name = db_name
        self.email = email

    def notifications(self) -> SlackNotifications:
        return DbSlackNotifications(self.db_name, self.email)

    def calendars(self) -> IcalCalendars:
        return DbIcalCalendars(self.db_name, self.email)

    def url(self) -> str:
        return '/user/' + self.email

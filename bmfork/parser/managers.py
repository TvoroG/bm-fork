from events import (BetcityTeamVsTeamEvent,
                    MarathonTeamVsTeamWithoutEqEvent,
                    MarathonTeamVsTeamWithEqEvent)

class Manager(object):

    def create_event(self, ph, e):
        for event_cls in self.events:
            event = event_cls.create(ph, e)
            if event is not None:
                return event
        return None


class BetcityManager(Manager):
    events = [BetcityTeamVsTeamEvent,]


class MarathonManager(Manager):
    events = [MarathonTeamVsTeamWithoutEqEvent,
              MarathonTeamVsTeamWithEqEvent,]


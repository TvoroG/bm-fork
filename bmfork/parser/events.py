# -*- coding: utf-8 -*-

class Event(object):
    def create(self, ph, e):
        return None

    @classmethod
    def assert_col_num(cls, l):
        return cls.col_num == l


class BetcityEvent(Event):
    pass


class BetcityTeamVsTeamEvent(BetcityEvent):
    col_num = 14
    
    def __init__(self, ph, e):
        self.ph = ph
        self.e = e

    @classmethod
    def create(cls, ph, e):
        cols = e.select('tr > td')
        chead = ph.find_previous_sibling(class_='chead')
        chead.extend(ph.find_next_sibling(class_='chead'))

        is_ok = (cls.assert_col_num(len(cols)) and
                 cls.assert_team_vs_team(chead[0]))
        if is_ok:
            return cls(ph, e)
        return None

    @classmethod
    def assert_team_vs_team(cls, chead):
        tds = chead.select('tr > td')
        return (tds[1].get_text() == 'Команда 1' and
                tds[4].get_text() == 'Команда 2')
        

class MarathonEvent(Event):
    pass


class MarathonTeamVsTeamEvent(MarathonEvent):

    def __init__(self, ph, e):
        self.ph = ph
        self.e = e

    @classmethod
    def create(cls, ph, e):
        cols = e.select('tr.event-header > td')
        names = e.select('.name')
        names.extend(e.select('.today-name'))

        print len(cols)
        is_ok = (cls.assert_col_num(len(cols)) and
                 cls.assert_team_vs_team(names[0]))
        if is_ok:
            return cls(ph, e)
        return None

    @classmethod
    def assert_team_vs_team(cls, names):
        members = names.select('.member-name')
        members.extend(names.select('.today-member-name'))
        return len(members) == 2


class MarathonTeamVsTeamWithoutEqEvent(MarathonTeamVsTeamEvent):
    col_num = 7


class MarathonTeamVsTeamWithEqEvent(MarathonTeamVsTeamEvent):
    col_num = 11

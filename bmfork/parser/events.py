# -*- coding: utf-8 -*-
from models import Synonym
from headersname import OBJ_LIST

class Event(object):

    def get_objects_ids(self):
        objs_ids = {}
        for obj in OBJ_LIST:
            if obj in self.bet_val:
                objs_ids[obj] = Synonym.query.filter_by(
                    name=self.bet_val[obj]).first()
        return objs_ids


class BetcityEvent(Event):
    def __init__(self, header, bet_val):
        self.header = header
        self.bet_val = bet_val
        self.objs_ids = self.get_objects_ids()


class MarathonEvent(Event):
    def __init__(self, header, bet_val):
        self.header = header
        self.bet_val = bet_val
        self.objs_ids = self.get_objects_ids()



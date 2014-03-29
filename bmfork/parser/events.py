# -*- coding: utf-8 -*-
from models import Synonym
from headersname import OBJ_LIST
from utils import create_sets_from

class Event(object):

    def __eq__(self, ev):
        return (self.header == ev.header and
                self.is_equal_objects_ids(ev))

    def get_ids_sets(self, obj):
        res_s = set()
        sets = self.objs_ids[obj].values()
        for s in sets:
            res_s.union(s)
        return res_s
                
    def is_equal_objects_ids(self, ev):
        for obj in OBJ_LIST:
            if obj in self.bet_val and obj in ev.bet_val:
                if not self.get_ids_sets(obj) & ev.get_ids_sets(obj):
                    return False
        return True

    def get_objects_ids(self):
        objs_ids = {}
        for obj in OBJ_LIST:
            if obj in self.bet_val:
                oids = Synonym.query.filter_by(name=self.bet_val[obj])
                objs_ids[obj] = create_sets_from(oids)
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



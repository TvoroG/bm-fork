# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from headers import BetcityHeader, MarathonHeader
from events import BetcityEvent, MarathonEvent
from headersname import betcity_headers_name, marathon_headers_name, OBJECT1, OBJECT2

class Manager(object):
    headers_name = None

    def create_header(self, bg):
        return None

    def create_event(self, ph, e):
        return None

    def get_bets_positions(self, col):
        pos = {}
        for i, td in enumerate(col):
            name = td.get_text(strip=True).lower()
            trans_name = self.headers_name.get(name, name)
            if trans_name in pos:
                pos[trans_name] = [pos[trans_name], i]
            else:
                pos[trans_name] = i
        return pos

    def get_bets_values(self, bp, col):
        val = {}
        lcol = len(col)
        for k in bp:
            if isinstance(bp[k], list):
                val[k] = []
                for l in bp[k]:
                    if l < lcol:
                        val[k].append(col[l].get_text(strip=True))
                    else:
                        val[k].append(None)
            elif bp[k] < lcol:
                val[k] = col[bp[k]].get_text(strip=True)
            else:
                val[k] = None
        return val


class BetcityManager(Manager):
    headers_name = betcity_headers_name

    def create_header(self, bg):
        head_sel = bg.select('thead')
        if not head_sel:
            return None

        cheads = bg.select('.chead')
        if not cheads:
            return None
        col = cheads[0].select('tr.th > td')
        
        bet_pos = self.get_bets_positions(col)
        return BetcityHeader(head_sel[0], bet_pos)

    def create_event(self, ph, e):
        tr = e.select('tr.tc')
        tr.extend(e.select('tr.tcl'))
        if not tr:
            return None

        tds = tr[0].select('td')
        bet_val = self.get_bets_values(ph.bet_pos, tds)
        return BetcityEvent(ph, bet_val)


class MarathonManager(Manager):
    headers_name = marathon_headers_name

    def create_header(self, bg):
        head_sel = bg.select('.category-path')
        if not head_sel:
            return None
        
        sel = bg.select('table.foot-market tr.coupone-labels')
        if not sel:
            return None
        sel = sel[0]

        cheads = sel.select('.first.left-name')
        cheads.extend(sel.select('a.hint'))
        bet_pos = self.get_bets_positions(cheads)
        return MarathonHeader(head_sel[0], bet_pos)

    def create_event(self, ph, e):
        ev_header = e.select('.event-header')
        if not ev_header:
            return None
        ev_header = ev_header[0]

        tds = ev_header.select('td .selection-link')
        if not tds:
            return None

        tds.insert(0, BeautifulSoup('<html></html>'))
        bet_val = self.get_bets_values(ph.bet_pos, tds)

        mems = ev_header.select('.member-name')
        mems.extend(ev_header.select('.today-member-name'))
        if len(mems) != 2:
            return None

        bet_val[OBJECT1] = mems[0].get_text(strip=True)
        bet_val[OBJECT2] = mems[1].get_text(strip=True)
        return MarathonEvent(ph, bet_val)

# -*- coding: utf-8 -*-
import sys
import mechanize
import urllib2
from bs4 import BeautifulSoup

from managers import BetcityManager, MarathonManager


class Bookmaker(object):
    def __init__(self):
        self.url = None
        self.cur_header = None
        super(Bookmaker, self).__init__()

    def parse(self):
        bm_events = []
        
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        
        bgs = self.get_bet_groups(soup)
        for bg in bgs:
            header = self.parse_header(bg)
            if header is not None:
                self.found_header(header)

            events = self.get_bet_group_events(bg)
            for e in events:
                event = self.parse_event(e)
                if event is not None:
                    bm_events.append(event)
                    self.found_event(event)
        
        return bm_events

    def parse_header(self, bg):
        return None

    def found_header(self, ph):
        return None

    def parse_event(self, e):
        return None

    def found_event(self, e):
        return None

    def get_html(self):
        return ''

    def open_connection(self):
        br = mechanize.Browser()
        br.open(self.url)
        return br

    def get_bet_groups(self, soup):
        return []

    def get_bet_group_events(self, bg):
        return []


# пока заблокировали
class Betcity(Bookmaker):
    def __init__(self):
        super(Betcity, self).__init__()
        self.url = 'http://betsbc.com/bets/bets.php'
        self.manager = BetcityManager()

    def parse_header(self, bg):
        self.cur_header = None
        header = self.manager.create_header(bg)
        return header
        
    def found_header(self, ph):
        self.cur_header = ph
        #print ''.join(ph.bet_pos.keys())

    def parse_event(self, e):
        if self.cur_header is None:
            return None
        event = self.manager.create_event(self.cur_header, e)
        return event

    def found_event(self, pe):
        #pass
        print ''.join(pe.objs_ids.keys())

    def get_html(self):
        br = self.open_connection()
        br.select_form(name='bets')
        
        # пока не выбираем долгосрочные ставки
        checkboxes = br.find_control(name='line_id[]').items
        for ch in checkboxes:
            ch.selected = True

        response = br.submit()
        return response.read()

    def get_bet_groups(self, soup):
        return soup.select('body > table')

    def get_bet_group_events(self, bg):
        return bg.select('#line')


class Marathon(Bookmaker):
    def __init__(self):
        super(Marathon, self).__init__()
        self.url = 'http://www.marathonbet.com/su/betting/all'
        self.manager = MarathonManager()

    def parse_header(self, bg):
        self.cur_header = None
        header = self.manager.create_header(bg)
        return header

    def found_header(self, ph):
        self.cur_header = ph
#        print ''.join(ph.bet_pos.keys())

    def parse_event(self, e):
        if self.cur_header is None:
            return None
        event = self.manager.create_event(self.cur_header, e)
        return event

    def found_event(self, pe):
#        pass
        print ''.join(pe.objs_ids.keys())

    def get_html(self):
        html = urllib2.urlopen(self.url)
        return html

    def get_bet_groups(self, soup):
        return soup.select('#container_EVENTS > .main-block-events')

    def get_bet_group_events(self, bg):
        sel = bg.select('table.foot-market > tbody')
        return sel
